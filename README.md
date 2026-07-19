# Real-ESRGAN WebGPU — WASM ブラウザアップスケーラー

> Real-ESRGAN を **ONNX Runtime Web** 経由で WebAssembly (WASM) に変換し、**WebGPU** アクセラレーションでブラウザ上で完全クライアントサイド動作させます。

![Real-ESRGAN WebGPU Demo](https://github.com/xororz/web-realesrgan/raw/master/src/assets/demo.jpg)

## 🌟 特徴

- **完全クライアントサイド** — 画像がサーバーに送信されません。プライバシー完全保護
- **WebGPU アクセラレーション** — 対応ブラウザでは GPU で高速推論
- **WASM フォールバック** — WebGPU 未対応環境でも動作 (CPU)
- **タイル処理** — 大きな画像もメモリ効率よく処理
- **複数モデル** — 高品質・高速・アニメ用など選択可能
- **アルファチャンネル対応** — PNG 透過画像もアップスケール可能

## 🚀 クイックスタート

### 前提条件

- Node.js >= 18
- npm >= 9

### インストール & 起動

```bash
# 1. リポジトリをクローン
git clone <your-repo-url>
cd web-realesrgan-wasm

# 2. 依存関係をインストール
npm install

# 3. 自己署名証明書を生成（WebGPU は HTTPS が必要）
chmod +x scripts/gen-cert.sh
bash scripts/gen-cert.sh

# 4. 開発サーバー起動
npm run dev
```

ブラウザで **https://localhost:8080** にアクセスしてください。
（自己署名証明書の警告が表示された場合は「続行」を選択）

### モデルの準備

アプリは起動時に HuggingFace から ONNX モデルを自動ダウンロードします。
初回のみダウンロードが発生し、以降はブラウザの IndexedDB にキャッシュされます。

| モデル | サイズ | 説明 |
|--------|--------|------|
| Real-ESRGAN x4plus | 67 MB | 最高品質 一般画像用 |
| Real-ESRGAN anime | 67 MB | アニメ・イラスト用 |
| Real-ESRGAN general | 67 MB | 高速 一般画像用 |

> **Note:** 上記は同じ ONNX ファイルを参照しています。実際のプロダクション用途では各モデルを個別に変換してください。

## 🔧 アーキテクチャ

```
PyTorch (.pth)
    │
    ▼
ONNX エクスポート (python/export_onnx.py)
    │
    ▼
ONNX Runtime Web (onnxruntime-web)
    │
    ├── WebGPU (推論) → GPU 高速パス
    │
    └── WASM  (推論) → CPU フォールバック
```

### パイプライン詳細

1. **画像入力** — ファイルドロップ / クリック選択
2. **前処理** — タイル分割、正規化、テンソル変換
3. **推論** — WebGPU または WASM で ONNX モデル実行
4. **後処理** — タイル結合、色補正、キャンバス描画
5. **出力** — プレビュー表示 & PNG ダウンロード

## 🧪 自分で ONNX 変換する場合

Python 環境で `python/export_onnx.py` を使用します：

```bash
cd python
pip install -r requirements.txt

# モデルダウンロード
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth

# ONNX 変換
python export_onnx.py \
    --input RealESRGAN_x4plus.pth \
    --output ../models/realesrgan-x4plus.onnx \
    --scale 4 \
    --num-block 23 \
    --dynamic
```

### 一括変換

```bash
chmod +x export_all_models.sh
bash export_all_models.sh
```

## 🌐 バックエンド比較

| バックエンド | 速度 | 対応ブラウザ | 初期化時間 |
|-------------|------|------------|-----------|
| WebGPU 🚀 | 最速 (GPU) | Chrome 113+, Edge 113+ | 1-3秒 (シェーダーコンパイル) |
| WASM (CPU) 🧠 | 中速 | 全ブラウザ | ほぼ0 |

WebGPU を使用するには HTTPS が必要です。自己証明書でも動作します。

## 📦 プロダクションビルド

```bash
npm run build
```

`dist/` ディレクトリに静的ファイルが出力されます。
任意のホスティングサービス (Vercel, Netlify, Cloudflare Pages, GitHub Pages) にデプロイ可能です。

### HTTPS の設定

WebGPU は HTTPS が必須です。Vercel / Netlify / Cloudflare Pages などは自動で HTTPS を提供します。

### CSP ヘッダー

必要に応じて以下の CSP を設定してください：

```http
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'wasm-unsafe-eval';
  connect-src 'self' https://huggingface.co blob:;
  img-src 'self' blob: data:;
```

## 📚 技術スタック

- **ONNX Runtime Web** — WebAssembly + WebGPU 推論エンジン
- **WebGPU** — GPU コンピュート API (Dawn / wgpu 実装)
- **WebAssembly (WASM)** — ポータブルバイナリ実行環境
- **RRDBNet** — Real-ESRGAN のベースアーキテクチャ (Residual-in-Residual Dense Block)

## 🔗 関連プロジェクト

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) — オリジナル PyTorch 実装 (Tencent ARC)
- [web-realesrgan](https://github.com/xororz/web-realesrgan) — TensorFlow.js 版ブラウザ Real-ESRGAN
- [ONNX Runtime Web](https://github.com/microsoft/onnxruntime) — Microsoft 製 ONNX 推論ランタイム
- [LiteRT.js](https://developers.googleblog.com/litertjs-googles-high-performance-web-ai-inference/) — Google 製 Web AI 推論 (2026年7月リリース)

## 📄 ライセンス

このプロジェクト自身のコード (`index.html`, `serve.py`, ドキュメント類) は
[WTFPL](./LICENSE) です。

同梱している以下のサードパーティ成果物は、それぞれ別のライセンスに従います
(いずれも copyleft ではなく、商用利用も可能な許諾型ライセンスです):

- `models/*.onnx` (Real-ESRGAN 学習済み重みの変換版) — BSD-3-Clause (Xintao Wang)
- `ort/*` (onnxruntime-web ビルド成果物) — MIT (Microsoft Corporation)
- `coi-serviceworker.js` — MIT (Guido Zuidhof and contributors)

詳細は [`THIRD-PARTY-NOTICES.md`](./THIRD-PARTY-NOTICES.md) を参照してください。

---

# Real-ESRGAN WebGPU — WASM Browser Upscaler (English)

> Run **Real-ESRGAN** entirely client-side in the browser via **ONNX Runtime Web** (WASM) with **WebGPU** acceleration.

## Features

- **100% Client-Side** — Images never leave your device
- **WebGPU Accelerated** — GPU inference on Chrome/Edge
- **WASM Fallback** — Works on all browsers without WebGPU
- **Tile Processing** — Memory-efficient large image handling
- **Multiple Models** — Quality/fast/anime presets
- **Alpha Channel Support** — PNG transparency preserved

## Quick Start

```bash
npm install
bash scripts/gen-cert.sh   # HTTPS certificate for WebGPU
npm run dev
```

Open **https://localhost:8080** in your browser.

## How It Works

```
PyTorch (.pth) → ONNX → ONNX Runtime Web → WebGPU / WASM
```

1. Load/convert model to ONNX format (or use pre-converted)
2. ONNX Runtime Web loads the model via WebAssembly
3. WebGPU backend runs inference on GPU (or WASM CPU fallback)
4. Result rendered to canvas, downloadable as PNG

## ONNX Export

```bash
cd python
pip install -r requirements.txt
python export_onnx.py --input RealESRGAN_x4plus.pth --output model.onnx
```

## Tech Stack

- **ONNX Runtime Web** — WASM + WebGPU inference engine
- **WebGPU** — Next-gen GPU compute API
- **WebAssembly** — Near-native execution in browser
- **RRDBNet** — Real-ESRGAN backbone architecture

## License

This project's own code (`index.html`, `serve.py`, docs) is [WTFPL licensed](./LICENSE).

Bundled third-party components carry their own licenses (all permissive,
none copyleft, all commercial-use friendly) — see
[`THIRD-PARTY-NOTICES.md`](./THIRD-PARTY-NOTICES.md):

- `models/*.onnx` (converted Real-ESRGAN weights) — BSD-3-Clause (Xintao Wang)
- `ort/*` (onnxruntime-web build artifacts) — MIT (Microsoft Corporation)
- `coi-serviceworker.js` — MIT (Guido Zuidhof and contributors)
