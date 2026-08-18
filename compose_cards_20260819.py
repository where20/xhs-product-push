#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-19"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "厨房神器",
        "title": "免翻面+可视化！九阳6L空气炸锅国补后185元",
        "subtitle": "双热源免翻面 · 高清可视窗口 · 0涂层304不锈钢 · 1700W大功率",
        "desc": "想做炸鸡薯条又怕油烟？九阳这款6L可视空气炸锅帮你搞定！高清透视窗实时观察食物状态，不用反复开盖确认，双热源包裹式加热真正免翻面。0涂层304不锈钢内胆健康无涂层脱落风险，1700W大功率脱脂率提升51%，做出来外酥里嫩还少油。国家补贴叠加活动最低185元起，性价比拉满，厨房小白闭眼入！",
        "highlights": [
            "6L大容量：整鸡、大份食材一锅搞定，3-6人家庭适用",
            "高清可视窗口：随时观察食材状态，烹饪全程可视化",
            "双热源免翻面：上下双热源包裹加热，无需中途翻面",
            "0涂层304不锈钢内胆：健康无涂层脱落风险，耐用好清洗",
            "1700W大功率+51%脱脂率：快速锁汁少油烟，健康低脂",
        ],
        "tags": ["空气炸锅", "厨房神器", "健康烹饪", "国补好价", "免翻面"],
        "suitable": "厨房小白 · 减脂人群 · 三代同堂家庭 · 健康饮食爱好者",
        "price_note": "国补后185-339元（规格不同）",
        "img": f"{OUT_DIR}/orig_product_1.jpg",
        "color": "#FF6B35",
    },
    {
        "num": "02",
        "category": "早餐神器",
        "title": "免手洗！九阳1.5L破壁机打完豆浆自动清洗",
        "subtitle": "高压自动清洗+热风烘干 · 316钛钢0涂层 · 12小时预约",
        "desc": "破壁机用完清洗太麻烦？九阳免手洗破壁机帮你解放双手！一键高压喷洗+热风烘干，全程自动完成，做完豆浆米糊不用沾手。1.5L黄金容量适合3-6人家庭，316钛钢0涂层内胆安全健康，预约12小时功能让早餐更从容。618活动叠加国补，到手299元起，堪称小家电里的性价比之王！",
        "highlights": [
            "免手洗黑科技：一键高压清洗+热风烘干，做完不用沾手",
            "1.5L黄金容量：适合3-6人家庭，一次满足全家量",
            "316钛钢0涂层内胆：健康无涂层脱落，母婴级安全",
            "12小时预约+4小时保温：睡前预约，起床就有热豆浆",
            "多功能菜单：豆浆、米糊、辅食、果汁、浓汤一键搞定",
        ],
        "tags": ["破壁机", "免手洗", "厨房电器", "国补好价", "早餐神器"],
        "suitable": "上班族早餐党 · 母婴家庭 · 注重健康饮食人群 · 懒人厨房",
        "price_note": "国补后299-1599元（不同型号规格）",
        "img": f"{OUT_DIR}/orig_product_2.jpg",
        "color": "#E53935",
    },
    {
        "num": "03",
        "category": "个护电器",
        "title": "徕芬高速吹风机SE国补后164元！负离子护发",
        "subtitle": "11万转高速无刷电机 · 2亿/cm³负离子 · 学生党平替戴森",
        "desc": "戴森太贵下不去手？徕芬SE让你用1/3价格体验高速吹风！11万转无刷电机带来21.5米/秒风速，2分钟速干长发不累手腕。2亿负离子浓度减少毛躁，智能恒温50次/秒校准风温，不烫头皮。噪音仅59dB不扰人，裸重390g超轻巧。国补后164元起，学生党通勤党闭眼入，告别毛躁狮王头！",
        "highlights": [
            "11万转高速无刷电机：21.5米/秒风速，2分钟速干长发",
            "2亿/cm³负离子：减少毛躁静电，吹完顺滑有光泽",
            "智能恒温50次/秒：精准控温不烫头皮，护发更安全",
            "59dB静音设计：图书馆级安静，早晚使用不扰人",
            "390g超轻裸重：长久举吹不累手腕，长发星人福音",
        ],
        "tags": ["高速吹风机", "负离子护发", "徕芬", "学生党", "国补好价"],
        "suitable": "长发女生 · 学生党 · 注重护发人群 · 追求高性价比用户",
        "price_note": "国补后164-429元（SE/SE 2/Swift 3等型号）",
        "img": f"{OUT_DIR}/orig_product_3.jpg",
        "color": "#FF80AB",
    },
    {
        "num": "04",
        "category": "生活品质",
        "title": "摩飞全自动咖啡机705元！冰咖热萃研磨一体",
        "subtitle": "冰咖快速萃取 · 全自动研磨系统 · 在家实现咖啡自由",
        "desc": "每天外卖咖啡花掉大几十？摩飞这台全自动咖啡机让你把咖啡馆搬回家！冰咖快速萃取+热饮一键制作，内置精准温控和高密研磨系统，还原现磨咖啡的香醇口感。研磨浓度3档可调，冷热双模式适配四季，全自动操作省心省力。外形复古高颜值，放在餐边柜上就是一道风景。京东活动705元起，比每天买咖啡更划算！",
        "highlights": [
            "冰咖热萃双模式：冰咖啡快速萃取+热饮一键制作，四季适配",
            "全自动研磨系统：内置高密磨豆器，现磨现萃保留香气",
            "3档浓度可调：满足不同口味偏好，浓淡由你掌控",
            "精准温控技术：92℃黄金萃取温度，每杯都是好风味",
            "复古高颜值设计：小户型友好，餐边柜颜值担当",
        ],
        "tags": ["咖啡机", "摩飞", "家居好物", "咖啡自由", "高颜值"],
        "suitable": "咖啡爱好者 · 小资白领 · 居家办公人群 · 追求生活仪式感",
        "price_note": "京东活动705-820元",
        "img": f"{OUT_DIR}/orig_product_4.jpg",
        "color": "#4E342E",
    },
    {
        "num": "05",
        "category": "居家清洁",
        "title": "万必洁多功能清洁膏7元！一罐搞定全屋清洁",
        "subtitle": "瓷砖不锈钢皮革通用 · 温和无刺激配方 · 小白鞋锅底全能擦",
        "desc": "清洁剂买了一堆柜子都塞满了？万必洁多功能清洁膏一罐顶十瓶！适用于瓷砖、不锈钢、皮革、小白鞋、锅底等多种材质，温和无刺激配方不伤器具表面。深层渗透瓦解顽固水垢油渍，轻轻一擦焕然一新。7元起的价格堪称年度性价比天花板，家庭主妇/主夫必备神器，囤一次用半年！",
        "highlights": [
            "一罐多能：瓷砖、不锈钢、皮革、小白鞋、锅底通用",
            "温和无刺激配方：不伤器具表面，母婴家庭放心用",
            "深层渗透瓦解：顽固水垢、油渍、黄渍一抹即净",
            "7元起超低价：花小钱解决大问题，性价比天花板",
            "小巧便携不占地：厨房一个、卫生间一个刚刚好",
        ],
        "tags": ["清洁好物", "多功能清洁膏", "平价神器", "家居收纳", "生活妙招"],
        "suitable": "家庭主妇/主夫 · 租房党 · 追求高效清洁人群 · 囤货达人",
        "price_note": "天猫活动7-35元（多规格可选）",
        "img": f"{OUT_DIR}/orig_product_5.jpg",
        "color": "#43A047",
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

    print(f"\n\u1f389 \u5b8c\u6210\uff01\u5171\u751f\u62101\u5f20\u5168\u56fe + {len(PRODUCTS)}\u5f20\u5207\u7247")


if __name__ == "__main__":
    main()
