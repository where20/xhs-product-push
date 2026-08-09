#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-10"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "数码家电",
        "title": "小米巨省电1.5P壁挂空调 N1A1",
        "subtitle": "超一级能效 · 极简百搭 · 夏日续命神器",
        "desc": "炎炎夏日，没有一台靠谱的空调简直活不下去！小米巨省电N1A1，1.5P黄金匹数正适合12-18㎡卧室或小客厅，超一级能效APF值远超国标，一整晚开着也花不了几度电，再也不心疼电费账单了！双排冷凝器加持，制冷速度更快、效果更稳；夜里开启睡眠模式，几乎听不到运转声，给你和家人一个安静舒适的夜晚。支持米家APP远程控制，下班路上提前开机，到家即享清凉！",
        "highlights": [
            "超一级能效，APF值5.13以上，变频节能省电王",
            "双排冷凝器+全直流变频压缩机，制冷快人一步",
            "睡眠模式噪音低至22dB(A)，图书馆级静音",
            "米家APP智能互联，支持小爱同学语音控制",
            "宽温域运行，-32℃极寒到60℃高温都稳得住",
        ],
        "tags": ["超省电", "智能家居", "静音", "高能效", "夏日必备"],
        "suitable": "新婚家庭 · 小户型业主 · 学生党租房 · 注重电费支出人群",
        "price_note": "活动价约1500元（国补后）/ 日常2299元",
        "img": f"{OUT_DIR}/product_1.jpg",
        "color": "#1E88E5",
    },
    {
        "num": "02",
        "category": "数码家电",
        "title": "Redmi G27U 4K电竞显示器",
        "subtitle": "4K 160Hz · 性价比之王 · 桌面党首选",
        "desc": "想给桌面来一次视觉升级，又不想花冤枉钱？Redmi G27U就是那个答案！27英寸4K分辨率搭配160Hz高刷新率，画面细腻程度和流畅度同时拉满，不管是修图剪视频还是打游戏，都能带来沉浸式视觉体验。显示器支持HDR400，亮暗层次更分明；支架可旋转可升降，找到最舒服的观看角度。它还配备双DP+双HDMI2.1全接口，接游戏机、接电脑、接主机全部搞定，桌面清爽一根线就够了。",
        "highlights": [
            "27英寸4K IPS面板，PPI高达163，显示细腻无颗粒感",
            "原生160Hz刷新率+1ms灰阶响应，游戏画面丝滑流畅",
            "HDR400认证，明暗细节更丰富，看电影修图都出彩",
            "双DP+双HDMI2.1全接口，接PC/游戏机/笔记本全兼容",
            "旋转升降人体工学支架，竖屏模式支持，程序员友好",
        ],
        "tags": ["4K高刷", "电竞屏", "高性价比", "多接口", "桌面升级"],
        "suitable": "电竞玩家 · 桌面美学爱好者 · 自媒体创作者 · 程序员",
        "price_note": "活动价约1599元 / 日常1999元",
        "img": f"{OUT_DIR}/product_2.jpg",
        "color": "#E53935",
    },
    {
        "num": "03",
        "category": "数码家电",
        "title": "Redmi Turbo 4 Pro 手机 16G+1T",
        "subtitle": "骁龙8S Gen4 · 7550mAh巨无霸电池 · 大容量神机",
        "desc": "手机存储永远不够用、续航焦虑天天有？Redmi Turbo 4 Pro 16G+1T版让你彻底和这些烦恼说拜拜！1TB海量存储，照片视频APP随便装，再也不用反复清理手机；7550mAh超大容量电池，满电出门一整天都不用带充电宝。骁龙8S Gen4处理器，性能对标旗舰，日常应用流畅无比，手游也能稳稳运行。全金属边框设计，质感直接拉高一档，拿在手里完全不像这个价位的机器！",
        "highlights": [
            "16GB+1TB超大存储组合，海量照片视频随心存",
            "7550mAh超大电池，续航焦虑彻底告别，一天一充绰绰有余",
            "骁龙8S Gen4处理器，8E同款架构，日常流畅游戏无压力",
            "全金属中框，质感出众，告别廉价塑料感",
            "国补后到手约2200元，同价位配置天花板",
        ],
        "tags": ["超大存储", "长续航", "高性能", "全金属机身", "大电池"],
        "suitable": "重度手机用户 · 游戏玩家 · 出差党 · 存储焦虑人群",
        "price_note": "16G+1T约2200元（国补后）/ 日常2699元",
        "img": f"{OUT_DIR}/product_3.jpg",
        "color": "#43A047",
    },
    {
        "num": "04",
        "category": "数码家电",
        "title": "大疆 Osmo Pocket 3 便携云台相机",
        "subtitle": "一英寸传感器 · 三轴云台 · Vlog创作者神器",
        "desc": "还在用手机拍Vlog，手持抖到怀疑人生？大疆Osmo Pocket 3来拯救你了！它搭载一英寸大底传感器，画质直接碾压手机；配合三轴机械云台，无论你怎么走动，画面稳如泰山。横竖拍一秒切换，智能跟随对单人和探店拍摄超级友好。机身巴掌大小，随手揣进口袋出门无压力。2026年小红书日常出镜率最高的拍摄设备之一，配上官方影像大赛的热度，现在入手正是好时机！",
        "highlights": [
            "一英寸传感器，弱光表现大幅提升，画质直逼专业相机",
            "三轴机械云台，物理防抖，走路拍摄画面依然平稳",
            "智能跟随6.0，单人拍摄也能精准锁定主角不跑焦",
            "横竖屏一键切换，适配抖音/小红书/微信视频号全平台",
            "巴掌大小仅179g，随身携带零压力，随时随地记录生活",
        ],
        "tags": ["云台防抖", "一英寸大底", "便携小巧", "Vlog神器", "智能跟随"],
        "suitable": "Vlog博主 · 旅行博主 · 探店达人 · 内容创作者",
        "price_note": "活动价约3499元 / 日常3999元",
        "img": f"{OUT_DIR}/product_4.jpg",
        "color": "#7B1FA2",
    },
    {
        "num": "05",
        "category": "健康零食",
        "title": "认养一头牛纯牛奶 200ml*16盒整箱",
        "subtitle": "A2β-酪蛋白 · 学生早餐必备 · 拼多多销冠",
        "desc": "每天早上给孩子/自己准备什么早餐？认养一头牛纯牛奶，专注品质牛奶的品牌，甄选优质奶源，牛奶口感醇厚、入口丝滑，是早餐桌和睡前一杯的常驻选手。200ml小盒装刚好一次一盒不浪费，整箱16盒全家共享或囤货都划算。作为拼多多常年热销榜常客，累计卖出数百万箱，口碑持续在线，好喝不贵，是真正的家庭刚需好物！",
        "highlights": [
            "甄选优质奶源，品质稳定，喝过的都说好",
            "200ml小盒装刚好一次一盒，避免开封浪费",
            "拼多多实时热销榜常客，累计销量数百万箱",
            "口感醇厚丝滑，早餐、睡前、运动后随时来一盒",
            "常温保存12个月，囤货无压力，保质期内喝完绰绰有余",
        ],
        "tags": ["家庭刚需", "早餐必备", "高销量", "口感醇厚", "性价比"],
        "suitable": "有娃家庭 · 注重早餐营养的上班族 · 学生党 · 送礼需求",
        "price_note": "整箱约39.9元 / 拼多多百亿补贴活动价",
        "img": f"{OUT_DIR}/product_5.jpg",
        "color": "#F57C00",
    },
]


