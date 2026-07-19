#!/bin/bash
# 全 Real-ESRGAN モデルを一括 ONNX 変換
set -euo pipefail

MODELS_DIR="./models"
ONNX_DIR="./onnx_models"
mkdir -p "$ONNX_DIR"

echo "=== Real-ESRGAN 一括 ONNX 変換 ==="

# 1. RealESRGAN_x4plus (フルモデル, 23ブロック)
if [ ! -f "$MODELS_DIR/RealESRGAN_x4plus.pth" ]; then
  echo "[DL] RealESRGAN_x4plus.pth をダウンロード中..."
  wget -O "$MODELS_DIR/RealESRGAN_x4plus.pth" \
    https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
fi
python export_onnx.py \
  --input "$MODELS_DIR/RealESRGAN_x4plus.pth" \
  --output "$ONNX_DIR/realesrgan-x4plus.onnx" \
  --scale 4 --num-block 23

# 2. RealESRGAN_x4plus_anime_6B (アニメ用, 6ブロック)
if [ ! -f "$MODELS_DIR/RealESRGAN_x4plus_anime_6B.pth" ]; then
  echo "[DL] RealESRGAN_x4plus_anime_6B.pth をダウンロード中..."
  wget -O "$MODELS_DIR/RealESRGAN_x4plus_anime_6B.pth" \
    https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus_anime_6B.pth
fi
python export_onnx.py \
  --input "$MODELS_DIR/RealESRGAN_x4plus_anime_6B.pth" \
  --output "$ONNX_DIR/realesr-anime-x4.onnx" \
  --scale 4 --num-block 6

# 3. realesr-general-x4v3 (軽量一般モデル)
if [ ! -f "$MODELS_DIR/realesr-general-x4v3.pth" ]; then
  echo "[DL] realesr-general-x4v3.pth をダウンロード中..."
  wget -O "$MODELS_DIR/realesr-general-x4v3.pth" \
    https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth
fi
python export_onnx.py \
  --input "$MODELS_DIR/realesr-general-x4v3.pth" \
  --output "$ONNX_DIR/realesr-general-x4v3.onnx" \
  --scale 4 --num-block 6

echo ""
echo "=== 完了 ==="
echo "出力ファイル:"
ls -lh "$ONNX_DIR/"
