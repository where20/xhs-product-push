#!/usr/bin/env python3
"""合成商品详情长图并裁剪"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

# 路径配置
OUTPUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-08-16"
FONT_CN = "/System/Library/Fonts/STHeiti Light.ttc"
IMG_WIDTH = 1080
CARD_HEIGHT = 540  # 每张卡片高度

def load_data():
    with open(f"{OUTPUT_DIR}/data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def create_tag_pill(draw, x, y, text, color):
    """创建标签药丸形状"""
    w, h = 100, 32
    r = 16
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=color)
    # 文字居中
    try:
        font = ImageFont.truetype(FONT_CN, 16)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_x = x + (w - text_w) // 2
    text_y = y + 6
    draw.text((text_x, text_y), text, fill="white", font=font)

def draw_product_card(canvas, product_img_path, product, y_offset, bg_color):
    """绘制单个商品卡片"""
    card = Image.new("RGB", (IMG_WIDTH, CARD_HEIGHT), bg_color)
    draw = ImageDraw.Draw(card)

    # 加载并粘贴商品图 (居中左侧)
    try:
        img = Image.open(product_img_path).convert("RGB")
        img.thumbnail((400, 400), Image.LANCZOS)
        img_w, img_h = img.size
        paste_x = 30 + (400 - img_w) // 2
        paste_y = (CARD_HEIGHT - img_h) // 2
        card.paste(img, (paste_x, paste_y))
    except Exception as e:
        print(f"加载图片失败: {e}")

    # 右侧文字区域
    text_x = 460

    # 商品名称
    try:
        name_font = ImageFont.truetype(FONT_CN, 28)
    except:
        name_font = ImageFont.load_default()
    draw.text((text_x, 30), product["name"], fill="white", font=name_font)

    # 描述文字
    try:
        desc_font = ImageFont.truetype(FONT_CN, 18)
    except:
        desc_font = ImageFont.load_default()

    # 描述分段
    desc = product["description"]
    lines = []
    words = desc
    max_chars = 28
    while len(words) > max_chars:
        lines.append(words[:max_chars])
        words = words[max_chars:]
    lines.append(words)

    y = 80
    for line in lines[:3]:
        draw.text((text_x, y), line, fill="#E0E0E0", font=desc_font)
        y += 28

    # 亮点
    y = 180
    try:
        hl_font = ImageFont.truetype(FONT_CN, 15)
    except:
        hl_font = ImageFont.load_default()

    for i, hl in enumerate(product["highlights"][:3]):
        bullet = f"• {hl}"
        draw.text((text_x, y), bullet, fill="#FFD700", font=hl_font)
        y += 25

    # 标签
    y = 290
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
    x = text_x
    for i, tag in enumerate(product["tags"][:3]):
        w, h = 100, 28
        r = 14
        draw.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=colors[i % len(colors)])
        try:
            tag_font = ImageFont.truetype(FONT_CN, 14)
        except:
            tag_font = ImageFont.load_default()
        draw.text((x + 10, y + 5), tag, fill="white", font=tag_font)
        x += 110

    # 适合人群
    y = 330
    try:
        sf_font = ImageFont.truetype(FONT_CN, 14)
    except:
        sf_font = ImageFont.load_default()
    draw.text((text_x, y), f"适合: {product['suitableFor']}", fill="#AAAAAA", font=sf_font)

    # 粘贴到画布
    canvas.paste(card, (0, y_offset))

def main():
    data = load_data()
    products = data["products"]

    # 创建总画布 (5张卡片 + 头部)
    HEADER_HEIGHT = 120
    total_height = HEADER_HEIGHT + len(products) * CARD_HEIGHT

    # 渐变背景
    canvas = Image.new("RGB", (IMG_WIDTH, total_height), "#1A1A2E")
    draw = ImageDraw.Draw(canvas)

    # 绘制头部
    try:
        header_font = ImageFont.truetype(FONT_CN, 42)
        sub_font = ImageFont.truetype(FONT_CN, 22)
    except:
        header_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    draw.text((40, 25), "🔥 今日好物推荐", fill="white", font=header_font)
    draw.text((40, 75), "小红书爆款清单 · 2026年8月热门商品", fill="#FF6B6B", font=sub_font)

    # 绘制分割线
    draw.rectangle([(0, HEADER_HEIGHT-5), (IMG_WIDTH, HEADER_HEIGHT-3)], fill="#FF6B6B")

    # 绘制商品卡片
    colors = ["#16213E", "#1A1A2E", "#16213E", "#1A1A2E", "#16213E"]
    for i, product in enumerate(products):
        img_path = f"{OUTPUT_DIR}/orig_product_{product['id']}.jpg"
        y_offset = HEADER_HEIGHT + i * CARD_HEIGHT
        draw_product_card(canvas, img_path, product, y_offset, colors[i])

    # 保存全图
    full_path = f"{OUTPUT_DIR}/product_card_full.jpg"
    canvas.save(full_path, "JPEG", quality=95)
    print(f"✅ 全图已保存: {full_path}")

    # 裁剪成5等份
    for i in range(5):
        y_start = HEADER_HEIGHT + i * CARD_HEIGHT
        cropped = canvas.crop((0, y_start, IMG_WIDTH, y_start + CARD_HEIGHT))
        crop_path = f"{OUTPUT_DIR}/product_{i+1}.jpg"
        cropped.save(crop_path, "JPEG", quality=90)
        print(f"✅ 裁剪 {i+1}/5: {crop_path}")

if __name__ == "__main__":
    main()
