#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成5款商品详情长图（1080px宽），每款商品一张3000px高卡片，5等份裁剪"""

import os
from PIL import Image, ImageDraw, ImageFont

# 配置
TODAY = "2026-08-25"
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
        "title": "南卡OE GT2开放式耳机：289元解锁千元音质，学生党开学刚需",
        "subtitle": "不入耳设计 · 18×11mm动圈 · 蓝牙6.0 · 讯飞×DeepSeek AI",
        "desc": "入耳式耳机戴久了耳朵又闷又胀？南卡OE GT2开放式耳机，佩戴不入耳道，长时间听歌依然舒适透气，还能随时感知环境音更安全。别看才200出头，音质却能媲美千元耳机——18×11mm矩形巨幕动圈+NanoLCP振膜，低音浑厚、高音清亮。蓝牙6.0开盖秒连，60ms低延迟打游戏也流畅，24小时续航从早撑到晚。讯飞×DeepSeek AI加持，翻译、对话、搜索一键搞定。开学季289元入手，学生党闭眼入！",
        "highlights": [
            "不入耳设计，久戴不胀痛，保护听力健康",
            "18×11mm动圈+Tri-Boost三腔体，低音浑厚媲美千元耳机",
            "蓝牙6.0+60ms低延迟，开盖秒连游戏流畅",
            "24小时续航，从早课到晚自习都不用充电",
            "讯飞×DeepSeek AI，翻译问答创作一机搞定"
        ],
        "tags": ["数码配件", "开放式耳机", "开学数码", "听力保护", "学生党"],
        "suitable": "学生党 · 运动人群 · 通勤族 · 注重听力健康者",
        "price_note": "参考价¥289",
        "img": f"{OUT_DIR}/product_1.jpg",
        "color": "#2ECC71",
    },
    {
        "num": "02",
        "category": "小家电",
        "title": "小米手持挂烫机2：99元搞定宿舍衣物褶皱，开学刚需",
        "subtitle": "1300W大功率 · 26秒即热 · 可折叠收纳 · 除菌除螨",
        "desc": "开学收拾行李箱压皱的衬衫卫衣，小米手持挂烫机2来帮忙！1300W大功率26秒即热，30kPa微增压蒸汽穿透力强，棉麻衬衫3秒熨平。130℃陶瓷釉面板兼具体温护衣，熨完不湿衣可直接穿出门。730g轻巧机身，可折叠放进书包；160mL水箱可连续熨6件衣物。京东国补后到手约99元，宿舍刚需神器，开学必入！",
        "highlights": [
            "1300W大功率26秒即热，熨衣不用等待",
            "30kPa微增压蒸汽，3秒穿透棉衬衫褶皱",
            "130℃陶瓷面板护衣不伤衣，熨完即穿",
            "730g可折叠，书包侧袋轻松收纳",
            "国补后约99元，宿舍熨衣性价比首选"
        ],
        "tags": ["小家电", "手持挂烫机", "宿舍好物", "开学必备", "衣物护理"],
        "suitable": "学生党 · 租房族 · 差旅人群 · 注重仪表者",
        "price_note": "京东国补后约¥99",
        "img": f"{OUT_DIR}/product_2.png",
        "color": "#3498DB",
    },
    {
        "num": "03",
        "category": "学习装备",
        "title": "书客护眼台灯L1：369元守护孩子视力，百元护眼灯天花板",
        "subtitle": "RRT2.0红光养眼 · SDIT自适应调光 · Ra98高显色 · 欧盟认证",
        "desc": "孩子每晚写作业揉眼睛？书客护眼台灯L1专为守护学生视力设计。RRT2.0红光养眼技术，精准过滤有害蓝光同时补足有益红光，降低80%近视风险。SDIT自适应调光系统，每秒100次实时监测环境光，亮度、色温自动调节到最适合的状态。Ra98高显色无频闪，绘本颜色真实还原。CE/FCC欧盟认证，CCTV展播推荐，百元价位护眼天花板，开学给孩子一份视力保障！",
        "highlights": [
            "RRT2.0红光养眼，近视风险降低80%",
            "SDIT自适应调光，每秒100次实时监测环境光",
            "Ra98高显色+无频闪，护眼不眼疲劳",
            "DT多漫射技术，1800次光束折射模拟自然光",
            "CE/FCC欧盟认证，CCTV展播推荐"
        ],
        "tags": ["学习装备", "护眼台灯", "书桌好物", "儿童护眼", "开学必备"],
        "suitable": "学生家长 · 考研人群 · 设计师 · 夜间阅读者",
        "price_note": "参考价¥369",
        "img": f"{OUT_DIR}/product_3.png",
        "color": "#F39C12",
    },
    {
        "num": "04",
        "category": "日用刚需",
        "title": "德佑加厚洗脸巾3包装：46元承包半年用量，比毛巾干净100倍",
        "subtitle": "加厚不掉絮 · 悬挂式抽取 · 一巾多用 · 婴儿级认证",
        "desc": "毛巾用久了细菌螨虫超标，脸上反复长痘可能是毛巾的锅！德佑加厚洗脸巾，一次性使用随扔随换，彻底告别螨虫困扰。加厚棉柔材质，触感细腻不掉絮，湿水后韧性依然很强，擦脸后还能顺手擦桌子擦镜子，一巾多用不浪费。悬挂式抽取方便卫生，3包约200抽，46元到手承包半年用量。天猫超市月销超6万件，口碑验证！",
        "highlights": [
            "一次性随扔，零螨虫零细菌皮肤更健康",
            "加厚不掉絮，湿水后韧性依然很强",
            "悬挂式抽取方便卫生，一抽一张不浪费",
            "一巾多用：擦脸→擦桌→擦镜，环保不浪费",
            "3包约46元，月销6万件，口碑验证"
        ],
        "tags": ["日用刚需", "洗脸巾", "洁面护肤", "租房好物", "懒人神器"],
        "suitable": "敏感肌 · 学生党 · 租房族 · 注重卫生人群",
        "price_note": "3包装约¥46",
        "img": f"{OUT_DIR}/product_4.jpg",
        "color": "#9B59B6",
    },
    {
        "num": "05",
        "category": "生活用品",
        "title": "苏泊尔保温杯316L：68元全天恒温，开学季饮水神器",
        "subtitle": "316L不锈钢内胆 · 真空锁温 · 单手开合 · 防漏便携",
        "desc": "开学上课一天，教室、图书馆、宿舍来回跑，随身一杯温水很重要。苏泊尔这款保温杯，采用母婴级316L不锈钢内胆，耐腐蚀更安全，装咖啡、装茶水都不担心异味残留。真空锁温技术，早起装热水到下午依然温热入口。弹盖单手开合设计，课间喝水不用找地方放杯子。密封防漏放进书包无压力，68元搞定全天饮水刚需，开学季性价比之选！",
        "highlights": [
            "316L不锈钢内胆，母婴级安全材质更放心",
            "真空锁温技术，全天保温保冷一杯搞定",
            "弹盖单手开合，课间喝水不用找桌子放",
            "密封防漏设计，书包侧袋随便放不渗漏",
            "68元开学价，比买奶茶还划算的实用刚需"
        ],
        "tags": ["生活用品", "保温杯", "开学必备", "宿舍好物", "随身水杯"],
        "suitable": "学生党 · 上班族 · 户外人群 · 注重健康饮水者",
        "price_note": "参考价¥68",
        "img": f"{OUT_DIR}/product_5.jpg",
        "color": "#E74C3C",
    },
]

