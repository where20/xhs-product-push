#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 5 款商品详情长图（1080px 宽），每款商品一张 3000px 高卡片，5 等份裁剪

通用版 (2026-10-21 起替代 compose_cards_YYYYMMDD.py 共 35 份)
  用法: python3 scripts/compose_cards.py [YYYY-MM-DD]
        # 默认今天; 也可用 XHS_DATE=2026-10-21
  输入: output/{date}/data.json
  输出: output/{date}/product_card_full.jpg + product_slice_1..5.jpg
"""
import os, sys, json
from PIL import Image, ImageDraw, ImageFont

# === 配置 ===
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import (  # noqa: E402
    DEFAULT_THEME_RGB,
    out_dir,
    resolve_date,
    safe_hex_to_rgb,
    theme_color_for,
)

TODAY = resolve_date()
OUT_DIR = out_dir(TODAY)
FONT_PATH = os.environ.get("FONT_CN") or "/System/Library/Fonts/STHeiti Light.ttc"
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
    font_title = ImageFont.truetype(FONT_PATH, 60)
    font_subtitle = ImageFont.truetype(FONT_PATH, 36)
    font_desc = ImageFont.truetype(FONT_PATH, 30)
    font_hl = ImageFont.truetype(FONT_PATH, 28)
    font_tag = ImageFont.truetype(FONT_PATH, 28)
    font_small = ImageFont.truetype(FONT_PATH, 26)
    font_num = ImageFont.truetype(FONT_PATH, 140)
    font_category = ImageFont.truetype(FONT_PATH, 38)
    font_price = ImageFont.truetype(FONT_PATH, 40)
except Exception as e:
    print(f"字体加载失败: {e}")
    sys.exit(1)


def draw_wrapped_text(draw, text, x, y, max_width, font, fill, line_spacing=8, max_lines=None):
    """自动换行绘制中文文本；max_lines 超出时截断并加省略号"""
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
    truncated = False
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        truncated = True
    cy = y
    for line in lines:
        draw.text((x, cy), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        cy += (bbox[3] - bbox[1]) + line_spacing
    if truncated and lines:
        # 省略号紧跟末行, 但不许越过右边界(max_width - 省略号宽度)
        eb = draw.textbbox((0, 0), "…", font=font)
        ell_w = eb[2] - eb[0]
        bb = draw.textbbox((0, 0), lines[-1], font=font)
        pos = x + (bb[2] - bb[0])
        max_pos = x + max_width - ell_w
        if pos > max_pos:
            pos = max_pos
        draw.text((pos, cy - (bb[3] - bb[1]) - line_spacing), "…",
                  font=font, fill=fill)
    return cy


def make_card(p, idx):
    """生成单张商品卡片"""
    img = Image.new("RGB", (WIDTH, CARD_H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # 主题色: 由"商品主色"派生的可读色(对白字 ≥4.5:1 WCAG AA)。
    # 早期版本直接拿商品主色(浅灰/奶白/米色)当底色配白字 —— 实测 155 张历史卡片
    # 里 85 张(54.8%)白字对比度 < 4.5:1, 40 张 < 2.5:1 属不可读。
    color = safe_hex_to_rgb(theme_color_for(p), DEFAULT_THEME_RGB)
    # 原色只做顶部 8px 品牌点缀条, 不承载任何文字
    accent = safe_hex_to_rgb(p.get("color"), DEFAULT_THEME_RGB)
    y_cursor = 0

    # 顶部色条
    draw.rectangle([0, 0, WIDTH, 8], fill=accent)
    draw.rectangle([0, 8, WIDTH, 280], fill=color)
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

    # 副标题（取 desc 前 90 字；截断交给 draw_wrapped_text 统一加省略号）
    # 旧写法固定拼 "…"，desc 不足 90 字时会凭空多一个省略号
    subtitle = p["desc"][:90]
    y_cursor = draw_wrapped_text(draw, subtitle, 50, y_cursor, WIDTH - 100,
                                 font_subtitle, (80, 80, 80), 8, max_lines=3)
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

    # 完整描述（限制行数，避免顶到下方价格条）
    draw.text((50, y_cursor), "商品详情", font=font_subtitle, fill=color)
    y_cursor += 70
    y_cursor = draw_wrapped_text(draw, p["desc"], 50, y_cursor, WIDTH - 100, font_desc,
                                 (50, 50, 50), 8, max_lines=7)
    y_cursor += 25

    # --- 预先计算底部价格条位置, 供上方内容做避让 ---
    _text = p["price_note"]
    _max_w = WIDTH - 140
    _lines, _cur = [], ""
    for ch in _text:
        _test = _cur + ch
        _bb = draw.textbbox((0, 0), _test, font=font_small)
        if _bb[2] - _bb[0] <= _max_w:
            _cur = _test
        else:
            _lines.append(_cur)
            _cur = ch
    if _cur:
        _lines.append(_cur)
    _lines = _lines[:4]
    _line_h = 36
    _bar_h = len(_lines) * _line_h + 36
    _bar_top = CARD_H - 70 - _bar_h

    # 标签 chips（优先渲染：带货核心信息，始终保留）
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

    # 适用人群（空间不足则跳过，优先保证标签与价格条）
    if y_cursor < _bar_top - 30:
        draw.text((50, y_cursor), "适合人群", font=font_subtitle, fill=color)
        y_cursor += 60
        draw_wrapped_text(draw, p["suitable"], 50, y_cursor, WIDTH - 100, font_small, (80, 80, 80), 6)

    # 价格说明（自动换行，高度自适应，始终渲染并贴底对齐 logo 上方）
    text = _text
    lines = _lines
    line_h = _line_h
    bar_h = _bar_h
    bar_top = _bar_top
    draw.rounded_rectangle([50, bar_top, WIDTH - 50, bar_top + bar_h], radius=15, fill=color)
    ty = bar_top + 18
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=font_small)
        draw.text(((WIDTH - (bb[2] - bb[0])) // 2, ty), ln, font=font_small, fill=(255, 255, 255))
        ty += line_h

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
