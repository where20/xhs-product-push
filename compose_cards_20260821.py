#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-21"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
FONT_PATH = "/System/Library/Fonts/STHeiti Light.ttc"
WIDTH = 1080
CARD_H = 3000
GAP = 20

# 5个商品数据
PRODUCTS = [
    {
        "num": "01",
        "category": "桌面好物",
        "title": "小米米家插线板20W快充版！新国标3孔+2A1C，宿舍桌面一个就够",
        "subtitle": "2A1C快充 · 新国标插孔 · 智能电流分配 · 750℃阻燃材质",
        "desc": "开学季宿舍桌面乱糟糟？充电头打架排不开？小米米家插线板20W快充版帮你一步搞定！3个新国标组合插孔+2个USB-A+1个USB-C，单口最高20W PD快充，手机平板笔记本一个全包。内置智能芯片自动分配电流，过流短路通通不怕。极简白色设计+隐藏式提示灯，桌面颜值瞬间拉满。京东¥54.9到手，学生党桌面刚需神器，趁开学季赶紧囤！",
        "highlights": [
            "2A1C三口快充：USB-C单口20W PD快充，USB-A单口18W，多设备同时充不发烫",
            "3个新国标插孔：大间距设计，大插头也不打架，全家设备一个全包",
            "智能电流分配：内置芯片自动识别设备，过流短路自动保护，安全不伤机",
            "极简白色桌面美学：隐藏式提示灯+简约外壳，桌面整洁颜值高",
            "阻燃PC+儿童安全门：通过750℃灼热丝验证，单孔防误插，宿舍用电更安心",
        ],
        "tags": ["小米", "插线板", "快充", "宿舍神器", "桌面收纳"],
        "suitable": "大学生 · 宿舍党 · 数码爱好者 · 桌面整理控",
        "price_note": "京东¥54-59",
        "img": f"{OUT_DIR}/orig_product_1.jpg",
        "color": "#FF7043",
    },
    {
        "num": "02",
        "category": "学习装备",
        "title": "书客SUKER护眼台灯L1！RRT红光养眼，百元级护眼天花板",
        "subtitle": "RRT红光养眼 · 国AA照度 · Ra98.6显色 · 减80%近视风险",
        "desc": "开学熬夜刷题，眼睛酸胀干涩？书客L1护眼台灯用百元价位做到专业级护眼，被丁香医生和CCTV双双推荐！独创RRT红光养眼技术，三分钟红光增益缓解用眼疲劳；国AA照度+182cm²大面积光源，2米大桌面全铺满无暗区；Ra98超高显色指数，还原真实色彩。45分钟定时休息提醒，手扫调光+夜灯模式，面面俱到。¥369-399，开学装备刚需好物！",
        "highlights": [
            "RRT红光养眼技术：独家专利，精准过滤有害蓝光+补充有益红光，降低80%近视风险",
            "国AA级照度：182cm²大面积光源，2米桌面全铺满，桌角也无暗区阴影",
            "Ra98.6超高显色指数：色彩还原真实细腻，画画、做手账、读绘本都适合",
            "OCLT光透镜技术：消除手影眩光，4000K暖白光越看越舒服，晚自习不累眼",
            "手扫无极调光+夜灯模式+45分钟定时休息：功能齐全，百元价位越级体验",
        ],
        "tags": ["护眼台灯", "书客", "学生党", "学习装备", "护眼好物"],
        "suitable": "学生党 · 考研族 · 设计师 · 夜读爱好者",
        "price_note": "京东¥369-399",
        "img": f"{OUT_DIR}/orig_product_2.jpg",
        "color": "#FFCA28",
    },
    {
        "num": "03",
        "category": "桌面照明",
        "title": "美的魔盒Plus折叠台灯！充插两用+Ra95高显色，百元内首选",
        "subtitle": "折叠仅手机大小 · 充插两用 · Ra95高显色 · 三段色温切换",
        "desc": "宿舍桌面有限，灯具占地太大？美的魔盒Plus折叠台灯折叠后只有手机大小，轻松放进抽屉，桌面永远整洁！展开即可充插两用——插电当主灯，拔电当移动灯，走到哪亮到哪。Ra95超高显色指数，还原书本真实色彩；无极调光+三段色温切换，阅读、看剧、起夜各取所需。京东阅读台灯热卖榜TOP2，百元内护眼台灯首选，开学季¥88性价比拉满！",
        "highlights": [
            "折叠仅手机大小：分体折叠设计，收纳后随手放抽屉，桌面空间零占用",
            "充插两用模式：插电当主台灯，拔电秒变移动夜灯，宿舍熄灯也不怕",
            "Ra95超高显色指数：百元以下少有，还原书本真实色彩，学习效率更高",
            "无极调光+三段色温：3000K暖光到6000K白光一键切换，阅读/夜灯/氛围全覆盖",
            "京东台灯热卖榜TOP2：50万+评价验证品质，百元内桌面照明闭眼入",
        ],
        "tags": ["美的", "折叠台灯", "宿舍好物", "学习灯具", "桌面照明"],
        "suitable": "住校生 · 小空间住户 · 租房党 · 多场景照明需求者",
        "price_note": "京东¥88",
        "img": f"{OUT_DIR}/orig_product_3.jpg",
        "color": "#26C6DA",
    },
    {
        "num": "04",
        "category": "出行必备",
        "title": "绿联20000mAh充电宝！自带线+多协议快充，京东50万+口碑认证",
        "subtitle": "自带Type-C+Lightning线 · 20000mAh大容量 · 多协议快充 · 3C认证",
        "desc": "开学外出最怕什么？手机没电又找不到充电头！绿联这款20000mAh充电宝自带Type-C线和Lightning线，苹果安卓都能直接插上就充，不用再带一堆线。支持PD、QC、FCP等多协议快充，iPhone和安卓都能快充回血。内置智能保护芯片，过充过放统统不怕。符合3C认证，飞机高铁都能带。京东累计50万+评价，开学季¥119起，全天候续航不断电！",
        "highlights": [
            "自带双线：Type-C+Lightning二合一，出行免带线，苹果安卓拿起就用",
            "20000mAh大容量：实测可充iPhone约5次，图书馆/上课/社团活动全天在线",
            "多协议快充：PD+QC+FCP+PPS，兼容苹果/华为/小米/三星等主流机型",
            "3C认证+智能保护：过充/过放/短路/过温全面保护，安心带上飞机高铁",
            "京东50万+评价：充电宝热卖榜常青款，口碑和销量双认证",
        ],
        "tags": ["绿联", "充电宝", "自带线", "快充", "出行必备"],
        "suitable": "大学生 · 通勤族 · 旅游爱好者 · 户外党",
        "price_note": "京东¥119",
        "img": f"{OUT_DIR}/orig_product_4.jpg",
        "color": "#66BB6A",
    },
    {
        "num": "05",
        "category": "健康好物",
        "title": "飞利浦电动牙刷Sonicare！声波31000次/分，口腔健康从开学抓起",
        "subtitle": "声波31000次/分 · 钻石菱形刷头 · 智能压力感应 · 两周续航",
        "desc": "刷牙敷衍了事，口腔问题悄悄找上门？飞利浦Sonicare声波震动牙刷，每分钟31000次高频震动，配合流动洁力深入牙缝盲区，把手动刷不干净的牙菌斑全部震出来！美国进口杜邦钻石菱形刷头，清洁效率比普通牙刷提升7倍。智能压力感应提示，防止用力过猛伤牙龈。USB充电底座，一次充电可用两周，旅行出差也方便。开学季¥229起，口腔健康是长期投资，入手不亏！",
        "highlights": [
            "声波31000次/分高频震动：流动洁力深入牙缝，比手动刷牙清洁力提升7倍",
            "美国进口杜邦钻石菱形刷头：菱形切面贴合牙面，清洁效率更高，不伤牙龈",
            "智能压力感应：刷牙用力过猛自动提醒，防止牙龈退缩，保护牙釉质",
            "USB充电+两周续航：一次充满用两周，出差旅行也方便，充一次用半个月",
            "全球销量TOP1品牌：飞利浦Sonicare系列全球用户超千万，品质值得信赖",
        ],
        "tags": ["飞利浦", "电动牙刷", "声波震动", "口腔护理", "健康好物"],
        "suitable": "学生党 · 职场人 · 家庭用户 · 口腔健康重视者",
        "price_note": "京东¥229",
        "img": f"{OUT_DIR}/orig_product_5.jpg",
        "color": "#42A5F5",
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

    # 标题
    font_title = load_font(52, bold=True)
    draw.text((40, img_y + 30), title[:32], fill=(30, 30, 30), font=font_title)
    # 换行标题（如果需要）
    if len(title) > 32:
        draw.text((40, img_y + 90), title[32:64], fill=(30, 30, 30), font=font_title)

    # 副标题
    font_sub = load_font(34)
    draw.text((40, img_y + 145), subtitle, fill=(100, 100, 100), font=font_sub)

    # 价格
    font_price = load_font(60, bold=True)
    draw.text((40, img_y + 200), price_note, fill=color, font=font_price)

    # 分割线
    line_y = img_y + 270
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
