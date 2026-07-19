# サードパーティ帰属表示 / Third-Party Notices

このプロジェクトは以下の第三者ソフトウェア・学習済みモデルを同梱・再配布しています。
それぞれ元のライセンス条件に従います。プロジェクト独自のコード (`index.html`, `serve.py`,
ドキュメント類) のライセンスは [`LICENSE`](./LICENSE) (WTFPL) を参照してください。

**いずれも許諾型ライセンス (BSD-3-Clause / MIT / Apache-2.0) であり、
copyleft (GPL/LGPL/AGPL) や非商用限定の条件は含まれていません。**
(プロジェクト自身のコードは WTFPL のためさらに緩く、事実上無条件です。)

---

## 1. Real-ESRGAN 学習済みモデル重み

- **同梱物**: `models/RealESRGAN_x2.onnx`, `RealESRGAN_x2_fp16.onnx`,
  `RealESRGAN_x4.onnx`, `RealESRGAN_x4_fp16.onnx`,
  `RealESRGAN_x8.onnx`, `RealESRGAN_x8_fp16.onnx`
  (いずれも [xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) の
  公式配布 `.pth` を `python/export_onnx.py` で ONNX に変換したもの)
- **ライセンス**: BSD 3-Clause License
- **著作権者**: Copyright (c) 2021, Xintao Wang

```
BSD 3-Clause License

Copyright (c) 2021, Xintao Wang
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

**学習データについての開示**: 上記の重みには専用の別ライセンスは存在せず、
リポジトリ本体と同じ BSD-3-Clause で配布されています。ただし一般用モデルの学習には
DIV2K / Flickr2K / OST300 という学術データセットの画像が使われており、
これら「元画像」自体は研究目的での利用を想定したデータセットです。学習済み重みへの
利用制限として作者・Tencent ARC Lab から明示的な注記はなく、これらの重みは商用含め
広く利用されていますが、法的に完全に整理された論点ではないため、参考情報として
ここに明記しておきます。

---

## 2. ONNX Runtime Web (onnxruntime-web)

- **同梱物**: `ort/ort.webgpu.min.js`, `ort/ort-wasm-simd-threaded.jsep.mjs`,
  `ort/ort-wasm-simd-threaded.jsep.wasm`
  ([microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) の
  ビルド済み配布物。`serve.py` が初回起動時に jsDelivr CDN から取得)
- **ライセンス**: MIT License
- **著作権者**: Copyright (c) Microsoft Corporation

```
MIT License

Copyright (c) Microsoft Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**内部同梱コンポーネントについて**: 上記の `.wasm` バイナリには ONNX Runtime が
内部で静的リンクしている protobuf / onnx / Eigen / oneDNN など複数のサードパーティ
コンポーネントが含まれます。それぞれの詳細なライセンス条文は本リポジトリには
同梱せず、公式の一覧を参照してください:
https://github.com/microsoft/onnxruntime/blob/main/ThirdPartyNotices.txt

---

## 3. coi-serviceworker

- **同梱物**: `coi-serviceworker.js`
  ([gzuidhof/coi-serviceworker](https://github.com/gzuidhof/coi-serviceworker))
- **ライセンス**: MIT License
- **著作権者**: Copyright (c) 2021 Guido Zuidhof and contributors
- 元となったアイデアは [@stefnotch のブログ記事](https://dev.to/stefnotch/enabling-coop-coep-without-touching-the-server-2d3n)
  に由来する旨が原リポジトリの README に記載されています。

```
MIT License

Copyright (c) 2021 Guido Zuidhof and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 4. (参考) BasicSR — 開発時のみ使用、非同梱

- **用途**: `python/export_onnx.py` (`.pth` → `.onnx` 変換スクリプト) が
  `pip install` 経由で利用する開発時依存。変換後のバイナリのみを本リポジトリに
  同梱しており、BasicSR 自体のコードは同梱・再配布していません。
- **ライセンス**: Apache License 2.0 ([XPixelGroup/BasicSR](https://github.com/XPixelGroup/BasicSR))
- 同梱・再配布していないため Apache-2.0 の帰属表示義務は発生しませんが、
  透明性のためここに記載しています。
