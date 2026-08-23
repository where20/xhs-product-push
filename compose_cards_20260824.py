#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-24"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "数码配件",
        "title": "得力魔方插座转换器一转四：12.9元解锁桌面充电自由",
        "subtitle": "USB-A+USB-C+Qi无线充 · 四面独立插孔 · 3C认证 · 赠运费险",
        "desc": "插座不够用是每个租房党和办公族的痛！得力这款魔方插座，一转四面独立插孔，USB-A+USB-C双口加无线充电，四个面同时工作互不干扰。3C认证国标品质，防触保护门设计家有小孩也安心。巴掌大小不占桌面，12.9元还赠运费险，学生党、租房族、打工人都闭眼入。",
        "highlights": [
            "一转四面独立插孔，同时工作不打架",
            "USB-A+USB-C双口+Qi无线充电四合一",
            "3C认证+防触保护门，安全有保障",
            "巴掌大小不占桌面，桌面瞬间整洁",
            "赠运费险，12.9元学生党闭眼入"
        ],
        "tags": ["数码配件", "插座转换器", "桌面收纳", "开学必备", "宿舍好物"],
        "suitable": "学生党 · 租房族 · 办公族 · 数码达人",
        "price_note": "券后¥12.9",
        "img": f"{OUT_DIR}/orig_product_1.jpg",
        "color": "#3498DB",
    },
    {
        "num": "02",
        "category": "小家电",
        "title": "九阳mini电热水壶1L：33元搞定独居党和上班族的热水自由",
        "subtitle": "304不锈钢内胆 · 防烫手柄 · 3分钟速沸 · 1L黄金容量",
        "desc": "大壶烧太多喝不完，小壶刚好一个人！九阳这款mini电热水壶，1L黄金容量，304不锈钢内胆，防烫手柄设计，3分钟速沸。放在办公室桌面不占地方，租房党一个人用刚刚好，早起泡杯咖啡、下午泡壶茶，随时喝上新鲜热水。比点外卖送的水便宜太多，33元搞定每日饮水刚需。",
        "highlights": [
            "1L黄金容量，一个人喝刚好不浪费",
            "304不锈钢内胆，饮水安全有保障",
            "防烫手柄设计，倒水不怕烫手",
            "3分钟速沸，早八人不用等太久",
            "迷你体积放桌面，随时有热水喝"
        ],
        "tags": ["小家电", "电热水壶", "一人食", "办公室好物", "居家必备"],
        "suitable": "租房党 · 上班族 · 独居人群 · 学生党",
        "price_note": "券后¥33.04",
        "img": f"{OUT_DIR}/orig_product_2.jpg",
        "color": "#E67E22",
    },
    {
        "num": "03",
        "category": "个护美妆",
        "title": "蜂花防脱洗发水750ml：十几块钱的国货老牌，发量守护神",
        "subtitle": "生姜精华+人参提取 · 无硅油温和配方 · 防脱率82% · 国货老字号",
        "desc": "国货老字号终于被年轻人发现了！蜂花防脱系列，主打生姜精华加人参提取物，无硅油温和配方，泡沫丰富好冲洗。500ml装十几块、750ml装不到二十，这个价格还要什么自行车！实测防脱率82%，适合轻度发根松动、日常掉发人群。老品牌品质靠得住，花小钱办大事。",
        "highlights": [
            "国货老字号，1928年至今品质认证",
            "生姜精华+人参提取物，防脱有实证",
            "无硅油温和配方，泡沫丰富好冲洗",
            "750ml不到20元，性价比天花板",
            "防脱率82%，轻度脱发日常养护够用"
        ],
        "tags": ["个护", "洗发水", "防脱固发", "国货平价", "学生党"],
        "suitable": "学生党 · 预算党 · 日常防脱人群 · 送礼长辈",
        "price_note": "券后约¥17.9",
        "img": f"{OUT_DIR}/orig_product_3.jpg",
        "color": "#27AE60",
    },
    {
        "num": "04",
        "category": "家居清洁",
        "title": "水卫士防溅水香氛洁厕泡泡：19.9元让卫生间脱胎换骨",
        "subtitle": "泡沫深入死角 · 祛味除菌 · 淡淡香氛 · 懒人神器",
        "desc": "卫生间有异味是最尴尬的居家痛点！水卫士这款洁厕泡泡，泡沫深入马桶弯道死角，溶掉老污垢的同时祛味除菌。淡淡香氛味道不刺鼻，用完整个人卫生间清爽怡人。2大瓶装19.9元，折算下来一次清洁不到一块钱。比请保洁便宜，比普通洁厕灵好用，轻松搞定全家卫生间卫生问题。",
        "highlights": [
            "泡沫深入弯道死角，强力溶解老污垢",
            "祛味除菌二合一，卫生间告别异味",
            "淡淡香氛不刺鼻，用完空气清新",
            "2瓶19.9元，一次清洁不到一块钱",
            "懒人神器，喷完等几分钟冲掉即可"
        ],
        "tags": ["家居清洁", "洁厕用品", "卫生间神器", "懒人好物", "平价神器"],
        "suitable": "租房族 · 家庭主妇 · 懒人党 · 注重卫生人群",
        "price_note": "券后¥19.9/2瓶",
        "img": f"{OUT_DIR}/orig_product_4.jpg",
        "color": "#1ABC9C",
    },
    {
        "num": "05",
        "category": "护肤日用",
        "title": "一次性洗脸巾加厚款：比毛巾干净，比纸巾好用，敏感肌必备",
        "subtitle": "加厚不掉絮 · 随用随扔 · 一巾多用 · 14.9元60抽",
        "desc": "毛巾用久了滋生细菌螨虫，脸上反复长痘可能是毛巾的锅！一次性洗脸巾，随用随扔，彻底告别螨虫和细菌。加厚纯棉材质，触感细腻柔软不掉絮，湿水后韧性依然很强。洗完脸轻轻擦拭吸水，擦完还能顺手擦桌子擦镜子，一巾多用不浪费。14.9元60抽，一抽不到两毛五，精致懒人必备！",
        "highlights": [
            "加厚纯棉材质，触感细腻柔软不掉絮",
            "湿水后韧性依然强，不易破损",
            "随用随扔，彻底告别毛巾细菌螨虫",
            "一巾多用：洗脸→擦桌→擦镜子",
            "14.9元60抽，一抽不到两毛五"
        ],
        "tags": ["护肤日用", "洗脸巾", "洁面巾", "敏感肌", "懒人好物"],
        "suitable": "敏感肌人群 · 精致懒人 · 注重卫生人群 · 全家通用",
        "price_note": "券后¥14.9/60抽",
        "img": f"{OUT_DIR}/orig_product_5.jpg",
        "color": "#9B59B6",
    },
]


