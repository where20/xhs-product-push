#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compose_cards_20260919.py
PIL 合成: 5 张商品图 + 详情文字 → 1080px 宽商品详情长图
然后 5 等份裁剪 + 1 张全图, 供 upload_cloudimgs.py 上传
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = Path('/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-19')
IMG_DIR = OUT_DIR / 'images'
IMG_DIR.mkdir(parents=True, exist_ok=True)

WIDTH = 1080
FONT_REG = '/System/Library/Fonts/STHeiti Medium.ttc'
FONT_BOLD = '/System/Library/Fonts/STHeiti Medium.ttc'

# 颜色
COLOR_BG = (255, 252, 247)
COLOR_TEXT = (50, 38, 28)
COLOR_ACCENT = (220, 88, 42)  # 中秋礼橙
COLOR_TAG = (245, 237, 227)
COLOR_TAG_TEXT = (153, 87, 47)
COLOR_PRICE = (220, 38, 42)
COLOR_BORDER = (240, 230, 218)

# 卡片尺寸
CARD_H = 1620  # 每张卡片纵向 1620px (1080×1620 → 1:1.5)


def font(size):
    return ImageFont.truetype(FONT_REG, size)


def font_bold(size):
    return ImageFont.truetype(FONT_BOLD, size)


def truncate(draw, text, font_obj, max_width):
    """文本超过宽度则用 ... 截断"""
    if draw.textlength(text, font=font_obj) <= max_width:
        return text
    while len(text) > 0 and draw.textlength(text + "...", font=font_obj) > max_width:
        text = text[:-1]
    return text + "..."


def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """在 PIL 1.x 上模拟圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def render_card(idx, p):
    """渲染单个商品卡片, 返回 1080 × CARD_H image"""
    img = Image.new('RGB', (WIDTH, CARD_H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # 顶部装饰条
    draw.rectangle([0, 0, WIDTH, 80], fill=COLOR_ACCENT)
    draw.text((48, 24), f"今日精选 · {idx:02d} / 05", font=font_bold(34), fill=(255, 255, 255))

    # 商品图 (顶部 1080×720)
    img_path = IMG_DIR / f'product_{idx}.jpg'
    if img_path.exists():
        prod = Image.open(img_path).convert('RGB')
        # 缩放到 1080×800 (留 80px 间隔)
        prod = prod.resize((WIDTH, 800), Image.LANCZOS)
        img.paste(prod, (0, 80))
    else:
        # 占位渐变
        for y in range(80, 880):
            ratio = (y - 80) / 800
            c = int(245 - ratio * 10)
            draw.rectangle([0, y, WIDTH, y + 1], fill=(c, c, c))

    # 内容区背景 (从 880 起)
    content_y = 880
    draw.rectangle([0, content_y, WIDTH, CARD_H], fill=COLOR_BG)

    # 分类标签 (左)
    draw.rounded_rectangle([48, content_y + 36, 48 + 220, content_y + 86], radius=24, fill=COLOR_TAG)
    draw.text((68, content_y + 44), truncate(draw, p['category'], font_bold(26), 200), font=font_bold(26), fill=COLOR_TAG_TEXT)

    # 编号 (右)
    draw.text((WIDTH - 200, content_y + 38), f"NO.{idx:02d}", font=font_bold(46), fill=COLOR_ACCENT)

    # 商品名称 (大字)
    name = truncate(draw, p['name'], font_bold(40), WIDTH - 96)
    draw.text((48, content_y + 110), name, font=font_bold(40), fill=COLOR_TEXT)

    # 价格 + 价格说明
    draw.text((48, content_y + 175), p['price'], font=font_bold(38), fill=COLOR_PRICE)
    if p.get('price_note'):
        pn = truncate(draw, p['price_note'], font(20), WIDTH - 96)
        draw.text((48, content_y + 222), pn, font=font(20), fill=(120, 100, 88))

    # 分隔线
    draw.line([48, content_y + 270, WIDTH - 48, content_y + 270], fill=COLOR_BORDER, width=2)

    # 5 大卖点
    draw.text((48, content_y + 290), "✦ 5 大亮点", font=font_bold(28), fill=COLOR_ACCENT)
    for i, h in enumerate(p.get('highlights', [])[:5], 1):
        text = truncate(draw, f"{i}. {h}", font(22), WIDTH - 96)
        draw.text((56, content_y + 332 + (i - 1) * 48), text, font=font(22), fill=COLOR_TEXT)

    # 适合人群 + 颜色
    bot_y = content_y + 332 + 5 * 48 + 12
    draw.text((48, bot_y), f"🎯 适合: {p.get('suitable', '')}", font=font(20), fill=(80, 65, 50))
    bot_y += 30
    draw.text((48, bot_y), f"🎨 颜色: {p.get('color', '')}", font=font(20), fill=(80, 65, 50))

    # 标签 (底部一行)
    tag_y = CARD_H - 80
    tags = p.get('tags', [])[:6]
    x = 48
    for tag in tags:
        tag_text = tag.replace('#', '')
        tw = int(draw.textlength(tag_text, font=font(18))) + 30
        if x + tw > WIDTH - 48:
            break
        draw.rounded_rectangle([x, tag_y, x + tw, tag_y + 38], radius=19, fill=COLOR_TAG)
        draw.text((x + 15, tag_y + 8), tag_text, font=font(18), fill=COLOR_TAG_TEXT)
        x += tw + 10

    # 底部装饰
    draw.rectangle([0, CARD_H - 24, WIDTH, CARD_H], fill=COLOR_ACCENT)

    return img


def main():
    with open(OUT_DIR / 'data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    products = data['products']
    total_h = len(products) * CARD_H + 100  # 顶部 100px header
    full = Image.new('RGB', (WIDTH, total_h), COLOR_BG)
    full_draw = ImageDraw.Draw(full)

    # 顶部 header
    full_draw.rectangle([0, 0, WIDTH, 100], fill=COLOR_ACCENT)
    full_draw.text((48, 28), f"小红书精选 · {data['date']}", font=font_bold(34), fill=(255, 255, 255))
    full_draw.text((48, 65), data['title'], font=font(20), fill=(255, 240, 230))

    # 拼接 5 张卡片
    for idx, p in enumerate(products, 1):
        card = render_card(idx, p)
        full.paste(card, (0, 100 + (idx - 1) * CARD_H))
        print(f"  ✅ 卡片 {idx:02d}: {p['name']}")

    # 保存全图
    full_path = OUT_DIR / 'products_full.jpg'
    full.save(full_path, 'JPEG', quality=88)
    print(f"✅ 全图: {full_path} ({(full_path.stat().st_size / 1024):.0f}KB, {WIDTH}×{total_h})")

    # 5 等份裁剪 (从拼接图中裁出单卡)
    for idx in range(1, len(products) + 1):
        y = 100 + (idx - 1) * CARD_H
        crop = full.crop((0, y, WIDTH, y + CARD_H))
        slice_path = OUT_DIR / f'product_slice_{idx:02d}.jpg'
        crop.save(slice_path, 'JPEG', quality=92)
        print(f"  ✅ 切片 {idx:02d}: {slice_path} ({(slice_path.stat().st_size / 1024):.0f}KB, {WIDTH}×{CARD_H})")


if __name__ == '__main__':
    main()