def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", size)
        except:
            return ImageFont.load_default()


def hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_product_card(product):
    img = Image.open(product["img"]).convert("RGBA")
    scale = WIDTH / img.width
    new_h = int(img.height * scale)
    img = img.resize((WIDTH, new_h), Image.LANCZOS)

    card_h = CARD_H
    card = Image.new("RGBA", (WIDTH, card_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(card)

    # 商品图
    card.paste(img, (0, 0))

    # 渐变遮罩
    for i in range(80):
        alpha = int(255 * i / 80)
        overlay = Image.new("RGBA", (WIDTH, 1), (255, 255, 255, alpha))
        card.paste(overlay, (0, new_h - 80 + i))

    # 编号标签
    num_font = load_font(72)
    r, g, b = hex_to_rgb(product["color"])
    draw.rounded_rectangle([30, new_h + 20, 160, new_h + 110], radius=16, fill=(r, g, b, 230))
    draw.text((50, new_h + 25), f"#{product['num']}", font=num_font, fill=(255, 255, 255))

    # 分类标签
    cat_font = load_font(28)
    bbox = draw.textbbox((0, 0), product["category"], font=cat_font)
    tw = bbox[2] - bbox[0] + 24
    draw.rounded_rectangle([170, new_h + 40, 170 + tw, new_h + 90], radius=16, fill=(100, 100, 100, 220))
    draw.text((182, new_h + 48), product["category"], font=cat_font, fill=(255, 255, 255))

    # 商品标题
    title_font = load_font(60)
    draw.text((40, new_h + 120), product["title"], font=title_font, fill=(30, 30, 30))

    # 副标题
    sub_font = load_font(28)
    draw.text((40, new_h + 195), product["subtitle"], font=sub_font, fill=(100, 100, 100))

    # 分隔线
    sep_y = new_h + 245
    draw.line([(40, sep_y), (WIDTH - 40, sep_y)], fill=(220, 220, 220), width=2)

    # 描述文字（自动换行）
    desc_font = load_font(30)
    desc_text = product["desc"]
    words = list(desc_text)
    lines_desc = []
    current = ""
    for char in words:
        test = current + char
        bbox = draw.textbbox((0, 0), test, font=desc_font)
        if bbox[2] - bbox[0] > WIDTH - 80:
            lines_desc.append(current)
            current = char
        else:
            current = test
    if current:
        lines_desc.append(current)

    dy = sep_y + 20
    for line in lines_desc:
        draw.text((40, dy), line, font=desc_font, fill=(60, 60, 60))
        dy += 48

    # 核心亮点标题
    hl_y = dy + 20
    hl_title_font = load_font(34)
    draw.text((40, hl_y), "\u2726 核心亮点", font=hl_title_font, fill=(30, 30, 30))
    hl_y += 50

    # 亮点列表
    hl_font = load_font(28)
    for i, hl in enumerate(product["highlights"]):
        dot_x = 55
        dot_y = hl_y + 4
        cr, cg, cb = hex_to_rgb(product["color"])
        draw.ellipse([dot_x, dot_y, dot_x + 16, dot_y + 16], fill=(cr, cg, cb))
        draw.text((dot_x + 24, hl_y), f"{i+1}. {hl}", font=hl_font, fill=(50, 50, 50))
        hl_y += 50

    # 卖点标签
    tag_y = hl_y + 20
    tag_font = load_font(22)
    x_pos = 40
    for tag in product["tags"]:
        bbox = draw.textbbox((0, 0), tag, font=tag_font)
        tw = bbox[2] - bbox[0] + 20
        if x_pos + tw > WIDTH - 40:
            x_pos = 40
            tag_y += 45
        draw.rounded_rectangle([x_pos, tag_y, x_pos + tw, tag_y + 38], radius=19, fill=(242, 242, 244))
        draw.text((x_pos + 10, tag_y + 6), tag, font=tag_font, fill=(80, 80, 80))
        x_pos += tw + 12

    # 适合人群
    suy = tag_y + 55
    draw.text((40, suy), f"\u9002\u7528\u4eba\u7fa4\uff1a{product['suitable']}", font=hl_font, fill=(80, 80, 80))

    # 价格说明
    pricey = suy + 50
    price_font = load_font(34)
    draw.text((40, pricey), product["price_note"], font=price_font, fill=(cr, cg, cb))

    # 底部品牌栏
    bottom_y = card_h - 65
    draw.rectangle([0, bottom_y, WIDTH, card_h], fill=(242, 242, 247))
    brand_font = load_font(24)
    brand_text = f"\u4eac\u4e00\u597d\u7269\u63a8\u8350 \u00b7 {TODAY} \u00b7 \u5c0f\u7ea2\u4e66\u5546\u54c1\u56fe\u6587\u5e26\u8d27"
    bw = draw.textbbox((0, 0), brand_text, font=brand_font)[2]
    draw.text(((WIDTH - bw) // 2, bottom_y + 16), brand_text, font=brand_font, fill=(150, 150, 160))

    # 转RGB
    if card.mode == "RGBA":
        white = Image.new("RGB", card.size, (255, 255, 255))
        white.paste(card, mask=card.split()[3])
        return white
    return card


def main():
    # 顶部标题栏
    header_h = 110
    total_h = header_h + len(PRODUCTS) * (CARD_H + GAP)

    canvas = Image.new("RGB", (WIDTH, total_h), (255, 255, 255))

    # 顶部标题
    header = Image.new("RGB", (WIDTH, header_h), (30, 30, 30))
    hdraw = ImageDraw.Draw(header)
    hfont = load_font(52)
    hfont2 = load_font(28)
    t = "\U0001f4e6 \u4eca\u65e5\u597d\u7269\u63a8\u8350"
    tw = hdraw.textbbox((0, 0), t, font=hfont)[2]
    hdraw.text(((WIDTH - tw) // 2, 25), t, font=hfont, fill=(255, 255, 255))
    s = f"\u5c0f\u7ea2\u4e66\u66fc\u7396\u5e26\u8d27 \u00b7 \u6bcf\u65e5\u7cbe\u9009 {TODAY}"
    sw = hdraw.textbbox((0, 0), s, font=hfont2)[2]
    hdraw.text(((WIDTH - sw) // 2, 72), s, font=hfont2, fill=(180, 180, 180))
    canvas.paste(header, (0, 0))

    # 绘制每个商品卡片
    y_offset = header_h
    for i, product in enumerate(PRODUCTS):
        card = draw_product_card(product)
        canvas.paste(card, (0, y_offset))
        if i < len(PRODUCTS) - 1:
            gap = Image.new("RGB", (WIDTH, GAP), (245, 245, 245))
            canvas.paste(gap, (0, y_offset + CARD_H))
        y_offset += CARD_H + GAP
        print(f"\u2705 \u5546\u54c1 {i+1}: {product['title']}")

    # 保存全图
    full_path = f"{OUT_DIR}/product_card_full.jpg"
    canvas.save(full_path, "JPEG", quality=95)
    print(f"\n\u2705 \u5168\u56fe\u5df2\u4fdd\u5b58: {full_path}")

    # 裁剪5份
    for i in range(len(PRODUCTS)):
        sy = header_h + i * (CARD_H + GAP)
        slice_ = canvas.crop((0, sy, WIDTH, sy + CARD_H))
        sp = f"{OUT_DIR}/product_slice_{i+1}.jpg"
        slice_.save(sp, "JPEG", quality=88)
        print(f"\u2705 \u5207\u7247 {i+1}: {sp}")

    print(f"\n\U0001f389 \u5b8c\u6210\uff01\u5171\u751f\u62101\u5f20\u5168\u56fe + {len(PRODUCTS)}\u5f20\u5207\u7247")


if __name__ == "__main__":
    main()
