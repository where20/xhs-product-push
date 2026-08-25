#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-26"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "小家电",
        "title": "希亦CG超声波清洗机：179元眼镜党神器，首发深度清洁",
        "subtitle": "48000Hz超声波 · UCT2.0技术 · UVC杀菌 · 42项严苛认证",
        "desc": "眼镜党、首饰控、化妆刷族的清洁救星！希亦CG超声波清洗机，179元解锁专业级深层清洁。48000Hz高频超声波每秒产生数万个微气泡，深入0.1mm缝隙将油脂灰尘彻底震离，配合UVC紫外线同步杀菌，眼镜鼻托、首饰雕花、化妆刷毛根、剃须刀头——这些手洗永远够不到的地方，CG2都能搞定。420ml大容量，一次可洗眼镜+手表+首饰。42项严苛认证，安全无虞。",
        "highlights": [
            "48000Hz高频超声波，镜片洁净率99%",
            "UCT2.0超能气泡技术，清洁力提升40%",
            "UVC紫外线同步杀菌，除菌率99.99%",
            "420ml加深清洁槽，眼镜首饰手表皆可用",
            "42项严苛测试认证，安全不伤物件"
        ],
        "tags": ["小家电", "超声波清洗", "眼镜党", "宿舍好物", "开学必备"],
        "suitable": "眼镜党 · 首饰控 · 化妆刷族 · 洁癖星人",
        "price_note": "参考价¥179",
        "img": f"{OUT_DIR}/product_1.jpg",
        "color": "#3498DB",
    },
    {
        "num": "02",
        "category": "数码配件",
        "title": "西圣Mike2领夹麦克风：199元校园创作神器，小白秒变专业博主",
        "subtitle": "98%清晰度 · AI降噪DSP · 即插即用 · 百元天花板",
        "desc": "开学想做社团短视频、课程录制、Vlog创作？西圣Mike2领夹麦克风，199元让你的音频质感直接跃升专业级别。高灵敏度全指向麦搭配发烧级AI降噪DSP芯片，嘈杂的操场、食堂、教室环境都能稳稳收好人声，清晰度高达98%。32位浮点数计算DSP，把万元级录音棚才有的音质下放到百元机型。手机、相机、电脑三端即插即用，录音小白也能秒上手。",
        "highlights": [
            "高灵敏度全指向麦，清晰度达98%",
            "发烧级AI降噪DSP芯片，嘈杂环境也能收音",
            "32位浮点数DSP芯片，万元级音质下放到百元",
            "手机相机电脑即插即用，录音小白秒上手",
            "百元麦克风天花板，小红书博主首选"
        ],
        "tags": ["数码配件", "领夹麦克风", "Vlog神器", "学生创作", "校园好物"],
        "suitable": "学生Vlogger · 课程录制 · 社团宣传 · 内容创作者",
        "price_note": "参考价¥199",
        "img": f"{OUT_DIR}/product_2.jpg",
        "color": "#F39C12",
    },
    {
        "num": "03",
        "category": "数码配件",
        "title": "闪迪至尊超极速移动固态SSD：1TB仅799元，大学生存储刚需",
        "subtitle": "读取2000MB/s · 金属抗摔 · 密码保护 · Win/Mac即插即用",
        "desc": "专业课作业多、剪辑素材大、课件PPT满天飞？闪迪至尊超极速移动固态SSD，1TB仅799元，是大学生存储扩容的高性价比之选。读取2000MB/s、写入1900MB/s，一部4K视频素材几秒传完，不用干等进度条。金属抗摔外壳，小巧便携，直接塞进书包侧袋。500G/1T双容量按需选，支持密码保护，论文和课程作业隐私不泄露。",
        "highlights": [
            "读取2000MB/s，写入1900MB/s极速传输",
            "金属抗摔外壳，宿舍图书馆随身带不怕磕",
            "500G/1T两种容量，大文件课件秒传不等待",
            "密码保护功能，论文资料隐私安全",
            "Win/Mac双系统兼容，即插即用无需驱动"
        ],
        "tags": ["数码配件", "移动固态硬盘", "存储设备", "大学生必备", "数码装备"],
        "suitable": "大学生 · 视频创作者 · 数据分析师 · 考研党",
        "price_note": "参考价¥799（1TB）",
        "img": f"{OUT_DIR}/product_3.jpg",
        "color": "#1ABC9C",
    },
    {
        "num": "04",
        "category": "小家电",
        "title": "美的M1-L213B微波炉：244元宿舍刚需，热饭解冻全能搞定",
        "subtitle": "21L容量 · 第五代磁控管 · 700W功率 · 行业TOP1品牌",
        "desc": "宿舍没有厨房、微波炉是刚需！美的M1-L213B微波炉，244元拿下21L黄金容量。700W功率，第五代磁控管加持，加热均匀不夹生，热饭热菜一键搞定。机械旋钮操作，比智能触屏更耐用。美的作为微波炉行业零售额TOP1品牌，累计用户超1.2亿，服务网点全覆盖，售后无忧。244元解决90%的日常加热需求，比叫外卖便宜，比排队微波炉快。",
        "highlights": [
            "21L容量，第五代磁控管，加热均匀不夹生",
            "700W功率，1-4人家庭/宿舍通用",
            "累计销量千万级，300元内微波炉闭眼选",
            "机械旋钮操作，爷爷奶奶也能秒上手",
            "美的行业TOP1品牌，服务网点全覆盖"
        ],
        "tags": ["小家电", "微波炉", "宿舍好物", "租房必备", "平价刚需"],
        "suitable": "租房党 · 宿舍党 · 独居人士 · 初独立学生",
        "price_note": "参考价¥244",
        "img": f"{OUT_DIR}/product_4.jpg",
        "color": "#E74C3C",
    },
    {
        "num": "05",
        "category": "数码配件",
        "title": "绿联双模无线鼠标：49.9元宿舍静音神器，久用手腕不酸",
        "subtitle": "人体工学 · 蓝牙+2.4G双模 · 静音按键 · DPI多档可调",
        "desc": "赶论文、做PPT、刷网课，一只好鼠标能大大提升效率。绿联双模无线鼠标，49.9元拿下人体工学造型，贴合手掌弧度，长时间使用手腕不易酸胀。蓝牙+2.4G双模连接，一键在笔记本、平板、手机之间切换。轻音按键设计，深夜在宿舍赶作业也不会打扰室友。DPI多档可调，兼容多种系统。49.9元耐用抗造，开学季高性价比刚需。",
        "highlights": [
            "人体工学造型，贴合手掌弧度，久用手腕不酸",
            "蓝牙+2.4G双模，手机平板笔记本一键切换",
            "轻音按键设计，深夜赶作业不打扰室友",
            "DPI多档可调，定位精准兼容Win/Mac/Harmony",
            "49.9元高性价比，丢了大不了再买一个"
        ],
        "tags": ["数码配件", "无线鼠标", "静音鼠标", "宿舍好物", "高性价比"],
        "suitable": "学生 · 办公族 · 静音需求者 · 码字党",
        "price_note": "参考价¥49.9",
        "img": f"{OUT_DIR}/product_5.jpg",
        "color": "#9B59B6",
    },
]

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def hex2rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def make_product_card(product):
    """制作单个商品卡片 1080x3000"""
    card = Image.new('RGB', (WIDTH, CARD_H), (255, 255, 255))
    draw = ImageDraw.Draw(card)
    font_title = load_font(52)
    font_subtitle = load_font(34)
    font_desc = load_font(30)
    font_highlight = load_font(28)
    font_tag = load_font(22)
    font_num = load_font(80)
    font_cat = load_font(28)
    font_price = load_font(38)
    font_suitable = load_font(24)
    font_label = load_font(26)

    color = hex2rgb(product["color"])
    PADDING = 50
    IMG_W = WIDTH - 2 * PADDING
    IMG_H = 1400

    # 商品图片区域
    try:
        img = Image.open(product["img"]).convert('RGB')
        img.thumbnail((IMG_W, IMG_H), Image.LANCZOS)
        iw, ih = img.size
        x_img = (WIDTH - iw) // 2
        y_img = PADDING
        card.paste(img, (x_img, y_img))
        # 图片底部渐变遮罩
        for y in range(IMG_H - 100, IMG_H):
            alpha = (y - (IMG_H - 100)) / 100.0
            r = int(255 * alpha + color[0] * (1 - alpha))
            g = int(255 * alpha + color[1] * (1 - alpha))
            b = int(255 * alpha + color[2] * (1 - alpha))
            draw.rectangle([PADDING, PADDING + y, WIDTH - PADDING, PADDING + y + 1], fill=(r, g, b))
    except Exception as e:
        print(f"图片加载失败: {product['img']} - {e}")
        draw.rectangle([PADDING, PADDING, WIDTH - PADDING, PADDING + IMG_H], fill=color)

    # 顶部彩色渐变条
    draw.rectangle([0, 0, WIDTH, 20], fill=color)

    cur_y = PADDING + IMG_H + 30

    # 编号圆角标签
    num_size = 90
    num_bb = draw.textbbox((0, 0), product["num"], font=font_num)
    num_w = num_bb[2] - num_bb[0]
    num_h = num_bb[3] - num_bb[1]
    num_x = PADDING
    num_y = cur_y
    draw_rounded_rect(draw, [num_x, num_y, num_x + num_w + 30, num_y + num_h + 16], 16, color)
    draw.text((num_x + 15, num_y + 8), product["num"], font=font_num, fill=(255, 255, 255))

    # 分类标签
    cat_bb = draw.textbbox((0, 0), product["category"], font=font_cat)
    cat_w = cat_bb[2] - cat_bb[0]
    cat_x = num_x + num_w + 45
    cat_y = cur_y + (num_h + 16 - (cat_bb[3] - cat_bb[1])) // 2 - 4
    draw_rounded_rect(draw, [cat_x, cat_y, cat_x + cat_w + 24, cat_y + (cat_bb[3] - cat_bb[1]) + 12], 10, (240, 240, 245))
    draw.text((cat_x + 12, cat_y + 6), product["category"], font=font_cat, fill=color)

    # 价格标签
    price_bb = draw.textbbox((0, 0), product["price_note"], font=font_price)
    price_w = price_bb[2] - price_bb[0]
    price_x = WIDTH - PADDING - price_w - 10
    price_y = cur_y
    draw_rounded_rect(draw, [price_x, price_y, price_x + price_w + 20, price_y + price_bb[3] - price_bb[1] + 16], 12, color)
    draw.text((price_x + 10, price_y + 8), product["price_note"], font=font_price, fill=(255, 255, 255))

    cur_y += max(num_h + 16, price_bb[3] - price_bb[1] + 16) + 25

    # 标题
    title_bb = draw.textbbox((0, 0), product["title"], font=font_title)
    if title_bb[2] > WIDTH - 2 * PADDING:
        # 拆行
        lines = []
        words = product["title"].split("：")
        cur_line = ""
        for chunk in words:
            if draw.textlength(cur_line + "：" + chunk, font=font_title) <= WIDTH - 2 * PADDING:
                cur_line = cur_line + "：" + chunk if cur_line else chunk
            else:
                if cur_line:
                    lines.append(cur_line)
                cur_line = chunk
        if cur_line:
            lines.append(cur_line)
        for line in lines:
            draw.text((PADDING, cur_y), line, font=font_title, fill=(30, 30, 30))
            cur_y += (title_bb[3] - title_bb[1]) + 8
    else:
        draw.text((PADDING, cur_y), product["title"], font=font_title, fill=(30, 30, 30))
        cur_y += (title_bb[3] - title_bb[1]) + 8

    # 副标题
    draw.text((PADDING, cur_y), product["subtitle"], font=font_subtitle, fill=color)
    cur_y += (draw.textbbox((0, 0), product["subtitle"], font=font_subtitle)[3]) + 20

    # 分隔线
    draw.line([(PADDING, cur_y), (WIDTH - PADDING, cur_y)], fill=(220, 220, 230), width=2)
    cur_y += 25

    # 适用人群
    suitable_label = "「适用人群」"
    draw.text((PADDING, cur_y), suitable_label, font=font_label, fill=color)
    draw.text((PADDING + draw.textlength(suitable_label, font=font_label) + 8, cur_y), product["suitable"], font=font_suitable, fill=(100, 100, 100))
    cur_y += 45

    # 商品介绍
    desc_lines = []
    words = product["desc"]
    cur_line = ""
    max_w = WIDTH - 2 * PADDING
    for ch in words:
        test = cur_line + ch
        if draw.textlength(test, font=font_desc) <= max_w:
            cur_line = test
        else:
            desc_lines.append(cur_line)
            cur_line = ch
    if cur_line:
        desc_lines.append(cur_line)
    for line in desc_lines:
        draw.text((PADDING, cur_y), line, font=font_desc, fill=(60, 60, 60))
        cur_y += (draw.textbbox((0, 0), line, font=font_desc)[3]) + 8
    cur_y += 15

    # 亮点标题
    draw.text((PADDING, cur_y), "✨ 商品亮点", font=font_label, fill=color)
    cur_y += 45

    # 亮点列表
    for i, hl in enumerate(product["highlights"]):
        bullet = f"{i+1}. "
        draw.text((PADDING, cur_y), bullet, font=font_highlight, fill=color)
        draw.text((PADDING + draw.textlength(bullet, font=font_highlight), cur_y), hl, font=font_highlight, fill=(50, 50, 50))
        cur_y += (draw.textbbox((0, 0), hl, font=font_highlight)[3]) + 12

    cur_y += 20
    # 标签
    tag_y_start = cur_y
    tag_x = PADDING
    for tag in product["tags"]:
        tag_bb = draw.textbbox((0, 0), f"#{tag}", font=font_tag)
        tag_w = tag_bb[2] - tag_bb[0] + 20
        tag_h = tag_bb[3] - tag_bb[1] + 10
        if tag_x + tag_w > WIDTH - PADDING:
            tag_x = PADDING
            tag_y_start += tag_h + 10
        draw_rounded_rect(draw, [tag_x, tag_y_start, tag_x + tag_w, tag_y_start + tag_h], 8, (245, 245, 250))
        draw.text((tag_x + 10, tag_y_start + 5), f"#{tag}", font=font_tag, fill=(120, 120, 130))
        tag_x += tag_w + 12

    return card


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total_h = 0
    cards = []
    for product in PRODUCTS:
        print(f"生成卡片: {product['num']} - {product['title'][:20]}...")
        card = make_product_card(product)
        cards.append(card)

    # 合成完整长图
    full_h = sum(c.height for c in cards) + GAP * (len(cards) - 1)
    full_img = Image.new('RGB', (WIDTH, full_h), (255, 255, 255))
    cur_y = 0
    for i, card in enumerate(cards):
        full_img.paste(card, (0, cur_y))
        if i < len(cards) - 1:
            # 隔断：彩色分割线
            sep_color = hex2rgb(PRODUCTS[i]["color"])
            for sy in range(cur_y + card.height, cur_y + card.height + GAP // 2):
                for sx in range(0, WIDTH):
                    alpha = 1.0
                    r, g, b = sep_color
                    full_img.putpixel((sx, sy), (r, g, b))
        cur_y += card.height + GAP

    full_path = f"{OUT_DIR}/product_card_full.jpg"
    full_img.save(full_path, "JPEG", quality=92)
    print(f"✅ 完整长图已保存: {full_path} ({full_img.width}x{full_img.height})")

    # 5等份裁剪
    slice_h = full_h // 5
    slice_paths = []
    for i in range(5):
        top = i * slice_h
        bottom = (i + 1) * slice_h if i < 4 else full_h
        slice_img = full_img.crop((0, top, WIDTH, bottom))
        slice_path = f"{OUT_DIR}/product_slice_{i+1}.jpg"
        slice_img.save(slice_path, "JPEG", quality=90)
        slice_paths.append(slice_path)
        print(f"  裁剪 {i+1}/5: {slice_path}")

    print("\n✅ 全部完成！")
    print(f"全图: {full_path}")
    for sp in slice_paths:
        print(f"切片: {sp}")


if __name__ == "__main__":
    main()
