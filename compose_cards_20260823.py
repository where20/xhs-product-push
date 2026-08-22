#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-23"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "厨房电器",
        "title": "美的 M2H1 小滋味微蒸烤炸一体机：369元解锁「厨房全能料理主机」",
        "subtitle": "微波空气炸 · 0.2秒瞬热烤管 · 五档变频 · 44道自动菜单 · 仅334mm深",
        "desc": "一台顶三台，这台微波炉重新定义了「热饭工具」的上限。美的 M2H1 小滋味系列将微波、蒸汽、烧烤、空气炸四大功能合为一体，配合专利 0.2 秒瞬热烤管和五档变频微波，下班回家无需预热，冻鸡翅直接扔进去，10 分钟出菜、均匀熟透，上班族和小家庭的厨房效率神器。",
        "highlights": [
            "微波空气炸：上下双烤管 + 360°热风，大块带骨肉10分钟熟透，无需翻面",
            "0.2秒瞬热烤管：开机即烤，省去预热等待，忙碌早餐也能快速搞定",
            "五档变频微波：低温发酵、慢速解冻、文火慢炖、中火焗烤、高温速热全覆盖",
            "机身仅334mm深：小厨房友好，不挤占台面空间",
            "44道自动菜单：彩屏触控选菜单，新手也能做出快手硬菜"
        ],
        "tags": ["微蒸烤炸一体", "省时神器", "小厨房首选", "懒人料理", "国补到手价"],
        "suitable": "上班族 · 小家庭 · 租房党 · 厨房新手",
        "price_note": "京东¥369",
        "img": f"{OUT_DIR}/orig_product_1.jpg",
        "color": "#E74C3C",
    },
    {
        "num": "02",
        "category": "居家清洁",
        "title": "网易严选除螨喷雾：免洗免晒，躺在床上终于「螨」没了",
        "subtitle": "植物抑螨成分 · 免洗免晒 · 卧室全覆盖 · 开学季宿舍必备 · ¥21.9",
        "desc": "被子、枕头、床垫、沙发——肉眼看不见的螨虫每天陪你入睡。网易严选这款除螨喷雾添加天然植物抑螨成分，喷洒后自然晾干即可，无需晾晒、无需清洗，适合学生宿舍、租房党和小空间家庭。喷雾细腻均匀，覆盖率高，一瓶搞定卧室全场景的螨虫困扰，开学季宿舍必备好物。",
        "highlights": [
            "植物成分抑螨：不添加杀虫剂，温和配方，敏感肌和母婴家庭可用",
            "免洗免晒：喷洒后自然晾干，省去晾晒等待，随时随地操作",
            "一瓶多用：被子、枕头、床垫、沙发、毛绒玩具全覆盖",
            "开学季宿舍必备：南方潮湿气候尤其需要，租房党和学生党刚需",
            "高性价比：21.9元搞定整间卧室除螨，均价不到2元/次"
        ],
        "tags": ["除螨抑菌", "免洗免晒", "宿舍好物", "居家刚需", "开学必备"],
        "suitable": "学生党 · 租房族 · 母婴家庭 · 南方潮湿地区",
        "price_note": "京东¥21.9",
        "img": f"{OUT_DIR}/orig_product_2.jpg",
        "color": "#27AE60",
    },
    {
        "num": "03",
        "category": "洗护美妆",
        "title": "水优季香氛沐浴露：高级伪体香，洗完被窝都是香的",
        "subtitle": "白兰天竺葵花木香调 · 氨基酸养肤 · 48小时持久留香 · 400ml大容量",
        "desc": "不是香水，却比香水更懂「自然伪体香」。水优季香氛沐浴露以白兰混合天竺葵花木香调为核心，清雅不甜腻、不刺鼻。配合氨基酸养肤体系，温和清洁的同时补水保湿，洗完肌肤水润通透，完全不拔干、不假滑。留香效果出众，洗澡后身上、浴室、被窝都会萦绕淡淡清香。",
        "highlights": [
            "白兰天竺葵花木香调：清雅治愈，自带氛围感伪体香，留香48小时",
            "氨基酸养肤体系：18种氨基酸 + 植物精油，温和清洁同时补水保湿",
            "浓稠啫喱质地：泡沫绵密丰富，一泵可洗全身，用量超省",
            "敏感肌友好：不含刺激性成分，夏季多汗和干燥敏感肌均适用",
            "400ml大容量：全家可用，一瓶顶一个月，均价不到1元/次"
        ],
        "tags": ["香氛沐浴露", "伪体香", "氨基酸养肤", "留香持久", "夏日本草"],
        "suitable": "追求香氛感人群 · 敏感肌 · 日常洗护升级",
        "price_note": "京东¥39.9",
        "img": f"{OUT_DIR}/orig_product_3.jpg",
        "color": "#9B59B6",
    },
    {
        "num": "04",
        "category": "洗护美妆",
        "title": "澳宝氨基酸沐浴露3瓶装：经典老牌回归，超市同款不到¥15/瓶",
        "subtitle": "三香套装 · 百合/蔷薇/橙花 · 500ml大容量 · 老广二十年口碑",
        "desc": "澳宝不需要营销，老广们用了二十年的口碑就是最好的广告。这款氨基酸沐浴露三瓶装含百合、蔷薇、橙花三种经典香型，泡沫丰富细腻、温和不刺激，洗完皮肤清爽不紧绷。3瓶500ml大容量装，超市同款品质，家庭囤货刚需好价。夏天出汗多，一瓶全家够用三个月。",
        "highlights": [
            "三香型套装：百合、蔷薇、橙花三种经典香型，满足不同喜好",
            "500ml大瓶装：澳洲配方，实惠大碗，全家可用三个月",
            "泡沫丰富细腻：温和清洁，洗完皮肤清爽不紧绷，夏季刚需",
            "超市同款品质：老广口碑品牌，二十年轻工品质积累",
            "历史低价41.2元/3瓶：单瓶不到14元，比超市更划算"
        ],
        "tags": ["经典沐浴露", "三香套装", "超市同款", "家庭囤货", "夏季刚需"],
        "suitable": "家庭用户 · 沐浴露囤货党 · 经典国货爱好者",
        "price_note": "京东¥41.2",
        "img": f"{OUT_DIR}/orig_product_4.jpg",
        "color": "#E91E63",
    },
    {
        "num": "05",
        "category": "洗护美妆",
        "title": "舒肤佳白桃乌龙樱花沐浴露：72小时淡雅留香，洗完整个人都温柔了",
        "subtitle": "白桃乌龙+樱花三调香 · 72小时留香 · 1.3kg超大桶 · 氨基酸配方",
        "desc": "舒肤佳这次真的卷到了香味赛道。白桃乌龙与樱花双香型混搭，前调清甜白桃，中调乌龙茶香收尾，尾调用樱花点缀，层次感分明。氨基酸配方温和不拔干，1.3kg超大桶装用到天荒地老。72小时淡雅留香，洗完澡整个人都带着温柔感，日常约会通勤都很加分。",
        "highlights": [
            "白桃乌龙 + 樱花三调香氛：前中后三调层次分明，不是普通沐浴露能比的",
            "72小时淡雅留香：比多数香水更持久，洗完被窝里都是香的",
            "氨基酸温和配方：温和清洁不刺激，敏感肌也能用",
            "1.3kg超大桶装：用到天荒地老，单次成本不到1元",
            "舒肤佳品牌保障：国民老牌，配方安全，超市常年畅销"
        ],
        "tags": ["香氛沐浴露", "三调香型", "72小时留香", "大桶装", "国民老牌"],
        "suitable": "日常约会 · 通勤人群 · 追求香感的女生 · 沐浴露重度用户",
        "price_note": "京东¥29.3",
        "img": f"{OUT_DIR}/orig_product_5.jpg",
        "color": "#F06292",
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
