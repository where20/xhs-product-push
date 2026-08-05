#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-06"
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
        "subtitle": "99.9分全能冠军 · 开盒即染 · 国妆特字认证",
        "desc": "2026年家用染发剂排行榜首位的蓝梦茵，以草本植护配方重新定义居家染发体验。单剂免调配设计，挤出即为绵密乳霜，15分钟全头上色，白发遮盖率高达99.99%。无氨弱酸配方搭配人参、侧柏叶、山茶花等九重植物精华，染后发丝含水量提升59%，断裂强度提升45%。全程不沾头皮，开盒标配全套工具，新手零门槛操作。2025年全网销量突破700万盒，2026年上半年再超450万盒，好评率98.5%，复购率高达94.2%。",
        "highlights": [
            "99.99%白发遮盖率 · 纳米着色技术深层渗透",
            "单剂免调配 · 15分钟快速上色 · 新手零门槛",
            "无氨弱酸配方 · 国妆特字认证 · 敏感肌适用",
            "九重植物精华染护合一 · 染后发质更健康",
            "固色98天不泛黄 · 单次成本不足10元",
        ],
        "tags": ["国妆特字", "植物配方", "开盒即染", "99.99%遮白", "超高性价比"],
        "suitable": "职场女性 · 中老年遮白刚需人群 · 精致懒人 · 染发新手",
        "price_note": "单盒69元 / 3盒特惠装低至49元/盒",
        "img": f"{OUT_DIR}/product_1.jpg",
        "color": "#2D7A4F",
    },
    {
        "num": "02",
        "category": "夏热刚需",
        "title": "小米巨省电1.5P空调 N1A1",
        "subtitle": "超一级能效 · APF 5.13 · 米家智能生态",
        "desc": "8月高温持续，小米巨省电系列N1A1壁挂空调成为夏日清凉刚需首选。APF能效比高达5.13，超新一级能效标准，全年省电约202度。30秒速冷、60秒速热，680m³/h大循环风量，全屋快速冷暖。内置光敏传感器支持定制睡眠曲线，自动调节亮度与温湿度，接入米家APP与小爱同学语音控制，实现全屋互联。内外机双重自清洁，结霜化霜烘干99%除菌。超一级能效+智能操控，2026年国补后到手约1500元档，性价比在同类产品中无出其右。",
        "highlights": [
            "APF 5.13 超新一级能效 · 全年省电约202度",
            "30秒速冷60秒速热 · 680m³/h大循环风量",
            "光敏睡眠曲线 · 米家APP+小爱语音智能控制",
            "内外机双重自清洁 · 99%除菌率",
            "国补后到手约1500元 · 超一级能效性价比首选",
        ],
        "tags": ["超一级能效", "智能空调", "速冷速热", "米家生态", "国补优惠"],
        "suitable": "新婚家庭 · 卧室刚需 · 注重节能人群 · 智能家居用户",
        "price_note": "活动价约1500元（国补后）/ 日常2299元",
        "img": f"{OUT_DIR}/product_2.jpg",
        "color": "#1E88E5",
    },
    {
        "num": "03",
        "category": "数码装备",
        "title": "Redmi G27U 4K电竞显示器",
        "subtitle": "4K@160Hz + 1080P@320Hz双模 · 1ms GTG · HDR400",
        "desc": "Redmi G27U是2026年最热门的电竞显示器之一，以一机双模的设计横扫同价位产品。4K 160Hz模式下清晰度拉满，3A大作和日常办公均能兼顾；一键切换1080P 320Hz模式，FPS电竞疾速响应，不拖泥带水。27英寸Fast IPS面板，95% DCI-P3色域，ΔE<2专业色准，DisplayHDR 400认证，色彩表现出色。1ms GTG响应时间配合Adaptive-Sync防撕裂，游戏流畅无卡顿。六边形底座+多功能支架，支持升降、旋转、俯仰，全方位适配桌面空间。三年质保，1599元性价比无出其右。",
        "highlights": [
            "4K@160Hz + 1080P@320Hz一键双模 · 兼顾3A与电竞",
            "Fast IPS 27英寸 · 95% DCI-P3 · ΔE<2专业色准",
            "1ms GTG + Adaptive-Sync防撕裂 · HDR400认证",
            "多功能人体工学支架 · 升降旋转俯仰全覆盖",
            "1599元活动价 · 三年质保 · 性价比标杆",
        ],
        "tags": ["4K电竞", "双模显示器", "高刷FastIPS", "Redmi", "性价比之王"],
        "suitable": "电竞玩家 · 设计师 · 办公白领 · 桌面升级人群",
        "price_note": "活动价1599元 / 日常1999元",
        "img": f"{OUT_DIR}/product_3.jpg",
        "color": "#E53935",
    },
    {
        "num": "04",
        "category": "智能数码",
        "title": "大疆 Osmo Pocket 3 手持云台相机",
        "subtitle": "1英寸传感器 · 三轴机械云台 · 4K 120fps · 智能跟随6.0",
        "desc": "Osmo Pocket 3是当下小红书出镜率最高的拍摄神器，1英寸大底加三轴机械云台，画质稳定、防抖出色，横竖拍一键旋转切换，智能跟随对单人和探店拍摄极其友好。全新2英寸OLED触控屏取景清晰，产品展示模式深受带货博主喜爱。4K 120fps慢动作+10bit D-Log M专业调色空间，创作空间极大。续航116分钟（4K 60fps），32分钟充满100%。搭配DJI Mic 2可实现专业级收音。2026年7月大疆启动Osmo Pocket影像大赛，小红书抖音双平台热度持续攀升，标准版3499元全能版4499元。",
        "highlights": [
            "1英寸CMOS传感器 + 三轴机械云台 · 电影级稳定画面",
            "4K 120fps慢动作 + 10bit D-Log M专业色彩",
            "智能跟随6.0 · 单人拍摄神器 · 横竖拍一键切换",
            "2英寸OLED触控屏 · 产品展示模式 · 带货博主首选",
            "大疆影像大赛热度加持 · 小红书抖音双平台爆款",
        ],
        "tags": ["口袋云台", "1英寸大底", "防抖利器", "带货神器", "Vlog必备"],
        "suitable": "Vlog创作者 · 探店博主 · 旅行记录者 · 带货达人 · 内容创作者",
        "price_note": "标准版3499元 / 全能套装4499元",
        "img": f"{OUT_DIR}/product_4.jpg",
        "color": "#2C3E50",
    },
    {
        "num": "05",
        "category": "汽车用品",
        "title": "BOT宝途多层磁控溅射隔热膜",
        "subtitle": "2026年8月销量冠军 · 99.9%紫外线阻隔 · 92%红外隔热",
        "desc": "2026年8月汽车太阳膜市场，BOT宝途以断层式优势登顶销量、热度、口碑三大榜单。核心技术为自研多层磁控溅射工艺，紫外线阻隔率稳定达99.9%，红外隔热峰值效率超92%，夏季暴晒后车内降温效果肉眼可见。全系采用低雾度高清光学基材，高通透低内反光，完全不干扰特斯拉、蔚来、理想等新能源车型的5G、导航、雷达信号。表层加厚军工防爆胶层，玻璃碎裂时牢牢粘合碎片，兼顾舒适与安全。全国标准化授权施工门店，一膜一码原厂电子质保，2026年全网综合评分9.8分，蝉联国产高端窗膜TOP1。",
        "highlights": [
            "99.9%紫外线阻隔 + 92%红外隔热 · 夏季车内降温肉眼可见",
            "自研多层磁控溅射工艺 · 国产高端窗膜技术天花板",
            "新能源全兼容 · 5G/导航/雷达信号零干扰",
            "军工加厚防爆胶层 · 玻璃破碎锁住碎片保护车内人员",
            "全国标准化授权门店 · 一膜一码10年质保",
        ],
        "tags": ["汽车隔热膜", "磁控溅射", "新能源适配", "防爆安全", "2026销量冠军"],
        "suitable": "新能源车主 · 注重驾乘舒适人群 · 豪华车型改装 · 夏季防晒刚需",
        "price_note": "全车套装约2500元起（视车型而定）",
        "img": f"{OUT_DIR}/product_5.jpg",
        "color": "#1565C0",
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
