#!/usr/bin/env python3
"""compose_cards_20260817b.py — 8/17 第二批 5 商品卡片合成"""
import sys
import json
import os

# 配置
PYTHON_SYS = "/usr/bin/python3"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-08-17"
DATA_FILE = f"{OUT_DIR}/data.json"
CARD_W = 1080

# 主题色：每个商品独立配色
THEMES = [
    # 1. 掌机 - 赛博朋克蓝紫
    {"bg": "#0a0a1a", "accent": "#6C63FF", "text": "#ffffff", "tag_bg": "#6C63FF", "title_size": 42, "tag_size": 20},
    # 2. 投影仪 - 温暖白咖
    {"bg": "#faf7f2", "accent": "#e67e22", "text": "#2c2c2c", "tag_bg": "#e67e22", "title_size": 42, "tag_size": 20},
    # 3. SSD - 科技银蓝
    {"bg": "#0d1117", "accent": "#58a6ff", "text": "#c9d1d9", "tag_bg": "#21262d", "title_size": 42, "tag_size": 20},
    # 4. 智能手表 - 商务墨绿金
    {"bg": "#0f1f15", "accent": "#2ecc71", "text": "#e8f5e9", "tag_bg": "#27ae60", "title_size": 42, "tag_size": 20},
    # 5. 折叠屏 - 轻奢深紫
    {"bg": "#1a0a2e", "accent": "#bb86fc", "text": "#f3e5f5", "tag_bg": "#7b1fa2", "title_size": 42, "tag_size": 20},
]

def get_image_dimensions(img_path):
    """获取图片宽高"""
    import struct, io
    with open(img_path, 'rb') as f:
        data = f.read(12)
    # JPEG: SOI + APP1 length
    if data[0:2] == b'\xff\xd8':
        # JPEG - use PIL
        try:
            from PIL import Image
            with Image.open(img_path) as im:
                return im.size
        except:
            pass
    # PNG
    if data[0:8] == b'\x89PNG\r\n\x1a\n':
        import struct
        with open(img_path, 'rb') as f:
            f.read(8)
            chunk = f.read(4)
            if chunk == b'IHDR':
                data = f.read(13)
                w = struct.unpack('>I', data[0:4])[0]
                h = struct.unpack('>I', data[4:8])[0]
                return (w, h)
    return (1080, 1080)  # fallback


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
            # 裁剪为正方形（中心裁剪）
            size = min(orig_w, orig_h)
            left = (orig_w - size) // 2
            top = (orig_h - size) // 2
            img = img.crop((left, top, left + size, top + size))
            # 缩放到合适大小（卡片内展示）
            img.thumbnail((900, 900), Image.LANCZOS)
            prod_w, prod_h = img.size
    else:
        prod_w, prod_h = 900, 900

    # 卡片尺寸：图片区域 + 信息区域
    info_h = 380
    card_h = prod_h + info_h
    card = Image.new('RGB', (CARD_W, card_h), theme['bg'])
    draw = ImageDraw.Draw(card)

    # 贴商品图（居中）
    if os.path.exists(img_path):
        card.paste(img, ((CARD_W - prod_w) // 2, 20))

    # 分割线
    draw.line([(40, prod_h + 25), (CARD_W - 40, prod_h + 25)],
              fill=theme['accent'], width=2)

    y = prod_h + 40

    # 商品名称
    try:
        name_font = ImageFont.truetype(FONT_PATH, theme['title_size'])
    except:
        name_font = ImageFont.load_default()
    name_text = product['name']
    # 截断超长名称
    while True:
        bbox = draw.textbbox((0, 0), name_text, font=name_font)
        if bbox[2] > CARD_W - 80:
            name_text = name_text[:-2] + '…'
        else:
            break
    draw.text((50, y), name_text, fill=theme['text'], font=name_font)
    y += theme['title_size'] + 10

    # 价格
    price_text = product.get('priceRange', '')
    if price_text:
        try:
            price_font = ImageFont.truetype(FONT_PATH, 28)
        except:
            price_font = ImageFont.load_default()
        draw.text((50, y), price_text, fill=theme['accent'], font=price_font)
        y += 38

    # 描述
    try:
        desc_font = ImageFont.truetype(FONT_PATH, 22)
    except:
        desc_font = ImageFont.load_default()
    desc = product.get('description', '')[:90] + '…'
    lines = textwrap.wrap(desc, width=22)
    for line in lines[:3]:
        draw.text((50, y), line, fill=theme['text'], font=desc_font)
        y += 30
    y += 5

    # 亮点
    highlights = product.get('highlights', [])[:3]
    try:
        tag_font = ImageFont.truetype(FONT_PATH, theme['tag_size'])
    except:
        tag_font = ImageFont.load_default()

    x_offset = 50
    tag_y = y + 5
    max_y = tag_y

    for hl in highlights:
        tag_text = '• ' + hl[:18]
        bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        # 圆角矩形背景
        pad_x, pad_y = 10, 5
        draw.rounded_rectangle(
            [x_offset - pad_x, tag_y - pad_y, x_offset + tw + pad_x, tag_y + th + pad_y],
            radius=8, fill=theme['tag_bg'])
        draw.text((x_offset, tag_y), tag_text, fill='#ffffff', font=tag_font)
        x_offset += tw + pad_x * 2 + 12
        if x_offset > CARD_W - 100:
            x_offset = 50
            tag_y += th + pad_y * 2 + 8
        max_y = max(max_y, tag_y + th + pad_y)

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
