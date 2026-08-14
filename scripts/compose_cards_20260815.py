#!/usr/bin/env python3
"""
xhs-product-push 商品详情长图合成脚本 2026-08-15
生成: product_card_full.jpg (1080px宽) + product_1.jpg ~ product_5.jpg (5等分裁剪)
配色主题: 数码蓝/冰丝粉/充电绿/空调橙/相机紫
"""
import os, json, sys
from PIL import Image, ImageDraw, ImageFont

PYTHON_BIN = "/Users/xiaoan/.workbuddy/binaries/python/versions/3.13.12/bin/python3"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-08-15"
DATA_FILE = os.path.join(OUT_DIR, "data.json")
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_HEIGHT = 1500
NUM_PRODUCTS = 5

# 商品主色调 (背景, 文字, 强调色)
THEMES = [
    ("#E3F2FD", "#1565C0", "#42A5F5"),  # Redmi手机-蓝
    ("#FCE4EC", "#AD1457", "#EC407A"),  # 冰丝防晒衣-粉
    ("#E8F5E9", "#2E7D32", "#66BB6A"),  # 移动电源-绿
    ("#FFF3E0", "#E65100", "#FF9800"),  # 空调-橙
    ("#EDE7F6", "#4527A0", "#7E57C2"),  # 大疆相机-紫
]

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            test = (line + " " + word).strip()
            if font.getlength(test) <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines

