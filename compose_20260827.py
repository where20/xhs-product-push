#!/usr/bin/env python3
"""合成 2026-08-27 商品详情长图 (1080px宽, 5等份裁剪)"""
import json, os
from PIL import Image, ImageDraw, ImageFont

TODAY = "2026-08-27"
WS_DIR = "/Users/xiaoan/.minimax/sessions/mvs_d7b4e76ce61d449d81ef32e4659d16a1/workspace"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
IMG_W = 1080
CARD_H = 1200   # 每张卡高度
PAD = 24
RADIUS = 28
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"

os.makedirs(OUT_DIR, exist_ok=True)

# 加载 data.json
with open(f"{OUT_DIR}/data.json") as f:
    data = json.load(f)

# 加载商品图
imgs = {}
for pid in range(1, 6):
    src = f"{WS_DIR}/product_{pid}_001.jpg"
    if os.path.exists(src):
        imgs[pid] = Image.open(src).convert("RGB")
        print(f"  Loaded product_{pid}: {imgs[pid].size}")
    else:
        print(f"  MISSING: {src}")

def round_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def paste_rounded(img, src_img, box, radius):
    """把 src_img 贴到 img 的 box 位置，保留圆角遮罩"""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # 缩放 src_img 到目标尺寸
    resized = src_img.resize((w, h), Image.LANCZOS)
    # 创建遮罩
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
    img.paste(resized, (x0, y0), mask)

def make_card(product, bg_img, pid):
    card = Image.new("RGB", (IMG_W, CARD_H), (255, 255, 255))
    draw = ImageDraw.Draw(card)
    cx = IMG_W // 2

    # 商品图区域 (顶部)
    img_h = 540
    if bg_img:
        paste_rounded(card, bg_img, (PAD, PAD, IMG_W - PAD, PAD + img_h), RADIUS)
    else:
        draw.rounded_rectangle((PAD, PAD, IMG_W - PAD, PAD + img_h), RADIUS, fill=(230, 235, 245))

    # === 标题区 ===
    title_y = PAD + img_h + 20
    draw.rounded_rectangle((PAD, title_y, IMG_W - PAD, title_y + 110), 18, fill=(245, 247, 252))

    # 商品名
    fnt_title = ImageFont.truetype(FONT_PATH, 38)
    name = product["name"]
    draw.text((PAD + 20, title_y + 10), name, font=fnt_title, fill=(30, 35, 50))

    # 价格
    price_text = product["price_range"]
    fnt_price = ImageFont.truetype(FONT_PATH, 32)
    draw.text((IMG_W - PAD - 20, title_y + 14), price_text, font=fnt_price, fill=(220, 45, 60), anchor="rt")

    # 卖点标签
    tags = product.get("tags", [])[:5]
    tag_y = title_y + 62
    x = PAD + 20
    fnt_tag = ImageFont.truetype(FONT_PATH, 22)
    for tag in tags:
        tw = draw.textlength(tag, font=fnt_tag) + 20
        if x + tw > IMG_W - PAD - 20:
            break
        draw.rounded_rectangle((x, tag_y, x + tw, tag_y + 40), 20, fill=(220, 100, 90))
        draw.text((x + 10, tag_y + 7), tag, font=fnt_tag, fill=(255, 255, 255))
        x += tw + 12

    # === 正文区 ===
    body_y = title_y + 130
    body_h = CARD_H - body_y - PAD - 10

    # 正文背景
    draw.rounded_rectangle((PAD, body_y, IMG_W - PAD, CARD_H - PAD), 18, fill=(248, 250, 255))

    # 小标题
    fnt_sub = ImageFont.truetype(FONT_PATH, 26)
    draw.text((PAD + 20, body_y + 14), "📝  商品详情", font=fnt_sub, fill=(50, 60, 90))

    # 描述
    fnt_desc = ImageFont.truetype(FONT_PATH, 26)
    desc_lines = wrap_text(product["description"], fnt_desc, IMG_W - PAD * 4 - 40, draw)
    ty = body_y + 52
    for line in desc_lines:
        draw.text((PAD + 20, ty), line, font=fnt_desc, fill=(80, 90, 110))
        ty += 38

    # 亮点
    fnt_hl = ImageFont.truetype(FONT_PATH, 24)
    ty += 10
    draw.text((PAD + 20, ty), "✨  核心亮点", font=fnt_sub, fill=(50, 60, 90))
    ty += 38
    for hl in product["highlights"]:
        bullet = "• "
        line_text = bullet + hl
        lines = wrap_text(line_text, fnt_hl, IMG_W - PAD * 4 - 20, draw)
        for ln in lines:
            draw.text((PAD + 20, ty), ln, font=fnt_hl, fill=(90, 100, 130))
            ty += 34
        ty += 4

    return card

def wrap_text(text, font, max_w, draw, max_lines=6):
    """简单按字符 wrap，返回行列表"""
    lines = []
    for para in text.split("\n"):
        words = para
        cur = ""
        for ch in words:
            test = cur + ch
            if draw.textlength(test, font=font) > max_w:
                if cur:
                    lines.append(cur)
                    cur = ch
                else:
                    lines.append(ch)
            else:
                cur = test
        if cur:
            lines.append(cur)
    return lines[:max_lines]

# 合成总图
total_h = CARD_H * 5
full_img = Image.new("RGB", (IMG_W, total_h), (220, 225, 235))
for i, product in enumerate(data["products"]):
    pid = product["id"]
    card = make_card(product, imgs.get(pid), pid)
    full_img.paste(card, (0, i * CARD_H))
    print(f"  Card {pid} pasted at y={i*CARD_H}")

# 保存全图
full_path = f"{OUT_DIR}/product_card_full.jpg"
full_img.save(full_path, "JPEG", quality=92)
print(f"\nFull card saved: {full_path} ({full_img.size})")

# 裁剪5张
for i in range(5):
    y = i * CARD_H
    crop = full_img.crop((0, y, IMG_W, y + CARD_H))
    out = f"{OUT_DIR}/product_{i+1}_card.jpg"
    crop.save(out, "JPEG", quality=92)
    print(f"  Crop {i+1}: {out}")

print("\nDone!")
