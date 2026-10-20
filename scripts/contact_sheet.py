#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contact_sheet.py — 出图核对拼图

用途
----
2026-10-18 踩坑: 选品中途换了 SKU 但出图 prompt 没同步 → 卡片写"梨"、配图是"山药",
图文不符直接推到飞书群。10-19、10-20 两次都靠肉眼核对 contact sheet 挡住。

把当时手写的拼图逻辑固化成一个脚本, 让"核对"成为出图后的固定动作, 而不是
"想起来才做"。

用法:
    python3 scripts/contact_sheet.py [YYYY-MM-DD]
    # 输出: output/{date}/_contact_sheet.jpg
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import out_dir, read_json, resolve_date  # noqa: E402

TH = 340
GAP = 14
COLS = 3
LABELS_FALLBACK = "1  2  3  4  5"


def main():
    date = resolve_date()
    od = out_dir(date)
    img_dir = os.path.join(od, "images")

    if not os.path.isdir(img_dir):
        print(f"❌ 找不到 {img_dir}", file=sys.stderr)
        sys.exit(2)

    # 有 data.json 就用商品名做标签, 否则退回序号
    labels = []
    dpath = os.path.join(od, "data.json")
    if os.path.exists(dpath):
        try:
            prods = read_json(dpath)["products"]
            labels = [
                f"{i}. {p.get('name','')[:26]}" for i, p in enumerate(prods, 1)
            ]
        except Exception:
            labels = []
    while len(labels) < 5:
        labels.append(LABELS_FALLBACK.split("  ")[len(labels)])

    files = sorted(
        f for f in os.listdir(img_dir)
        if f.startswith("product_") and f.endswith(".jpg")
    )
    if not files:
        print(f"❌ {img_dir} 下没有 product_*.jpg", file=sys.stderr)
        sys.exit(2)

    n = len(files)
    rows = (n + COLS - 1) // COLS
    W = COLS * TH + (COLS + 1) * GAP
    H = rows * (TH + 44) + (rows + 1) * GAP
    sheet = Image.new("RGB", (W, H), (250, 250, 250))
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", 17)
    except Exception:
        font = ImageFont.load_default()

    for i, fn in enumerate(files):
        im = Image.open(os.path.join(img_dir, fn)).convert("RGB")
        w, h = im.size
        s = TH / min(w, h)
        im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
        c, r = i % COLS, i // COLS
        x = GAP + c * (TH + GAP)
        y = GAP + r * (TH + 44 + GAP)
        sheet.paste(im, (x + (TH - im.width) // 2, y))
        dr.rectangle([x - 1, y - 1, x + TH, y + TH], outline=(200, 200, 200))
        lbl = labels[i] if i < len(labels) else fn
        dr.text((x, y + TH + 10), lbl, fill=(20, 20, 20), font=font)

    out = os.path.join(od, "_contact_sheet.jpg")
    sheet.save(out, quality=90)
    print(f"✅ contact sheet → {out} ({sheet.size[0]}×{sheet.size[1]})")
    print("   ⚠️ 请肉眼核对: 每张图是否与标签上的商品名一致(10-18 踩坑 #2)")


if __name__ == "__main__":
    main()