def draw_card(canvas, product, index, theme, product_img_path):
    bg_color, accent_color, text_color = theme
    draw = ImageDraw.Draw(canvas)
    card_y = index * CARD_HEIGHT

    draw.rectangle([0, card_y, WIDTH, card_y + CARD_HEIGHT], fill=bg_color)
    draw.rectangle([0, card_y, WIDTH, card_y + 6], fill=accent_color)

    # 商品实图
    orig_img_path = os.path.join(OUT_DIR, product.get("image", f"orig_product_{index+1}.jpg"))
    if os.path.exists(orig_img_path):
        try:
            orig_img = Image.open(orig_img_path).convert("RGBA")
            img_x, img_y = WIDTH - 360, card_y + 30
            img_w, img_h = 330, 330
            orig_img = orig_img.resize((img_w, img_h), Image.LANCZOS)
            # 白色圆角背景
            bg_layer = Image.new("RGBA", (img_w, img_h), (255, 255, 255, 255))
            bg_layer.paste(orig_img, (0, 0))
            canvas.paste(bg_layer, (img_x, img_y), bg_layer)
        except Exception as e:
            print(f"⚠️ 图片加载失败 {orig_img_path}: {e}")
            draw.rounded_rectangle([img_x, img_y, img_x + 330, img_y + 330], radius=20, fill="white")
            draw.ellipse([img_x+50, img_y+50, img_x+280, img_y+280], fill=accent_color+"33")
    else:
        img_x, img_y = WIDTH - 360, card_y + 30
        draw.rounded_rectangle([img_x, img_y, img_x + 330, img_y + 330], radius=20, fill="white")
        draw.ellipse([img_x + 50, img_y + 50, img_x + 280, img_y + 280], fill=accent_color + "33")
        draw.ellipse([img_x + 100, img_y + 100, img_x + 230, img_y + 230], fill=accent_color + "55")

    # 序号圆
    seq_x, seq_y = 40, card_y + 30
    draw.ellipse([seq_x, seq_y, seq_x + 60, seq_y + 60], fill=accent_color)
    try:
        seq_font = ImageFont.truetype(FONT_PATH, 28)
    except:
        seq_font = ImageFont.load_default()
    seq_text = str(product["id"])
    tw, th = draw.textbbox((0, 0), seq_text, font=seq_font)[2:]
    draw.text((seq_x + 30 - tw//2, seq_y + 30 - th//2), seq_text, fill="white", font=seq_font)

    # 标题
    try:
        title_font = ImageFont.truetype(FONT_PATH, 34)
        tag_font = ImageFont.truetype(FONT_PATH, 22)
        desc_font = ImageFont.truetype(FONT_PATH, 26)
        hl_font = ImageFont.truetype(FONT_PATH, 24)
    except:
        title_font = tag_font = desc_font = hl_font = ImageFont.load_default()

    title = product["name"]
    title_lines = wrap_text(title, title_font, 640)
    ty = card_y + 35
    for line in title_lines[:2]:
        draw.text((40, ty), line, fill=text_color, font=title_font)
        ty += 42

    # 分类标签
    cat = product.get("category", "")
    ty += 10
    try:
        tag_box = draw.textbbox((0, 0), cat, font=tag_font)
        tag_w = tag_box[2] - tag_box[0]
    except:
        tag_w = len(cat) * 14
    draw.rounded_rectangle([40, ty, 40 + tag_w + 20, ty + 38], radius=10, fill=accent_color)
    draw.text((50, ty + 5), cat, fill="white", font=tag_font)

    # 价格区间
    price = product.get("priceRange", "")
    ty += 50
    draw.text((40, ty), price, fill=text_color, font=tag_font)

    # 描述
    desc = product.get("description", "")
    ty += 45
    desc_lines = wrap_text(desc, desc_font, WIDTH - 80)
    for line in desc_lines[:4]:
        draw.text((40, ty), line, fill="#444444", font=desc_font)
        ty += 34

    # 分隔线
    ty += 15
    draw.line([(40, ty), (WIDTH - 40, ty)], fill=accent_color + "55", width=2)

    # 亮点
    ty += 20
    draw.text((40, ty), "✨ 核心亮点", fill=text_color, font=hl_font)
    ty += 38
    highlights = product.get("highlights", [])
    for hl in highlights[:5]:
        hl_lines = wrap_text("• " + hl, hl_font, WIDTH - 80)
        for line in hl_lines:
            draw.text((50, ty), line, fill="#333333", font=hl_font)
            ty += 30
        ty += 4

    # 卖点标签
    ty += 10
    tags = product.get("tags", [])
    tx = 40
    ty2 = ty + 30
    for tag in tags:
        try:
            t_box = draw.textbbox((0, 0), tag, font=tag_font)
            t_w = t_box[2] - t_box[0] + 16
        except:
            t_w = len(tag) * 14 + 16
        if tx + t_w > WIDTH - 30:
            tx = 40
            ty2 += 42
        draw.rounded_rectangle([tx, ty, tx + t_w, ty + 36], radius=8, fill=accent_color + "22", outline=accent_color)
        draw.text((tx + 8, ty + 6), tag, fill=text_color, font=tag_font)
        tx += t_w + 10

    # 来源标注
    ty2 += 55
    source = product.get("source", "")
    try:
        s_box = draw.textbbox((0, 0), f"📌 {source}", font=tag_font)
        s_w = s_box[2] - s_box[0]
    except:
        s_w = len(source) * 12
    draw.rounded_rectangle([40, ty2, 40 + s_w + 20, ty2 + 36], radius=8, fill="#f5f5f5")
    draw.text((50, ty2 + 6), f"📌 {source}", fill="#888888", font=tag_font)

    return canvas

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    data = load_data()
    products = data["products"]

    canvas = Image.new("RGB", (WIDTH, CARD_HEIGHT * NUM_PRODUCTS), "white")

    for i, product in enumerate(products):
        theme = THEMES[i % len(THEMES)]
        draw_card(canvas, product, i, theme, None)

    # 保存全图
    full_path = os.path.join(OUT_DIR, "product_card_full.jpg")
    canvas.save(full_path, "JPEG", quality=95)
    print(f"✅ 全图已保存: {full_path}")

    # 裁剪5张
    for i in range(NUM_PRODUCTS):
        crop_y = i * CARD_HEIGHT
        card_img = canvas.crop((0, crop_y, WIDTH, crop_y + CARD_HEIGHT))
        out_path = os.path.join(OUT_DIR, f"product_{i+1}.jpg")
        card_img.save(out_path, "JPEG", quality=92)
        print(f"✅ 第{i+1}张已保存: {out_path}")

if __name__ == "__main__":
    main()
