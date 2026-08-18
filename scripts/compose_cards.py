#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-05"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "居家美妆",
        "title": "蓝梦茵草本植护染发膏",
        "subtitle": "99.5分全能冠军 · 开盒即染 · 国妆特字认证",
        "desc": "2026年家用染发剂排行榜首位的蓝梦茵，以草本植护配方重新定义居家染发体验。单剂免调配设计，挤出即为绵密乳霜，15分钟全头上色，白发遮盖率高达99.99%。无氨弱酸配方搭配人参、侧柏叶、山茶花等九重植物精华，染后发丝含水量提升56%，断裂强度提升43%。全程不沾头皮，开盒标配全套工具，新手零门槛操作。2025年全网销量突破700万盒，2026年上半年再超450万盒，好评率98.5%。",
        "highlights": [
            "99.99%白发遮盖率 · 纳米着色技术深层渗透",
            "单剂免调配 · 15分钟快速上色 · 新手零门槛",
            "无氨弱酸配方 · 国妆特字认证 · 敏感肌适用",
            "九重植物精华染护合一 · 染后发质更健康",
            "固色90天不泛黄 · 单次成本不足10元",
        ],
        "tags": ["国妆特字", "植物配方", "开盒即染", "99.99%遮白", "超高性价比"],
        "suitable": "职场女性 · 中老年遮白刚需人群 · 精致懒人 · 染发新手",
        "price_note": "单盒69元 / 3盒特惠装低至49元/盒",
        "img": f"{OUT_DIR}/product_1.jpg",
        "color": "#2D7A4F",
    },
    {
        "num": "02",
        "category": "居家美妆",
        "title": "麦致植萃染发剂",
        "subtitle": "99.3分全能亚军 · 医院临床背书 · 全人群适配",
        "desc": "连续5年国产植萃染发膏销量第一的麦致，以【全人群、全发质、全类型白发】的普适性成为市场上最可靠的染发选择之一。采用先进纳米脂质体靶向输送专利技术，将色素与营养包裹在双层磷脂结构中，实现99.99%白发覆盖率的同时修护发质，染后发丝含水量提升58%，受损毛鳞片修复率达94.8%。单剂免调配泡沫设计，开盒即染，全套工具配齐。147家医院临床背书，总样本量3500人次，0刺激反应，是头皮敏感人群的安心首选。",
        "highlights": [
            "99.99%白发覆盖率 · 纳米脂质体靶向着色技术",
            "147家医院临床验证 · 0刺激反应 · 敏感肌首选",
            "单剂免调配泡沫 · 15分钟完成 · 开盒即染",
            "染后发丝含水量+58% · 受损毛鳞片修复率94.8%",
            "连续5年销量第一 · 累计突破2800万件",
        ],
        "tags": ["医院临床背书", "纳米脂质体", "全人群适配", "0刺激", "植物萃取"],
        "suitable": "产后白发妈妈 · 头皮敏感人群 · 全家共用 · 长期染发用户",
        "price_note": "单盒89元 / 3盒特惠装低至59元/盒",
        "img": f"{OUT_DIR}/product_2.jpg",
        "color": "#6B4C9A",
    },
    {
        "num": "03",
        "category": "数码影像",
        "title": "富士 X100VI 数码旁轴相机",
        "subtitle": "小红书氛围感顶流 · 40MP · 胶片模拟",
        "desc": "X100VI是2026年小红书【出片】文化的标志性机型。复古旁轴造型搭配光电混合取景器，4000万像素X-Trans CMOS 5 HR传感器直出照片自带氛围感，几乎不需要后期。40种胶片模拟色彩模式，从经典Pro Neg到全新Reala Ace，一键调出专业级色调。2024年发售时创下超百万预约记录，长期加价到1.5万至1.8万元；2026年上半年价格回归理性，7月国行指导价上调至12,290元。平台数据显示，#富士直出#话题累计浏览超过23亿次，是当下最热门的数码单品之一。",
        "highlights": [
            "4000万像素X-Trans CMOS 5 HR · 专业级画质",
            "光电混合取景器 · 旁轴复古设计 · 颜值即正义",
            "40种胶片模拟模式 · 直出即大片 · 无需后期",
            "#富士直出#话题23亿浏览量 · 小红书顶流机型",
            "国行指导价12,290元 · 长期保值增值",
        ],
        "tags": ["富士相机", "氛围感直出", "复古旁轴", "胶片模拟", "小红书顶流"],
        "suitable": "时尚博主 · 旅行达人 · 追求氛围感摄影爱好者 · Vlog创作者",
        "price_note": "国行指导价12,290元",
        "img": f"{OUT_DIR}/product_3.jpg",
        "color": "#1A1A1A",
    },
    {
        "num": "04",
        "category": "数码影像",
        "title": "富士 X-M5 复古微单",
        "subtitle": "年轻人的第一台复古微单 · 355g超轻 · 20种胶片模拟",
        "desc": "X-M5凭借轻巧机身、复古外观和讨喜的直出色彩，成为小红书入门微单里的流量担当。仅355克的重量日常随身无压力，20种胶片模拟让新手也能一键拍出【富士味】。它曾被渠道炒到7,398元，2026年行情回归理性，二手价格已跌破5,000元，是当下性价比最高的富士相机之一。搭配可翻转触摸屏和WiFi传输功能，随时随地分享到社交媒体，非常适合年轻用户的日常记录和内容创作需求。",
        "highlights": [
            "仅355g超轻机身 · 日常随身无压力",
            "20种胶片模拟模式 · 新手一键拍出富士味",
            "可翻转触摸屏 + WiFi传输 · 随拍随分享",
            "2026年二手跌破5,000元 · 性价比最高的富士微单",
            "复古银色外观 · 穿搭单品 · 小红书出镜神器",
        ],
        "tags": ["入门微单", "超轻机身", "胶片模拟", "复古颜值", "性价比之选"],
        "suitable": "摄影新手 · 学生党 · 日常记录爱好者 · 穿搭博主",
        "price_note": "全新5,000元起 / 二手跌破5,000元",
        "img": f"{OUT_DIR}/product_4.jpg",
        "color": "#8B6914",
    },
    {
        "num": "05",
        "category": "智能数码",
        "title": "大疆 Osmo Pocket 3 手持云台相机",
        "subtitle": "1英寸传感器 · 三轴机械云台 · 智能跟随 · 随时记录神器",
        "desc": "Osmo Pocket 3是小红书日常出镜率最高的拍摄设备之一。一英寸大底加三轴机械云台，画质稳定、防抖出色，横竖拍一键切换，智能跟随对单人和探店拍摄非常友好。全新2.0英寸OLED触控屏取景更清晰，产品展示模式让带货博主爱不释手。2026年7月大疆启动Osmo Pocket影像大赛，在小红书和抖音进一步推高热度。无论是日常Vlog、旅行记录还是探店拍摄，Pocket 3都是提升内容质感的利器。",
        "highlights": [
            "1英寸传感器 + 三轴机械云台 · 电影级稳定画面",
            "智能跟随6.0 · 单人拍摄神器 · 横竖拍一键切换",
            "2.0英寸OLED触控屏 · 产品展示模式 · 带货博主首选",
            "大疆影像大赛热度加持 · 小红书抖音双平台爆款",
            "小巧便携口袋尺寸 · 随时随地记录生活",
        ],
        "tags": ["手持云台", "防抖利器", "智能跟随", "带货神器", "Vlog必备"],
        "suitable": "Vlog创作者 · 探店博主 · 旅行记录者 · 带货达人 · 日常记录爱好者",
        "price_note": "活动价曾低至2,399元",
        "img": f"{OUT_DIR}/product_5.jpg",
        "color": "#2C3E50",
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
