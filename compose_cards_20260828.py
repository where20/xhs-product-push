#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-28"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "教学装备",
        "title": "老师开学第一件！西圣Bee扩音器，239元解决嗓子嘶哑难题",
        "subtitle": "HiTone人声增益 · D类旗舰DSP · 360°环向扩声 · 2.4G+蓝牙双无线",
        "desc": "新学期开学，老师们最怕的就是连续上课嗓子发炎。西圣Bee小蜜蜂扩音器，239元解决大教室后排听不清、老师连续上课嗓子嘶哑两大痛点。搭载旗舰级D类高增益DSP功放芯片，16芯全频发声单元配合360°广角环向扩声结构，音量洪亮不刺耳，大教室最后一排也能听得清清楚楚。自研HiTone™人声动态增益引擎，精准识别老师声线，说话不用刻意提高音量，嗓子轻松了上课反而更从容。全链路抗啸叫算法从根源杜绝刺耳噪音，2.4G+蓝牙5.4双无线模式，30米稳定连接，课堂来回走动不断联。领夹麦仅20g，全天佩戴肩膀无负担。Type-C快充8小时续航，一节课接一节课不用频繁充电。",
        "highlights": [
            "D类高增益DSP旗舰芯片，16芯全频发声，360°环向扩声，声音洪亮不刺耳",
            "HiTone™人声动态增益，精准还原人声，老师不用扯着嗓子讲课",
            "全链路六重抗啸叫算法，复杂教室环境零啸叫，课堂全程稳定",
            "2.4G+蓝牙5.4双无线，30米稳定不断联，走动讲课不受限",
            "领夹麦20g全天佩戴无负担，8小时续航Type-C快充，课堂无断电焦虑"
        ],
        "tags": ["扩音器", "小蜜蜂", "西圣Bee", "教师必备", "开学好物", "护嗓神器", "教学装备"],
        "suitable": "老师 · 讲师 · 培训师 · 导游 · 需要长时间讲话人群",
        "price_note": "参考价¥239",
        "img": f"{OUT_DIR}/product_1.jpg",
        "color": "#E74C3C",
    },
    {
        "num": "02",
        "category": "学习工具",
        "title": "课本笔记不想抄？惠普便携扫描仪，399元把纸质资料装进口袋",
        "subtitle": "1200DPI光学分辨率 · 无线直传手机 · 自动纠偏裁边 · 多页PDF合并",
        "desc": "开学后大量课本、课件、试卷需要整理，手抄太费时间，拍照又不便于后期编辑。惠普便携扫描仪，399元解决纸质资料数字化难题，无需连接电脑，机身可直接完成扫描并保存到存储卡或无线传输到手机。1200DPI光学分辨率，手写字迹、试卷小字都能清晰识别。多页合并输出PDF功能，完整保存老师布置的整章练习题。自动纠偏+自动裁边功能，歪斜纸张自动修正画面，扫描效果比手机拍照整齐十倍。机身小巧可放入书包，图书馆自习直接扫描课本页面，不用反复翻找。无线同步手机后，课件笔记直接整理成电子文档，复习效率翻倍。",
        "highlights": [
            "1200DPI高分辨率，手写字迹、试卷小字清晰识别，还原度极高",
            "无线扫描直传手机，扫描文件直接保存到手机，无需电脑中转",
            "多页PDF合并输出，老师整章练习题完整保存，复习时不用翻原书",
            "自动纠偏+自动裁边，歪斜纸张自动修正，扫描效果比拍照整齐",
            "机身小巧放入书包，图书馆、教室随时用，碎片时间整理资料效率翻倍"
        ],
        "tags": ["扫描仪", "惠普", "便携扫描", "开学必备", "学习工具", "笔记整理", "无纸化"],
        "suitable": "学生 · 考研党 · 图书馆常客 · 资料整理需求者",
        "price_note": "参考价¥399",
        "img": f"{OUT_DIR}/product_2.jpg",
        "color": "#3498DB",
    },
    {
        "num": "03",
        "category": "创意数码",
        "title": "打印照片不再怕废片！小米口袋照片打印机Pro，599元留住开学记忆",
        "subtitle": "热升华专业打印 · 自动覆膜防水 · AR视频照片 · 打印前可修图确认",
        "desc": "新学期新开始，总有些珍贵瞬间想要永久保存。小米口袋照片打印机Pro，599元让开学季的每个重要时刻变成可以触摸的实体回忆。热升华专业打印技术，无需墨盒墨水，打印过程自动覆膜，防水防刮不易褪色，保存十年颜色依旧鲜艳。313×313DPI高清分辨率，1670万色域256级色阶过渡，色彩还原细腻真实，人物肤色自然不偏色。AR视频照片功能，扫描照片即可播放关联视频，让静态画面动起来。打印前可以先在APP修图确认再打印，完全告别拍立得废片风险。23英寸背胶相纸，撕开即贴，轻松做手账装饰、宿舍照片墙。蓝牙5.2多人共享，社团活动现场打印送给同学，社交破冰神器。",
        "highlights": [
            "热升华无墨打印+自动覆膜，照片防水防刮不易褪色，保存十年依旧鲜艳",
            "313×313DPI高清分辨率，1670万色域256级色阶，色彩还原真实细腻",
            "AR视频照片：扫描静态照片即可播放关联视频，让回忆动起来",
            "打印前先修图再确认，完全避免拍立得废片风险，不浪费每一张相纸",
            "23英寸背胶相纸撕开即贴，手账装饰、宿舍照片墙随时创作"
        ],
        "tags": ["照片打印机", "小米", "口袋打印机", "开学好物", "创意数码", "手账神器", "回忆保存"],
        "suitable": "学生党 · 手账爱好者 · 摄影爱好者 · 礼物送礼需求",
        "price_note": "参考价¥599",
        "img": f"{OUT_DIR}/product_3.jpg",
        "color": "#9B59B6",
    },
    {
        "num": "04",
        "category": "生活好物",
        "title": "室友打鼾睡不着？南卡DeepSleep睡眠耳机，689元换一夜好眠",
        "subtitle": "3克零感佩戴 · 40dB三重降噪 · 睡眠模式自动停播 · 睡眠报告追踪",
        "desc": "宿舍生活作息不同，室友打鼾、楼道喧哗、空调噪音严重影响睡眠质量。南卡DeepSleep睡眠耳机，专为浅眠人群设计，689元换来整夜安宁。单耳仅重3克，6mm超薄声学结构，侧睡翻身零压迫，耳朵完全感觉不到它的存在。降噪与舒眠双引擎协同，物理隔音+主动降噪+白噪音三重方案，最高40dB降噪深度，把鼾声、车流、室友聊天全部过滤掉，只留安静陪伴入睡。专属APP睡眠模式，检测到入睡自动停止播放，不打扰深度睡眠，同时记录深睡浅睡比例和夜间醒转次数，生成睡眠报告让你对自己的睡眠质量心中有数。SuperSound OS 2.0声学系统，三频均衡耐听，听白噪音助眠一整夜也不会听觉疲劳。12小时单次续航+60小时充电盒总续航，一整晚不用起身充电。",
        "highlights": [
            "3克零感佩戴：6mm超薄结构，侧睡翻身零压迫，整晚佩戴耳朵不酸不胀",
            "降噪与舒眠双引擎，三重降噪方案，最高40dB降噪把鼾声噪音全部过滤",
            "睡眠模式智能感应，入睡自动停播，不打扰深度睡眠，更不浪费电量",
            "睡眠报告生成：深睡浅睡比例、夜间醒转次数、睡眠时长数据化追踪",
            "12小时单次续航+60小时总续航，一次充电撑一整周，起夜复习也不怕"
        ],
        "tags": ["睡眠耳机", "南卡", "降噪耳机", "宿舍神器", "失眠好物", "隔音耳机", "睡眠监测"],
        "suitable": "浅眠人群 · 宿舍党 · 失眠困扰者 · 对噪音敏感人群",
        "price_note": "参考价¥689",
        "img": f"{OUT_DIR}/product_4.jpg",
        "color": "#1ABC9C",
    },
    {
        "num": "05",
        "category": "学习照明",
        "title": "熄灯后刷题眼睛累？书客SKR1屏幕挂灯，289元拯救熄灯后学习体验",
        "subtitle": "AOT光路菱镜 · RG0无蓝光 · Ra97显色 · 红光舒缓 · 智能感光调光",
        "desc": "宿舍熄灯后，笔记本屏幕强光直射眼睛，台灯又照亮整张桌子打扰室友。书客SKR1屏幕挂灯，289元完美解决这个两难困境。挂灯挂在显示器上方，只照亮屏幕前的工作区域，手指键盘清晰可见，屏幕不反光，室友那边完全不受影响。紫光激发全光谱光源，RG0无蓝光等级，显色指数Ra98高度还原屏幕和书本真实色彩。内置红光舒缓模块，有效减轻长时间盯屏带来的眼部酸胀。智能感应环境亮度自动调光，桌面各处光线均匀无阴影，眼睛不疲劳学习效率更高。触控开关无极调光，从暖光到白光多档色温可调，熄灯后开最小档暖光刷题，眼睛舒服不刺眼。不占桌面空间，折叠拆装只需三秒，考研党、赶作业学生党必备。",
        "highlights": [
            "屏幕挂载不占桌面，只照亮工作区，熄灯后刷题不影响室友",
            "RG0无蓝光，紫光激发全光谱，显色指数Ra98，长时间用眼不酸不涩",
            "红光舒缓模块，屏幕前用眼疲劳有效减轻，考研党熬夜刷题眼睛不遭罪",
            "智能感光自动调光，桌面光线均匀无阴影，眼睛不用频繁调节焦距",
            "触控无极调光多档色温，暖光到白光一键切换，289元护眼性价比无敌"
        ],
        "tags": ["屏幕挂灯", "书客", "护眼灯", "熄灯神器", "学习照明", "宿舍好物", "考研党"],
        "suitable": "考研党 · 学生党 · 夜间学习者 · 长时间盯屏人群",
        "price_note": "参考价¥289",
        "img": f"{OUT_DIR}/product_5.jpg",
        "color": "#F39C12",
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
