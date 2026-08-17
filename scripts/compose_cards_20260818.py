#!/usr/bin/env python3
"""compose_cards_20260818.py — 8/18 商品卡片合成"""
import sys
import json
import os

FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-08-18"
DATA_FILE = f"{OUT_DIR}/data.json"
CARD_W = 1080

# 主题色：每个商品独立配色
THEMES = [
    # 1. 洗衣机 - 清爽蓝白
    {"bg": "#f0f4f8", "accent": "#2196F3", "text": "#1a237e", "tag_bg": "#1565C0", "title_size": 40, "tag_size": 19},
    # 2. 微烤一体机 - 温暖橙色系
    {"bg": "#fff8f0", "accent": "#ff7043", "text": "#bf360c", "tag_bg": "#e64a19", "title_size": 40, "tag_size": 19},
    # 3. TWS耳机 - 科技深黑
    {"bg": "#1a1a2e", "accent": "#e040fb", "text": "#ffffff", "tag_bg": "#7b1fa2", "title_size": 40, "tag_size": 19},
    # 4. 4K投影 - 影院深蓝
    {"bg": "#0d1b2a", "accent": "#00b4d8", "text": "#caf0f8", "tag_bg": "#0077b6", "title_size": 40, "tag_size": 19},
    # 5. 扫地机器人 - 科技灰绿
    {"bg": "#1b2e1b", "accent": "#4caf50", "text": "#e8f5e9", "tag_bg": "#2e7d32", "title_size": 40, "tag_size": 19},
]


def get_image_dimensions(img_path):
    """获取图片宽高"""
    try:
        from PIL import Image
        with Image.open(img_path) as im:
            return im.size
    except:
        return (1080, 1080)


def make_card(idx, product, img_path, theme, out_path):
    """生成单张商品卡片"""
    from PIL import Image, ImageDraw, ImageFont
    import textwrap

    # 读取商品图
    if os.path.exists(img_path):
        orig_w, orig_h = get_image_dimensions(img_path)
        with Image.open(img_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # 中心裁剪正方形
            size = min(orig_w, orig_h)
            left = (orig_w - size) // 2
            top = (orig_h - size) // 2
            img = img.crop((left, top, left + size, top + size))
            img.thumbnail((880, 880), Image.LANCZOS)
            prod_w, prod_h = img.size
    else:
        prod_w, prod_h = 880, 880

    # 信息区域高度
    info_h = 360
    card_h = prod_h + info_h
    card = Image.new('RGB', (CARD_W, card_h), theme['bg'])
    draw = ImageDraw.Draw(card)

    # 贴商品图（居中）
    if os.path.exists(img_path):
        card.paste(img, ((CARD_W - prod_w) // 2, 20))

    # 顶部色带
    draw.rectangle([0, 0, CARD_W, 8], fill=theme['accent'])

    # 商品名
    name = product.get('name', '')
    try:
        name_font = ImageFont.truetype(FONT_PATH, 26)
    except:
        name_font = ImageFont.load_default()
    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_w = name_bbox[2] - name_bbox[0]
    name_x = (CARD_W - name_w) // 2
    draw.text((name_x, prod_h + 15), name, fill=theme['accent'], font=name_font)

    # 标题（大字）
    title = product.get('title', '')
    try:
        title_font = ImageFont.truetype(FONT_PATH, theme['title_size'])
    except:
        title_font = ImageFont.load_default()
    lines = textwrap.wrap(title, width=18)
    y = prod_h + 52
    for line in lines[:2]:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        tw = bbox[2] - bbox[0]
        draw.text(((CARD_W - tw) // 2, y), line, fill=theme['text'], font=title_font)
        y += theme['title_size'] + 6

    # 描述（3行）
    desc = product.get('description', '')[:110] + '…'
    try:
        desc_font = ImageFont.truetype(FONT_PATH, 21)
    except:
        desc_font = ImageFont.load_default()
    y += 5
    desc_lines = textwrap.wrap(desc, width=22)
    for line in desc_lines[:3]:
        draw.text((40, y), line, fill=theme['text'], font=desc_font)
        y += 30

    # 亮点标签
    highlights = product.get('highlights', [])[:3]
    try:
        tag_font = ImageFont.truetype(FONT_PATH, theme['tag_size'])
    except:
        tag_font = ImageFont.load_default()

    x_offset = 40
    tag_y = y + 5
    for hl in highlights:
        tag_text = '• ' + hl[:20]
        bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        pad_x, pad_y = 8, 4
        draw.rounded_rectangle(
            [x_offset - pad_x, tag_y - pad_y, x_offset + tw + pad_x, tag_y + th + pad_y],
            radius=6, fill=theme['tag_bg'])
        draw.text((x_offset, tag_y), tag_text, fill='#ffffff', font=tag_font)
        x_offset += tw + pad_x * 2 + 10
        if x_offset > CARD_W - 120:
            x_offset = 40
            tag_y += th + pad_y * 2 + 6

    card.save(out_path, 'JPEG', quality=92)
    print(f"  ✅ product_{idx}.jpg → {os.path.basename(out_path)} ({CARD_W}x{card_h})")


def main():
    from PIL import Image
    with open(DATA_FILE, encoding='utf-8') as f:
        data = json.load(f)

    products = data['products']

    # 生成单张卡片
    for i, product in enumerate(products):
        idx = i + 1
        theme = THEMES[i % len(THEMES)]
        img_path = f"{OUT_DIR}/orig_product_{idx}.jpg"
        out_path = f"{OUT_DIR}/product_{idx}.jpg"
        make_card(idx, product, img_path, theme, out_path)

    # 合成全图（垂直拼接5张）
    card_imgs = []
    for i in range(1, 6):
        path = f"{OUT_DIR}/product_{i}.jpg"
        if os.path.exists(path):
            with Image.open(path) as im:
                card_imgs.append(im.copy())

    if card_imgs:
        total_h = sum(img.height for img in card_imgs)
        max_w = max(img.width for img in card_imgs)
        from PIL import Image as PILImage
        full = PILImage.new('RGB', (max_w, total_h), '#111111')
        y = 0
        for img in card_imgs:
            full.paste(img, (0, y))
            y += img.height
        full_path = f"{OUT_DIR}/product_card_full.jpg"
        full.save(full_path, 'JPEG', quality=90)
        print(f"✅ product_card_full.jpg 合成完成 ({max_w}x{total_h})")

    print(f"\n🎉 全部完成！")


if __name__ == '__main__':
    main()
