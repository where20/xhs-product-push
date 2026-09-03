#!/usr/bin/env python3
"""生成 5 款商品详情长图(1080px 宽),每款商品一张 3000px 高卡片,5 等份裁剪
基于 compose_cards_20260903.py 模式,TODAY=2026-09-04
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont

# === 配置 ===
TODAY = "2026-09-04"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20
TOTAL_H = CARD_H * 5 + GAP * 4  # 5 张卡片 + 4 个间距

# === 加载数据 ===
with open(f"{OUT_DIR}/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
products = data["products"]

# === 字体 ===
try:
    font_title = ImageFont.truetype(FONT_PATH, 56)
    font_subtitle = ImageFont.truetype(FONT_PATH, 34)
    font_desc = ImageFont.truetype(FONT_PATH, 28)
    font_hl = ImageFont.truetype(FONT_PATH, 26)
    font_tag = ImageFont.truetype(FONT_PATH, 26)
    font_small = ImageFont.truetype(FONT_PATH, 24)
    font_num = ImageFont.truetype(FONT_PATH, 140)
    font_category = ImageFont.truetype(FONT_PATH, 36)
    font_price = ImageFont.truetype(FONT_PATH, 38)
except Exception as e:
    print(f"字体加载失败: {e}")
    sys.exit(1)


def hex_to_rgb(hexstr):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_wrapped_text(draw, text, x, y, max_width, font, fill, line_spacing=8):
    """自动换行绘制中文文本"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    cy = y
    for line in lines:
        draw.text((x, cy), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        cy += (bbox[3] - bbox[1]) + line_spacing
    return cy


def make_card(p, idx):
    """生成单张商品卡片"""
    img = Image.new("RGB", (WIDTH, CARD_H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    color = hex_to_rgb(p.get("color", "#1C3A5F"))
    y_cursor = 0

    # 顶部色条
    draw.rectangle([0, 0, WIDTH, 280], fill=color)
    # 编号
    draw.text((50, 50), p["num"], font=font_num, fill=(255, 255, 255))
    # 品类
    draw.text((50, 200), p["category"], font=font_category, fill=(255, 255, 255))
    # 价格右上角
    bbox = draw.textbbox((0, 0), p["price"], font=font_price)
    pw = bbox[2] - bbox[0]
    draw.text((WIDTH - pw - 50, 90), p["price"], font=font_price, fill=(255, 255, 255))
    y_cursor = 280

    # 商品图
    try:
        product_img = Image.open(f"{OUT_DIR}/images/product_{p['id']}.jpg").convert("RGB")
        product_img = product_img.resize((WIDTH - 100, WIDTH - 100), Image.LANCZOS)
        img.paste(product_img, (50, y_cursor + 30))
        y_cursor += (WIDTH - 100) + 60
    except Exception as e:
        print(f"⚠️ 加载图片 {p['id']} 失败: {e}")
        y_cursor += 100

    # 标题
    title = p["name"]
    y_cursor = draw_wrapped_text(draw, title, 50, y_cursor, WIDTH - 100, font_title, color, 12)
    y_cursor += 20

    # 副标题(用 desc 前 80 字)
    subtitle = p["desc"][:90] + "…"
    y_cursor = draw_wrapped_text(draw, subtitle, 50, y_cursor, WIDTH - 100, font_subtitle, (80, 80, 80), 8)
    y_cursor += 30

    # 分隔线
    draw.line([(50, y_cursor), (WIDTH - 50, y_cursor)], fill=color, width=3)
    y_cursor += 30

    # 5 个亮点
    draw.text((50, y_cursor), "5 大核心亮点", font=font_subtitle, fill=color)
    y_cursor += 70
    for i, hl in enumerate(p["highlights"]):
        # 编号小方块
        draw.rectangle([50, y_cursor, 100, y_cursor + 50], fill=color)
        draw.text((60, y_cursor + 5), str(i + 1), font=font_hl, fill=(255, 255, 255))
        y_cursor = draw_wrapped_text(draw, hl, 120, y_cursor + 5, WIDTH - 170, font_hl, (50, 50, 50), 6)
        y_cursor += 25
    y_cursor += 20

    # 完整描述
    draw.text((50, y_cursor), "商品详情", font=font_subtitle, fill=color)
    y_cursor += 70
    y_cursor = draw_wrapped_text(draw, p["desc"], 50, y_cursor, WIDTH - 100, font_desc, (50, 50, 50), 8)
    y_cursor += 25

    # 适用人群
    if y_cursor < CARD_H - 350:
        draw.text((50, y_cursor), "适合人群", font=font_subtitle, fill=color)
        y_cursor += 60
        y_cursor = draw_wrapped_text(draw, p["suitable"], 50, y_cursor, WIDTH - 100, font_small, (80, 80, 80), 6)
        y_cursor += 20

    # 标签 chips
    if y_cursor < CARD_H - 250:
        draw.text((50, y_cursor), "卖点标签", font=font_subtitle, fill=color)
        y_cursor += 60
        chip_x = 50
        chip_y = y_cursor
        for tag in p["tags"]:
            bbox = draw.textbbox((0, 0), tag, font=font_tag)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            cw = tw + 30
            ch = th + 16
            if chip_x + cw > WIDTH - 50:
                chip_x = 50
                chip_y += ch + 10
            draw.rounded_rectangle([chip_x, chip_y, chip_x + cw, chip_y + ch], radius=12, fill=color)
            draw.text((chip_x + 15, chip_y + 5), tag, font=font_tag, fill=(255, 255, 255))
            chip_x += cw + 10
        y_cursor = chip_y + ch + 30

    # 价格说明
    if y_cursor < CARD_H - 120:
        draw.rounded_rectangle([50, CARD_H - 150, WIDTH - 50, CARD_H - 60], radius=15, fill=color)
        price_text = f"💰 {p['price_note']}"
        bbox = draw.textbbox((0, 0), price_text, font=font_price)
        pw = bbox[2] - bbox[0]
        draw.text(((WIDTH - pw) // 2, CARD_H - 125), price_text, font=font_price, fill=(255, 255, 255))

    # 底部 logo
    draw.text((50, CARD_H - 40), f"xhs-product-push · {TODAY}", font=font_small, fill=(180, 180, 180))
    return img


# === 合成完整长图 ===
print(f"📐 总尺寸: {WIDTH} x {TOTAL_H}")
canvas = Image.new("RGB", (WIDTH, TOTAL_H), (245, 245, 245))
for i, p in enumerate(products):
    p["num"] = f"0{i+1}"
    print(f"🎨 生成第 {i+1} 张: {p['name']}")
    card = make_card(p, i)
    y_offset = i * (CARD_H + GAP)
    canvas.paste(card, (0, y_offset))

# 保存全图
full_path = f"{OUT_DIR}/product_card_full.jpg"
canvas.save(full_path, quality=92)
print(f"✅ 全图已保存: {full_path} ({os.path.getsize(full_path) // 1024} KB)")

# 5 等份裁剪
for i in range(5):
    top = i * (CARD_H + GAP)
    bottom = top + CARD_H
    slice_img = canvas.crop((0, top, WIDTH, bottom))
    slice_path = f"{OUT_DIR}/product_slice_{i+1}.jpg"
    slice_img.save(slice_path, quality=92)
    print(f"✂️ 切片 {i+1} 已保存: {slice_path} ({os.path.getsize(slice_path) // 1024} KB)")

print("✅ 全部完成")