def load_font(size):
    """加载字体"""
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def create_product_card(product, index):
    """创建单个商品卡片"""
    img = Image.new("RGB", (WIDTH, CARD_H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    font_title = load_font(48)
    font_sub = load_font(28)
    font_desc = load_font(32)
    font_tag = load_font(26)
    font_small = load_font(24)
    font_price = load_font(52)
    font_num = load_font(80)
    font_header = load_font(36)

    color = product["color"]

    # 顶部色块
    draw.rectangle([(0, 0), (WIDTH, 200)], fill=color)

    # 序号
    draw.text((50, 40), f"#{product['num']}", font=font_num, fill="#FFFFFF")

    # 分类标签
    draw.text((200, 60), product["category"], font=font_header, fill="#FFFFFF")

    # 价格
    draw.text((700, 50), product["price_note"], font=font_price, fill="#FFFFFF")

    # 商品图片（居中，1080x1080）
    if os.path.exists(product["img"]):
        try:
            prod_img = Image.open(product["img"])
            prod_img = prod_img.convert("RGB")
            # 裁剪成正方形（居中裁剪）
            w, h = prod_img.size
            min_dim = min(w, h)
            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            prod_img = prod_img.crop((left, top, left+min_dim, top+min_dim))
            prod_img = prod_img.resize((WIDTH, WIDTH), Image.LANCZOS)
            img.paste(prod_img, (0, 200))
        except Exception as e:
            print(f"图片加载失败: {e}")
            draw.rectangle([(0, 200), (WIDTH, 1280)], fill="#F0F0F0")
            draw.text((WIDTH//2-200, 700), "[商品图片]", font=font_title, fill="#CCCCCC")
    else:
        draw.rectangle([(0, 200), (WIDTH, 1280)], fill="#F0F0F0")
        draw.text((WIDTH//2-200, 700), "[商品图片]", font=font_title, fill="#CCCCCC")

    # 商品标题
    y = 1300
    draw.text((50, y), product["title"], font=font_title, fill="#1A1A1A")
    y += 70

    # 副标题/卖点
    draw.text((50, y), product["subtitle"], font=font_sub, fill="#666666")
    y += 50

    # 分隔线
    draw.line([(50, y), (WIDTH-50, y)], fill=color, width=3)
    y += 30

    # 商品描述
    desc_lines = []
    words = list(product["desc"])
    line = ""
    max_chars = 28
    for i, w in enumerate(words):
        if len(line) >= max_chars:
            desc_lines.append(line)
            line = ""
        line += w
    if line:
        desc_lines.append(line)

    for line in desc_lines[:5]:
        draw.text((50, y), line, font=font_desc, fill="#333333")
        y += 46

    y += 20

    # 亮点
    draw.text((50, y), "✨ 核心亮点", font=font_header, fill=color)
    y += 55

    for hl in product["highlights"]:
        draw.text((50, y), f"• {hl}", font=font_desc, fill="#444444")
        y += 42

    y += 20

    # 标签
    tag_str = " | ".join(product["tags"])
    draw.text((50, y), f"【{tag_str}】", font=font_tag, fill="#888888")
    y += 45

    # 适用人群
    draw.text((50, y), f"适用人群：{product['suitable']}", font=font_small, fill="#888888")
    y += 40

    # 底部价格
    draw.rectangle([(0, CARD_H-100), (WIDTH, CARD_H)], fill=color)
    draw.text((50, CARD_H-80), f"限时特价 {product['price_note']}", font=font_price, fill="#FFFFFF")
    draw.text((700, CARD_H-75), "小红书图文带货", font=font_small, fill="#FFFFFF")

    return img

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # 合成完整长图
    full_h = 0
    cards = []
    for i, product in enumerate(PRODUCTS):
        print(f"正在生成卡片 {i+1}/5: {product['title'][:30]}...")
        card = create_product_card(product, i)
        cards.append(card)
        full_h += CARD_H
        if i < len(PRODUCTS) - 1:
            full_h += GAP

    # 拼接
    full_img = Image.new("RGB", (WIDTH, full_h), "#FFFFFF")
    y_offset = 0
    for card in cards:
        full_img.paste(card, (0, y_offset))
        y_offset += CARD_H + GAP

    full_path = f"{OUT_DIR}/full_card.jpg"
    full_img.save(full_path, "JPEG", quality=92)
    print(f"✅ 完整长图已保存: {full_path}")

    # 裁剪成5份
    PART_H = CARD_H
    for i in range(5):
        top = i * (PART_H + GAP)
        part = full_img.crop((0, top, WIDTH, top + PART_H))
        part_path = f"{OUT_DIR}/detail_{i+1}.jpg"
        part.save(part_path, "JPEG", quality=90)
        print(f"  第{i+1}张详情图已保存: {part_path}")

    print(f"\n🎉 全部完成！共生成1张全图+5张详情图")

if __name__ == "__main__":
    main()
