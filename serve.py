#!/usr/bin/env python3
"""Cross-Origin Isolation 対応の静的サーバー。

`python -m http.server` は COOP/COEP を出さないため、ブラウザ側で
SharedArrayBuffer が使えず onnxruntime-web の WASM マルチスレッドが
単一スレッドに落ちる。このサーバーは COOP/COEP と CORP を付与して
`crossOriginIsolated === true` を成立させ、全コアで WASM を回せる
ようにする。

    python3 serve.py                    # http://localhost:8000 (COOP/COEP あり)
    python3 serve.py 8080               # ポート指定
    python3 serve.py 8080 0.0.0.0       # バインド先も指定
    python3 serve.py --no-coi           # COOP/COEP なし (GitHub Pages と同じ挙動を再現。
                                        # coi-serviceworker が正しく動いてるか確認する用)
"""
import http.server
import socketserver
import sys
import urllib.request
from pathlib import Path

NO_COI = '--no-coi' in sys.argv
_pos = [a for a in sys.argv[1:] if not a.startswith('--')]
PORT = int(_pos[0]) if len(_pos) > 0 else 8000
HOST = _pos[1] if len(_pos) > 1 else ''

# ORT を同一オリジンから配信する (CDN + COEP + proxy worker の相性で
# "worker not ready" が出るのを回避するため)。
ORT_VERSION = '1.21.0'
ORT_CDN = f'https://cdn.jsdelivr.net/npm/onnxruntime-web@{ORT_VERSION}/dist/'
ORT_FILES = [
    'ort.webgpu.min.js',
    'ort-wasm-simd-threaded.jsep.mjs',
    'ort-wasm-simd-threaded.jsep.wasm',
]


def ensure_ort():
    d = Path('ort')
    d.mkdir(exist_ok=True)
    for name in ORT_FILES:
        p = d / name
        if p.exists() and p.stat().st_size > 0:
            continue
        url = ORT_CDN + name
        print(f'DL: {url}')
        try:
            urllib.request.urlretrieve(url, p)
        except Exception as e:
            print(f'  失敗: {e} — スキップします (standalone.html が CDN にフォールバックします)')


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.wasm': 'application/wasm',
        '.onnx': 'application/octet-stream',
        '.mjs': 'application/javascript',
    }

    def end_headers(self):
        if not NO_COI:
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
            self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        if self.path.endswith(('.onnx', '.wasm')):
            self.send_header('Cache-Control', 'public, max-age=86400')
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


ensure_ort()

with Server((HOST, PORT), Handler) as httpd:
    where = HOST or 'localhost'
    mode = 'COOP/COEP 無し (GitHub Pages と同じ挙動、SW 検証用)' if NO_COI else 'COOP/COEP 有り'
    print(f'{mode} で配信中: http://{where}:{PORT}')
    print('  → http://%s:%d/ を開いてください' % (where, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
