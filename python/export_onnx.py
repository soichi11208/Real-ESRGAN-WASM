#!/usr/bin/env python3
"""
Real-ESRGAN PyTorch → ONNX 変換スクリプト

Usage:
    pip install torch basicsr onnx onnxruntime
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
    python export_onnx.py --input RealESRGAN_x4plus.pth --output realesrgan-x4plus.onnx

Options:
    --input      入力 .pth モデルパス (default: RealESRGAN_x4plus.pth)
    --output     出力 .onnx パス (default: realesrgan-x4plus.onnx)
    --scale      アップスケール倍率 (default: 4)
    --num-block  RRDB ブロック数 (default: 23)
    --opset      ONNX opset version (default: 17)
    --dynamic    動的サイズを有効化 (推奨)   (default: True)
"""

import argparse
import torch
import torch.onnx


def main(args):
    # ──── RRDBNet (Real-ESRGAN の基本アーキテクチャ) ────
    from basicsr.archs.rrdbnet_arch import RRDBNet

    model = RRDBNet(
        num_in_ch=3,
        num_out_ch=3,
        num_feat=64,
        num_block=args.num_block,
        num_grow_ch=32,
        scale=args.scale,
    )

    # 重みをロード
    state_dict = torch.load(args.input, map_location='cpu')
    # Real-ESRGAN のチェックポイントは 'params_ema' キーに保存
    if 'params_ema' in state_dict:
        model.load_state_dict(state_dict['params_ema'])
    elif 'params' in state_dict:
        model.load_state_dict(state_dict['params'])
    else:
        model.load_state_dict(state_dict)

    model.eval()
    model.cpu()
    print(f"[✓] モデルロード完了: {args.input}")
    print(f"    アーキテクチャ: RRDBNet(scale={args.scale}, num_block={args.num_block})")

    # ──── ダミー入力 ────
    dummy_input = torch.randn(1, 3, 64, 64)

    # ──── ONNX エクスポート ────
    input_names = ["input"]
    output_names = ["output"]

    if args.dynamic:
        dynamic_axes = {
            "input": {2: "height", 3: "width"},
            "output": {2: "height", 3: "width"},
        }
        print("[i] 動的サイズ有効: 任意サイズの入力を許容")
    else:
        dynamic_axes = None
        print("[i] 固定サイズ: 64x64 入力のみ")

    with torch.no_grad():
        torch.onnx.export(
            model,
            dummy_input,
            args.output,
            verbose=False,
            input_names=input_names,
            output_names=output_names,
            dynamic_axes=dynamic_axes,
            opset_version=args.opset,
            export_params=True,
            do_constant_folding=True,
        )

    print(f"[✓] ONNX エクスポート完了: {args.output}")

    # ──── 簡単な検証 ────
    try:
        import onnx
        onnx_model = onnx.load(args.output)
        onnx.checker.check_model(onnx_model)
        print(f"[✓] ONNX チェック通過: {onnx_model.graph.name}")
        print(f"    入力: {[i.name + str(i.type.tensor_type.shape) for i in onnx_model.graph.input]}")
        print(f"    出力: {[o.name for o in onnx_model.graph.output]}")
    except ImportError:
        print("[!] onnx パッケージが未インストールのためチェックをスキップ")
    except Exception as e:
        print(f"[!] ONNX チェックで警告: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-ESRGAN → ONNX converter")
    parser.add_argument("--input", default="RealESRGAN_x4plus.pth",
                        help="入力 .pth モデルファイル")
    parser.add_argument("--output", default="realesrgan-x4plus.onnx",
                        help="出力 .onnx ファイル")
    parser.add_argument("--scale", type=int, default=4,
                        help="アップスケール倍率 (2 or 4)")
    parser.add_argument("--num-block", type=int, default=23,
                        help="RRDB ブロック数 (x4plus:23, anime:6)")
    parser.add_argument("--opset", type=int, default=17,
                        help="ONNX opset version (推奨: 17+)")
    parser.add_argument("--no-dynamic", dest="dynamic", action="store_false",
                        help="動的サイズを無効化")
    parser.set_defaults(dynamic=True)
    args = parser.parse_args()
    main(args)
