#!/usr/bin/env python3
"""compose_cards_20260820.py — 8/20 商品卡片合成"""
import sys
import json
import os

PYTHON_BIN = "/Users/xiaoan/.workbuddy/binaries/python/versions/3.13.12/bin/python3"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-08-20"
DATA_FILE = f"{OUT_DIR}/data.json"
CARD_W = 1080

# 5个商品主题色
THEMES = [
    # 1. 谷雨光感水 - 温柔粉金色
    {"bg": "#fdf6f0", "accent": "#d4a574", "text": "#5d3a1a", "tag_bg": "#b8860b", "title_size": 40, "tag_size": 19},
    # 2. 全棉时代洗脸巾 - 清新棉白
    {"bg": "#f5f5f0", "accent": "#66bb6a", "text": "#1b5e20", "tag_bg": "#2e7d32", "title_size": 40, "tag_size": 19},
    # 3. 小熊料理锅 - 活力橙
    {"bg": "#fff8f0", "accent": "#ff7043", "text": "#bf360c", "tag_bg": "#e64a19", "title_size": 40, "tag_size": 19},
    # 4. 茶花收纳箱 - 温馨暖黄
    {"bg": "#fffde7", "accent": "#ffb300", "text": "#5d4037", "tag_bg": "#f57f17", "title_size": 40, "tag_size": 19},
    # 5. 诺特兰德益生菌 - 清新蓝绿
    {"bg": "#e0f7fa", "accent": "#26a69a", "text": "#004d40", "tag_bg": "#00897b", "title_size": 40, "tag_size": 19},
]


def get_image_dimensions(img_path):
    try:
        from PIL import Image
        with Image.open(img_path) as im:
            return im.size
    except:
        return (1080, 1080)


def wrap_text(text, font, max_width, draw):
    """智能换行"""
    words = text.split('\n')
    lines = []
    for word_group in words:
        words_in = word_group.split(' ')
        current = ''
        for word in words_in:
            test = (current + ' ' + word).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def make_single_card(idx, product, img_path, theme, out_path):
    """生成单张商品详情卡片"""
    from PIL import Image, ImageDraw, ImageFont

    # 读取商品图
    if os.path.exists(img_path):
        orig_w, orig_h = get_image_dimensions(img_path)
        with Image.open(img_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            size = min(orig_w, orig_h)
            left = (orig_w - size) // 2
            top = (orig_h - size) // 2
            img = img.crop((left, top, left + size, top + size))
            img.thumbnail((880, 880), Image.LANCZOS)
            prod_w, prod_h = img.size
    else:
        prod_w, prod_h = 880, 880

    info_h = 400
    card_h = prod_h + info_h
    card = Image.new('RGB', (CARD_W, card_h), theme['bg'])
    draw = ImageDraw.Draw(card)

    # 顶部色带
    draw.rectangle([0, 0, CARD_W, 8], fill=theme['accent'])

    # 贴商品图（居中）
    if os.path.exists(img_path):
        card.paste(img, ((CARD_W - prod_w) // 2, 20))

    # 商品名
    title = product.get('title', '')[:40]
    try:
        title_font = ImageFont.truetype(FONT_PATH, 28)
    except:
        title_font = ImageFont.load_default()
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (CARD_W - title_w) // 2
    draw.text((title_x, prod_h + 15), title, fill=theme['accent'], font=title_font)

    # 价格
    price = product.get('price', '')
    price_font_size = 32
    try:
        price_font = ImageFont.truetype(FONT_PATH, price_font_size)
    except:
        price_font = ImageFont.load_default()
    draw.text((60, prod_h + 65), price, fill=theme['tag_bg'], font=price_font)

    # 描述
    desc = product.get('description', '')
    desc_font_size = 22
    try:
        desc_font = ImageFont.truetype(FONT_PATH, desc_font_size)
    except:
        desc_font = ImageFont.load_default()
    max_w = CARD_W - 120
    desc_lines = wrap_text(desc, desc_font, max_w, draw)
    y = prod_h + 120
    for line in desc_lines[:3]:
        if y > card_h - 40:
            break
        draw.text((60, y), line, fill=theme['text'], font=desc_font)
        y += desc_font_size + 8

    # 卖点标签
    tags = product.get('tags', [])[:5]
    tag_y = y + 15
    tag_x = 60
    tag_gap = 18
    for tag in tags:
        try:
            tag_font = ImageFont.truetype(FONT_PATH, 18)
        except:
            tag_font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), f" #{tag} ", font=tag_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tag_x + tw > CARD_W - 20:
            tag_x = 60
            tag_y += th + tag_gap
        draw.rounded_rectangle(
            [tag_x - 4, tag_y - 2, tag_x + tw + 4, tag_y + th + 2],
            radius=8,
            fill=theme['tag_bg']
        )
        draw.text((tag_x, tag_y), f"#{tag}", fill='white', font=tag_font)
        tag_x += tw + 24

    card.save(out_path, 'JPEG', quality=92)
    print(f"  [Card {idx}] 保存: {out_path}")


def compose_full_image(product_files, out_path):
    """将5张卡片合成为一张长图（5等份纵向拼接）"""
    from PIL import Image
    import math

    # 每张卡片高度约 880+400=1280
    card_heights = []
    cards = []
    for pf in product_files:
        try:
            with Image.open(pf) as im:
                cards.append(im.copy())
                card_heights.append(im.height)
        except Exception as e:
            print(f"    警告: 无法读取 {pf}: {e}")
            cards.append(None)

    if not cards or all(c is None for c in cards):
        print(f"  错误: 无可用卡片，生成终止")
        return

    total_h = sum(h for h, c in zip(card_heights, cards) if c)
    max_w = max(c.width for c in cards if c)

    full = Image.new('RGB', (max_w, total_h + 20), '#ffffff')
    y = 0
    for card, h in zip(cards, card_heights):
        if card:
            if card.width < max_w:
                new_card = Image.new('RGB', (max_w, h), '#ffffff')
                new_card.paste(card, ((max_w - card.width) // 2, 0))
                card = new_card
            full.paste(card, (0, y))
            y += h

    full.save(out_path, 'JPEG', quality=92)
    print(f"  [Full] 保存: {out_path} ({max_w}x{total_h})")


def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    products = data.get('products', [])

    # 生成5张独立卡片
    card_paths = []
    for i, product in enumerate(products):
        img_path = os.path.join(OUT_DIR, f"orig_product_{i+1}.jpg")
        out_card = os.path.join(OUT_DIR, f"product_{i+1}.jpg")
        theme = THEMES[i] if i < len(THEMES) else THEMES[-1]
        make_single_card(i+1, product, img_path, theme, out_card)
        card_paths.append(out_card)

    # 合成全图
    full_out = os.path.join(OUT_DIR, "product_card_full.jpg")
    compose_full_image(card_paths, full_out)

    # 裁剪5张 slice
    from PIL import Image
    try:
        with Image.open(full_out) as full:
            fw, fh = full.size
            slice_h = fh // 5
            for i in range(5):
                top = i * slice_h
                bottom = top + slice_h if i < 4 else fh
                crop = full.crop((0, top, fw, bottom))
                slice_out = os.path.join(OUT_DIR, f"product_slice_{i+1}.jpg")
                crop.save(slice_out, 'JPEG', quality=88)
                print(f"  [Slice {i+1}] 保存: {slice_out}")
    except Exception as e:
        print(f"  裁剪失败: {e}")

    print("\n全部完成!")


if __name__ == "__main__":
    main()
