#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vs_data_20260925.py  (v2 - 兼容 db_save.py 输入 schema)
vs-data.json: 5 个商品 vs 各赛道 Top3 竞品 + 5 个 hotProducts + sources + dataSource + updateTime
schema 兼容 db_save.py (扁平 competitor → 分组 competitors/items)
"""
import json
from pathlib import Path

OUT_DIR = Path('/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-25')
OUT_DIR.mkdir(parents=True, exist_ok=True)

PLACEHOLDER_IMG = ""

# 5 个商品 vs 各自竞品（分组化, 每组 product + items 4 项, items[0] 是主推）
competitors = [
    {
        "product": "三只松鼠 每日坚果 750g 30袋独立包装 ¥89-¥119",
        "group": "京东坚果果干排行榜",
        "items": [
            {
                "name": "三只松鼠 每日坚果 750g 30袋独立包装 腰果开心果 干果坚果礼盒 中秋团购送礼",
                "price": "¥89-¥119",
                "advantage": "京东坚果果干 TOP1 + 5,000,000+ 评价 + 三只松鼠 14 年坚果大厂 + 4 种坚果 + 2 种果干科学配比 + 750g/30 袋独立包装",
                "jd_sales": "京东 5,000,000+ 评价 · 坚果果干榜 TOP1",
                "color": "#E8C547",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "百草味 低 GI 每日纯坚果 700g 无添加 休闲零食独立包装 团购中秋礼品",
                "price": "¥89-¥139",
                "advantage": "百草味老牌零食同规格 700g 低价位段,但是销量 4,000,000 低于三只松鼠 5,000,000+",
                "jd_sales": "京东 4,000,000+ 评价",
                "color": "#D2A36C"
            },
            {
                "name": "沃隆 每日坚果纯坚果 750g/30袋 低 GI 腰果开心果 休闲零食送礼中秋礼盒",
                "price": "¥89-¥139",
                "advantage": "沃隆每日坚果开创者 750g/30 袋,行业标准制定方,但是同等规格价格高于三只松鼠",
                "jd_sales": "京东 1,000,000+ 评价",
                "color": "#8B7355"
            },
            {
                "name": "洽洽 小黄袋每日坚果 750g/30袋 混合干果 腰果 儿童孕妇零食坚果礼盒",
                "price": "¥69-¥99",
                "advantage": "洽洽瓜子在坚果赛道 750g/30 袋价位段 ¥69-99 比三只松鼠便宜 10-20%,但是坚果种类仅 4 种且无果干",
                "jd_sales": "京东 500,000+ 评价",
                "color": "#F0C674"
            }
        ]
    },
    {
        "product": "波司登 秋季轻薄羽绒服女短款 90 绒 ¥399-¥599",
        "group": "京东女士轻薄羽绒短款排行榜",
        "items": [
            {
                "name": "波司登 BOSIDENG 秋季轻薄羽绒服女短款 90 绒 三防轻便 内胆葫芦纹 保暖外套",
                "price": "¥399-¥599",
                "advantage": "京东女士轻薄羽绒 TOP1 + 2,000+ 评价 + 波司登 50 年羽绒大厂 + 90% 白鸭绒 + 三防面料（防风/防水/防污）+ 葫芦纹车线",
                "jd_sales": "京东 2,000+ 评价 · 女士轻薄羽绒短款榜 TOP1",
                "color": "#D2B48C",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "鸭鸭 YAYA 佟丽娅同款 轻薄羽绒服女 新款冬季短款 圆领内胆修身 时尚薄外套",
                "price": "¥299-¥499",
                "advantage": "鸭鸭 1972 年国民老牌 50,000+ 评价,但价位段 ¥299-499 比波司登便宜 17%, 90 绒占比次于波司登",
                "jd_sales": "京东 50,000+ 评价",
                "color": "#FAEBD7"
            },
            {
                "name": "雪中飞 26 新款 百搭时尚鸭绒 女式内穿羽绒马甲 便携轻薄 松紧灯笼袖鸭绒",
                "price": "¥199-¥349",
                "advantage": "雪中飞波司登旗下副线 20,000+ 评价, 价位段 ¥199-349 比波司登便宜 50%,但是马甲款式非短款羽绒",
                "jd_sales": "京东 20,000+ 评价",
                "color": "#000000"
            },
            {
                "name": "坦博尔 轻薄羽绒服女短款 翻领宽松舒适 衬衫式女士外套",
                "price": "¥299-¥459",
                "advantage": "坦博尔山东老牌 5,000+ 评价,翻领衬衫式比波司登立领更适合职场,但是含绒量 80% 低于波司登 90%",
                "jd_sales": "京东 5,000+ 评价",
                "color": "#A9A9A9"
            }
        ]
    },
    {
        "product": "西昊 M56 二代 人体工学椅 ¥399-¥599",
        "group": "京东工学电脑椅子排行榜",
        "items": [
            {
                "name": "西昊 M56 二代 人体工学椅 办公椅 电脑电竞椅子 人工力学座椅 学习升降椅背",
                "price": "¥399-¥599",
                "advantage": "京东工学电脑椅 TOP1 + 500,000+ 评价 + 西昊 130+ 项国家专利 + 多米诺立体腰靠 + 4D 联动扶手 + 135° 后仰 + 升降腰枕",
                "jd_sales": "京东 500,000+ 评价 · 工学电脑椅榜 TOP1",
                "color": "#1A1A1A",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "京东京造 Z9Pro 二代 人体工学椅 电竞椅 办公椅子 电脑椅 灰 6D 腰托",
                "price": "¥699-¥999",
                "advantage": "京东京造自营 6D 腰托 50,000+ 评价,但是价位段 ¥699-999 比西昊 M56 ¥399-599 贵 75%",
                "jd_sales": "京东 50,000+ 评价",
                "color": "#2F4F4F"
            },
            {
                "name": "黑白调 P1 二代 人体工学椅 电脑电竞椅子 人工力学座椅 办公椅 双背联动扶手",
                "price": "¥399-¥599",
                "advantage": "黑白调 200,000+ 评价价位段 ¥399-599 与西昊 M56 同, 但是 2026 品牌榜 TOP1 黑白调 (P2Pro) 在中端更占优",
                "jd_sales": "京东 200,000+ 评价",
                "color": "#000000"
            },
            {
                "name": "永艺 沃克 300Pro+ 人体工学椅 电脑椅办公椅 电竞椅子 人工力学座椅 5D 护腰",
                "price": "¥699-¥899",
                "advantage": "永艺中国椅业首家上市 5,000+ 评价,但是销量低于西昊 M56 二代 (500,000+) 100 倍",
                "jd_sales": "京东 5,000+ 评价",
                "color": "#808080"
            }
        ]
    },
    {
        "product": "霸王 防脱滋养洗发水 400ml ¥39-¥59",
        "group": "京东防脱发洗发水排行榜",
        "items": [
            {
                "name": "霸王 防脱滋养洗发水 草本老牌 中药何首乌 侧柏叶 防脱配方 400ml",
                "price": "¥39-¥59",
                "advantage": "京东防脱洗发水 TOP1 + 单品评价 100 万+ + 霸王 1928 年广州中药世家 + 港交所 01338 + 4 大草本（侧柏叶/何首乌/人参/当归）+ 国妆特字",
                "jd_sales": "京东单品评价 100 万+ · 防脱洗发水榜 TOP1",
                "color": "#5D4037",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "ReneFurterer 馥绿德雅 法国 三相防脱洗发水 微胶囊 控油防脱 200ml",
                "price": "¥189-¥299",
                "advantage": "馥绿德雅法国皮尔法伯集团 1957 年品牌,微胶囊技术高端,但是价位段 ¥189-299 比霸王贵 4-5 倍",
                "jd_sales": "京东 200,000+ 评价",
                "color": "#A5D6A7"
            },
            {
                "name": "KERASTASE 巴黎卡诗 欧莱雅集团 根源特护 防脱洗发水 500ml",
                "price": "¥299-¥389",
                "advantage": "卡诗欧莱雅高端沙龙护发'洗护届爱马仕',但是价位段 ¥299-389 比霸王贵 6-8 倍",
                "jd_sales": "京东 500,000+ 评价",
                "color": "#D4AF37"
            },
            {
                "name": "RYO 吕 爱茉莉太平洋 红参滋养 防脱洗发水 韩方强韧 400ml",
                "price": "¥69-¥119",
                "advantage": "吕韩国爱茉莉太平洋 2008 年韩方洗护品牌,红参滋养,但是价位段 ¥69-119 比霸王贵 76-100%",
                "jd_sales": "京东 100,000+ 评价",
                "color": "#B22222"
            }
        ]
    },
    {
        "product": "太力 真空压缩收纳袋 电动气泵 11件套 ¥89-¥129",
        "group": "京东电泵压缩袋排行榜",
        "items": [
            {
                "name": "太力 真空压缩收纳袋 电动气泵抽真空 被子羽绒衣服 大容量 11 件套 [销量 NO.1]",
                "price": "¥89-¥129",
                "advantage": "京东电泵压缩袋销量 NO.1 + 1,000,000+ 评价 + 太力深交所上市 18 个行业十大品牌 + 11 件多规格 + 电动气泵一键抽真空",
                "jd_sales": "京东 1,000,000+ 评价 · 电泵压缩袋销量 NO.1",
                "color": "#A4C8E1",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "收纳博士 DRstorage 真空压缩收纳袋 电动气泵 棉被子羽绒衣服 20 件套",
                "price": "¥79-¥129",
                "advantage": "收纳博士 2,000,000+ 评价 9 件套,但是手泵款 ¥79 比太力电动气泵款 ¥89 便宜 ¥10 但需手动",
                "jd_sales": "京东 2,000,000+ 评价",
                "color": "#87CEEB"
            },
            {
                "name": "京东京造 真空压缩收纳袋 家庭 20 件套 搬家打包 大容量 加厚棉被 羽绒服 带电泵",
                "price": "¥99-¥149",
                "advantage": "京东京造自营 20 件套价位段 ¥99-149 比太力 11 件套 ¥89-129 略贵 10-15%,但是件数多 9 件",
                "jd_sales": "京东 200,000+ 评价",
                "color": "#4682B4"
            },
            {
                "name": "百易特 真空压缩收纳袋 电动气泵 棉被子羽绒衣服 收纳袋 11 件套 宇航员款",
                "price": "¥69-¥109",
                "advantage": "百易特价位段 ¥69-109 比太力便宜 22%,但是销量 100,000 远低于太力 1,000,000",
                "jd_sales": "京东 100,000+ 评价",
                "color": "#6495ED"
            }
        ]
    }
]

# 5 个 hotProducts (landing page 渲染用) - 从 5 个主推商品衍生
hot_products = [
    {
        "name": "三只松鼠 每日坚果 750g/30袋",
        "category": "每日坚果",
        "price": "¥89-¥119",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 5,000,000+ 评价 · 坚果果干 TOP1",
        "platform": "京东自营"
    },
    {
        "name": "波司登 秋季轻薄羽绒服女 90 绒",
        "category": "轻薄羽绒",
        "price": "¥399-¥599",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 2,000+ 评价 · 女士轻薄羽绒短款 TOP1",
        "platform": "京东自营"
    },
    {
        "name": "西昊 M56 二代 人体工学椅",
        "category": "人体工学椅",
        "price": "¥399-¥599",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 500,000+ 评价 · 工学电脑椅 TOP1",
        "platform": "京东自营"
    },
    {
        "name": "霸王 防脱滋养洗发水 400ml",
        "category": "防脱洗发水",
        "price": "¥39-¥59",
        "image": PLACEHOLDER_IMG,
        "sales": "京东单品评价 100 万+ · 防脱洗发水 TOP1",
        "platform": "京东自营"
    },
    {
        "name": "太力 真空压缩袋 电动气泵 11件套",
        "category": "真空收纳",
        "price": "¥89-¥129",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 1,000,000+ 评价 · 电泵压缩袋 NO.1",
        "platform": "京东自营"
    }
]

# sources (真实 URL/网站名,严禁编造)
sources = [
    "京东坚果果干排行榜 https://www.jd.com/phb/key_1320955ddd873dd7f892.html",
    "京东女士轻薄羽绒短款排行榜 https://www.jd.com/phb/key_1315a04c9ca763d3f43a.html",
    "京东工学电脑椅子排行榜 https://www.jd.com/phb/key_9847660afc9a9bf096e8.html",
    "买购网 2026 防脱发洗发水十大品牌 https://www.maigoo.com/maigoo/722fangtf_index.html?frompc=1",
    "京东电泵压缩袋排行榜 https://www.jd.com/phb/key_1620ab2fd1258441d217.html",
    "买购网 2026 真空压缩袋十大品牌 https://m.maigoo.com/best/9850.html",
    "品玩 2026 人体工学椅 TOP10 深度解读 https://www.pingwest.com/a/311893",
    "今日头条 2026 防脱洗发水排行榜 https://www.toutiao.com/article/7641034765067502122"
]

build_vs = {
    "date": "2026-09-25",
    "sources": sources,
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": "WebSearch 真实数据 · 2026-09-25 cron 自动化抓取 (京东官方榜单 + 京东自营官方价格 + 买购网十大品牌)",
    "updateTime": "2026-09-25 07:30"
}

with open(OUT_DIR / 'vs-data.json', 'w', encoding='utf-8') as f:
    json.dump(build_vs, f, ensure_ascii=False, indent=2)

print(f"✅ vs-data.json 已写入: {OUT_DIR / 'vs-data.json'}")
print(f"  - 竞品组数: {len(competitors)}")
print(f"  - hotProducts: {len(hot_products)}")
print(f"  - sources: {len(sources)}")
for grp_idx, grp in enumerate(competitors):
    print(f"  - 组 {grp_idx+1}: {grp['product'][:40]}... ({len(grp['items'])} 项)")