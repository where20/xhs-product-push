#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-22"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "数码装备",
        "title": "影石 Insta360 X4 全景运动相机：先拍摄再构图，8K超清记录每个瞬间",
        "subtitle": "8K全景录制 · AI智能剪辑 · FlowState防抖 · 10米防水 · 135分钟续航",
        "desc": "Insta360 X4 是影石全新一代旗舰全景相机，搭载 5nm AI 芯片，突破性支持 8K30fps 全景视频录制，配合 5.7K60fps 高帧率和 4K100fps 慢动作，无论骑行、滑雪还是旅行，一机搞定所有精彩视角。隐形自拍杆让画面中自拍杆完全消失，轻松拍出无人机跟拍大片感。",
        "highlights": [
            "8K30fps 全景视频 + 5.7K60fps 高帧率，影像力拉到顶",
            "隐形自拍杆效果，呈现无人机跟拍视角",
            "FlowState 防抖 + 360° 水平矫正，颠簸画面也稳如泰山",
            "10 米防水 + 135 分钟续航，户外运动无压力",
            "AI 一键出片，App 剪辑零门槛"
        ],
        "tags": ["全景相机", "8K录像", "AI剪辑", "骑行装备", "vlog神器"],
        "suitable": "vlog博主 · 骑行爱好者 · 滑雪玩家 · 旅行记录者",
        "price_note": "京东¥2,999",
        "img": f"{OUT_DIR}/orig_product_1.jpg",
        "color": "#5C6BC0",
    },
    {
        "num": "02",
        "category": "健康办公",
        "title": "乐歌 E7Pro 电动升降桌：双电机价格甜点，久坐办公族的续命神器",
        "subtitle": "双电机 · 125kg承重 · 35mm/s升降 · 4档记忆 · 钢化玻璃桌面",
        "desc": "乐歌 E7Pro 是 2026 年双电机电动升降桌的「价格甜点」，双电机配置承重 125kg，升降速度达 35mm/s，钢化玻璃桌面质感高级。4 档高度记忆，家里人各自设定一键切换，遇阻回弹保护功能，桌下有孩子宠物也安心。久坐超 1 小时就腰酸背痛？一键切换站立办公，站着效率更高。",
        "highlights": [
            "双电机驱动，承重 125kg，多显示器 + 主机全搞定",
            "35mm/s 升降速度，3 秒坐站切换",
            "钢化玻璃桌面，质感高级，清洁一抹即净",
            "4 档高度记忆，家人各设各的，一键直达",
            "遇阻回弹保护，安全性拉满"
        ],
        "tags": ["电动升降桌", "双电机", "久坐救星", "办公装备", "健康生活"],
        "suitable": "居家办公族 · 程序员 · 设计师 · 学生宿舍",
        "price_note": "京东¥1,299",
        "img": f"{OUT_DIR}/orig_product_2.jpg",
        "color": "#26A69A",
    },
    {
        "num": "03",
        "category": "睡眠好物",
        "title": "TLK特蕾卡护颈记忆棉枕：三阶释压分区，脖子终于找到对的支撑",
        "subtitle": "五分区人体工学 · 6-12cm高度可调 · 三层复合释压 · 翻身0分贝",
        "desc": "TLK特蕾卡护颈枕是 2026 年护颈枕横评综合第一，五分区人体工学结构精准适配颈椎自然曲度。脑窝释压区稳稳托住头部，颈椎强力支撑区主动填补颈后空隙。三层复合结构（云感释压绵 + 韧力支撑绵 + 高密抗压绵）兼顾柔软包裹与整夜稳定支撑。TPE 软管支持 6-12cm 高度自由调节。",
        "highlights": [
            "五分区人体工学结构，颈椎贴合度实测第一",
            "6-12cm 高度自由调节，精准匹配个人颈椎曲度",
            "三层复合释压，柔软包裹 + 整夜稳托",
            "翻身趋近 0 分贝，宿舍/夫妻同枕互不干扰",
            "整枕可机洗 + 母婴级安全认证"
        ],
        "tags": ["护颈枕", "记忆棉", "五分区支撑", "可调节高度", "颈椎护理"],
        "suitable": "久坐办公族 · 落枕反复 · 混合睡姿 · 宿舍共用",
        "price_note": "京东¥259",
        "img": f"{OUT_DIR}/orig_product_3.jpg",
        "color": "#66BB6A",
    },
    {
        "num": "04",
        "category": "居家安全",
        "title": "探秘智能感应小夜灯：中科院硅基黄光技术，零蓝光护眼整晚不伤眼",
        "subtitle": "中科院硅基黄光 · FPF≤0.05%零蓝光 · 3.5米人体感应 · 2700K暖黄光",
        "desc": "探秘小夜灯搭载中科院硅基黄光技术，通过权威无蓝光认证（FPF≤0.05%），真正零蓝光护眼。120° 人体感应 + 光敏双传感器，感应距离 3.5 米，反应速度 0.3 秒，夜间起身自动亮灯，人走后 30 秒缓慢熄灭，不惊扰睡眠。2700K 暖黄光经多层漫反射处理，光线柔和不直射眼睛。",
        "highlights": [
            "中科院硅基黄光技术，FPF≤0.05%，真正零蓝光护眼",
            "120° 人体感应 + 光敏双传感器，3.5 米感应、0.3 秒响应",
            "2700K 暖黄光 + 多层漫反射，起夜开灯不晃眼",
            "人走 30 秒缓慢熄灭，不惊扰家人睡眠",
            "食品级软硅胶一体成型，Type-C 快充 2.5 小时"
        ],
        "tags": ["智能感应灯", "零蓝光", "护眼夜灯", "人体感应", "母婴适用"],
        "suitable": "母婴家庭 · 老年人 · 独居青年 · 夜起人群",
        "price_note": "京东¥79",
        "img": f"{OUT_DIR}/orig_product_4.jpg",
        "color": "#FFA726",
    },
    {
        "num": "05",
        "category": "氛围好物",
        "title": "ALLWAY Aqua10 香薰机蓝牙音响：冷雾香薰 + 蓝牙Hi-Fi + 助眠灯光",
        "subtitle": "三合一香薰机 · 华东师大认证 · LDAC高清音质 · 1600万色RGB · SGS抗菌",
        "desc": "ALLWAY Aqua10 是 2026 年「科学情绪干预终端」，一台实现冷雾香薰扩散 + 蓝牙 Hi-Fi 音响 + 智能氛围灯光三合一。磁吸式冷扩香结构兼容水溶性/油溶性精油，配合华东师范大学心理学院双盲测试认证的定制复方精油，受试者 α 脑波增幅 19.3%。音响部分 2×5W 钕磁喇叭 + LDAC 高清编码，1600 万色 RGB + 节律光谱模式。",
        "highlights": [
            "冷雾香薰 + 蓝牙音响 + 氛围灯光，一机三用",
            "华东师大双盲测试认证，α 脑波增幅 19.3%",
            "2×5W 钕磁喇叭 + LDAC 高清编码，音质发烧级",
            "1600 万色 RGB + 节律光谱模式，适配全天情绪节律",
            "SGS 抗菌认证，大肠杆菌抑制率 99.2%"
        ],
        "tags": ["香薰机", "蓝牙音响", "助眠灯光", "三合一", "情绪疗愈"],
        "suitable": "卧室助眠 · 办公舒压 · 瑜伽冥想 · 七夕送礼",
        "price_note": "京东¥399",
        "img": f"{OUT_DIR}/orig_product_5.jpg",
        "color": "#AB47BC",
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
    num = product['num']
    category = product['category']
    title = product['title']
    subtitle = product['subtitle']
    desc = product['desc']
    highlights = product['highlights']
    tags = product['tags']
    suitable = product['suitable']
    price_note = product['price_note']
    img_path = product['img']

    # 顶部装饰条
    draw.rectangle([0, 0, WIDTH, 8], fill=color)

    # 商品编号 + 品类标签
    font_num = load_font(80, bold=True)
    font_cat = load_font(40)
    draw.text((40, 30), f"#{num}", fill=color, font=font_num)
    draw.text((160, 45), category, fill=(120, 120, 120), font=font_cat)

    # 商品图片
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
    if len(title) <= 30:
        draw.text((40, img_y + 30), title, fill=(30, 30, 30), font=font_title)
        title_y2 = img_y + 85
    else:
        # 找到合适断点
        split = title[:30].rfind('，') + 1 or title[:30].rfind('、') + 1 or 30
        draw.text((40, img_y + 30), title[:split], fill=(30, 30, 30), font=font_title)
        draw.text((40, img_y + 85), title[split:split+32], fill=(30, 30, 30), font=font_title)
        title_y2 = img_y + 130

    # 副标题
    font_sub = load_font(34)
    draw.text((40, title_y2 + 10), subtitle, fill=(100, 100, 100), font=font_sub)

    # 价格
    font_price = load_font(60, bold=True)
    draw.text((40, title_y2 + 60), price_note, fill=color, font=font_price)

    # 分割线
    line_y = title_y2 + 135
    draw.line([(40, line_y), (WIDTH-40, line_y)], fill=(220, 220, 220), width=2)

    # 描述文字
    font_desc = load_font(36)
    desc_y = line_y + 20
    max_chars = 36
    lines = []
    for i in range(0, len(desc), max_chars):
        lines.append(desc[i:i+max_chars])
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
    for i, hl in enumerate(highlights):
        bullet_text = f"  {i+1}. {hl}"
        draw.text((40, bullet_y), bullet_text, fill=(60, 60, 60), font=font_hl)
        bullet_y += 48

    # 标签
    tag_y = bullet_y + 30
    font_tag = load_font(30)
    x_pos = 40
    for tag in tags:
        tag_w = len(tag) * 30 + 24
        draw.rounded_rectangle([x_pos, tag_y, x_pos + tag_w, tag_y + 50], radius=10, fill=(240, 240, 240))
        draw.text((x_pos + 12, tag_y + 8), tag, fill=(100, 100, 100), font=font_tag)
        x_pos += tag_w + 15
        if x_pos > WIDTH - 200:
            x_pos = 40
            tag_y += 65

    # 适用人群
    suit_y = tag_y + 80
    draw.text((40, suit_y), f"适用：{suitable}", fill=(140, 140, 140), font=load_font(30))

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