def load_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", size)
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.truetype(FONT_PATH, size)


def hex2rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def create_product_card(product, index):
    """创建单个商品卡片，3000px高"""
    card = Image.new('RGB', (WIDTH, CARD_H), 'white')
    draw = ImageDraw.Draw(card)

    color = hex2rgb(product['color'])

    # 顶部装饰条
    draw.rectangle([0, 0, WIDTH, 8], fill=color)

    # 商品编号 + 品类标签
    font_num = load_font(80, bold=True)
    font_cat = load_font(40)
    draw.text((40, 30), f"#{product['num']}", fill=color, font=font_num)
    draw.text((160, 45), product['category'], fill=(120, 120, 120), font=font_cat)

    # 商品图片
    img_path = product['img']
    if os.path.exists(img_path):
        img = Image.open(img_path).convert('RGB')
        img_w, img_h = img.size
        target_h = 800
        target_w = int(target_h * img_w / img_h)
        if target_w > WIDTH - 80:
            target_w = WIDTH - 80
            target_h = int(target_w * img_h / img_w)
        img = img.resize((target_w, target_h), Image.LANCZOS)
        paste_x = (WIDTH - target_w) // 2
        card.paste(img, (paste_x, 120))
        img_y = 120 + target_h
    else:
        draw.rectangle([40, 120, WIDTH-40, 920], fill=(240, 240, 240))
        draw.text((WIDTH//2 - 100, 500), "[图片]", fill=(180, 180, 180), font=load_font(50))
        img_y = 920

    # 标题（分两行）
    font_title = load_font(52, bold=True)
    title = product['title']
    if len(title) <= 30:
        draw.text((40, img_y + 30), title, fill=(30, 30, 30), font=font_title)
        title_y2 = img_y + 85
    else:
        split = title[:30].rfind('，') + 1 or title[:30].rfind('、') + 1 or title[:30].rfind('：') + 1 or 30
        draw.text((40, img_y + 30), title[:split], fill=(30, 30, 30), font=font_title)
        draw.text((40, img_y + 85), title[split:split+32], fill=(30, 30, 30), font=font_title)
        title_y2 = img_y + 130

    # 副标题
    font_sub = load_font(34)
    draw.text((40, title_y2 + 10), product['subtitle'], fill=(100, 100, 100), font=font_sub)

    # 价格
    font_price = load_font(60, bold=True)
    draw.text((40, title_y2 + 60), product['price_note'], fill=color, font=font_price)

    # 分割线
    line_y = title_y2 + 135
    draw.line([(40, line_y), (WIDTH-40, line_y)], fill=(220, 220, 220), width=2)

    # 描述文字
    font_desc = load_font(36)
    desc_y = line_y + 20
    max_chars = 36
    lines = []
    for i in range(0, len(product['desc']), max_chars):
        lines.append(product['desc'][i:i+max_chars])
    for line in lines[:4]:
        draw.text((40, desc_y), line, fill=(80, 80, 80), font=font_desc)
        desc_y += 48

    # 亮点标题
    hl_y = desc_y + 20
    draw.rectangle([40, hl_y, 200, hl_y + 5], fill=color)
    font_hl_title = load_font(38, bold=True)
    draw.text((40, hl_y + 15), "核心亮点", fill=(40, 40, 40), font=font_hl_title)

    # 亮点列表
    font_hl = load_font(34)
    bullet_y = hl_y + 65
    for i, hl in enumerate(product['highlights']):
        bullet_text = f"  {i+1}. {hl}"
        draw.text((40, bullet_y), bullet_text, fill=(60, 60, 60), font=font_hl)
        bullet_y += 48

    # 标签
    tag_y = bullet_y + 30
    font_tag = load_font(30)
    x_pos = 40
    for tag in product['tags']:
        tag_w = len(tag) * 30 + 24
        draw.rounded_rectangle([x_pos, tag_y, x_pos + tag_w, tag_y + 50], radius=10, fill=(240, 240, 240))
        draw.text((x_pos + 12, tag_y + 8), tag, fill=(100, 100, 100), font=font_tag)
        x_pos += tag_w + 15
        if x_pos > WIDTH - 200:
            x_pos = 40
            tag_y += 65

    # 适用人群
    suit_y = tag_y + 80
    draw.text((40, suit_y), f"适用：{product['suitable']}", fill=(140, 140, 140), font=load_font(30))

    # 底部装饰
    draw.rectangle([0, CARD_H - 8, WIDTH, CARD_H], fill=color)

    return card


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    all_cards = []
    for i, product in enumerate(PRODUCTS):
        card = create_product_card(product, i)
        all_cards.append(card)

    # 合成全图
    full_h = len(all_cards) * CARD_H + (len(all_cards) - 1) * GAP
    full_img = Image.new('RGB', (WIDTH, full_h), 'white')

    y_offset = 0
    for card in all_cards:
        full_img.paste(card, (0, y_offset))
        y_offset += CARD_H + GAP

    full_img.save(f"{OUT_DIR}/product_card_full.jpg", quality=95)
    print(f"全图已保存: {OUT_DIR}/product_card_full.jpg ({WIDTH}x{full_h})")

    # 裁剪成5张
    for i in range(len(all_cards)):
        y_start = i * (CARD_H + GAP)
        y_end = y_start + CARD_H
        segment = full_img.crop((0, y_start, WIDTH, y_end))
        segment.save(f"{OUT_DIR}/product_{i+1}.jpg", quality=92)
        print(f"第{i+1}张卡片已保存: {OUT_DIR}/product_{i+1}.jpg")

    print("全部完成！")


if __name__ == "__main__":
    main()
