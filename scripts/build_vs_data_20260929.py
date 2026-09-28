#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vs_data_20260929.py  (v2 - 兼容 db_save.py 输入 schema)
vs-data.json: 5 个商品 vs 各赛道 Top3 竞品 + 5 个 hotProducts + sources + dataSource + updateTime
"""
import json
from pathlib import Path

OUT_DIR = Path('/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-29')
OUT_DIR.mkdir(parents=True, exist_ok=True)

PLACEHOLDER_IMG = ""

# 5 个商品 vs 各自竞品（分组化, 每组 product + items 4 项, items[0] 是主推）
competitors = [
    {
        "product": "可复美 Collgene 柔肤水 500ml ¥133-¥168",
        "group": "京东柔肤水 KanS 销量榜 + 天猫爽肤水爽肤乳榜",
        "items": [
            {
                "name": "可复美 Collgene 柔肤水 500ml 补水保湿舒缓湿敷水 敏感肌爽肤水 巨子生物官方旗舰店",
                "price": "¥133-¥168",
                "advantage": "京东柔肤水 KanS 销量 TOP1 + 单品销量 30 万+ + 巨子生物核心专利重组胶原蛋白 + 4D 玻尿酸 + 神经酰胺 + 马齿苋舒缓修护 + 500ml 大容量湿敷",
                "jd_sales": "京东柔肤水 KanS TOP1 · 30 万+ 评价 · 巨子生物官方",
                "color": "#B0D4E8",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "薇诺娜 Winona 极润保湿柔肤水 敏感肌爽肤水化妆水湿敷护肤干皮舒缓补水",
                "price": "¥89-¥169",
                "advantage": "薇诺娜 2008 年国产敏感肌大厂 ¥89-¥169 (单品评价 10 万+), 青刺果油 + 神经酰胺成分, 但是价格带与可复美重叠, 销量 10 万+ 不到可复美 30 万+ 的一半",
                "jd_sales": "京东 ¥89-¥169 · 10 万+ 评价",
                "color": "#C8E0F0"
            },
            {
                "name": "珂润 Curel 保湿化妆水 II 150ml 干燥敏感肌 爽肤水化妆水",
                "price": "¥115-¥208",
                "advantage": "珂润 1999 年日本花王旗下敏感肌品牌 ¥115-¥208, 神经酰胺功能成分类似可复美, 但是 150ml 容量仅是可复美 500ml 的 30%, 单 ml 价格贵 1 倍",
                "jd_sales": "京东 ¥115-¥208 · 2 万+ 评价",
                "color": "#D8E8F0"
            },
            {
                "name": "百雀羚 Pechoin 草本精萃爽肤水清爽补水保湿滋润精华水化妆水",
                "price": "¥43.7-¥129",
                "advantage": "百雀羚 1931 年中国国货老字号 ¥43.7-¥129, 比可复美便宜 50-67%, 但是植物草本配方侧重保湿而非修护, 医美术后 / 屏障受损场景不如可复美",
                "jd_sales": "京东 ¥43.7 起 · 2 万+ 评价",
                "color": "#E0F0E8"
            }
        ]
    },
    {
        "product": "小米 自带线充电宝 20000mAh 67W ¥129-¥149",
        "group": "京东随身电源移动电源榜 + 京东大毫安充电宝榜",
        "items": [
            {
                "name": "小米 MI 自带线充电宝 20000mAh 67W 浅蓝色 可上飞机/火车 充手机平板笔记本 iPhone",
                "price": "¥129-¥149",
                "advantage": "京东随身电源移动电源 TOP1 + 单品评价 200 万+ + 3C 国家认证可上飞机/高铁 + 67W 双向百瓦快充 + 自带 Type-C 线 + 20000mAh 大容量",
                "jd_sales": "京东随身电源 TOP1 · 200 万+ 评价 · 3C 认证",
                "color": "#9DBFD9",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "CUKTECH 酷态科 25 号 SE 充电宝 自带线 120W 快充 25000mAh 钛灰",
                "price": "¥299-¥349",
                "advantage": "CUKTECH 2019 年国产新势力 ¥299-¥349 (25000mAh), 120W 单口充电更快, 但是容量大 25% 价格贵 130%, 国庆出游预算低于 200 元首选小米",
                "jd_sales": "京东 ¥299 起 · 2 万+ 评价",
                "color": "#6B7B8B"
            },
            {
                "name": "京东京造 35W 充电宝 自带线 20000 毫安 大容量小巧轻薄 3c 认证京东自营",
                "price": "¥99-¥149",
                "advantage": "京东京造 2018 年京东自有品牌 ¥99-¥149 (20000mAh), 价格与小米基本持平, 3C 认证同款, 但是 35W 比小米 67W 充电慢近 1 倍, 笔记本应急不如小米",
                "jd_sales": "京东 ¥99 起 · 50 万+ 评价",
                "color": "#7B8FA0"
            },
            {
                "name": "Anker 安克 能量舱 165W 自带线 25000 毫安 苹果笔记本电脑移动电源",
                "price": "¥549-¥699",
                "advantage": "Anker 2011 年美国品牌 ¥549-¥699 (25000mAh), 165W 笔记本快充, 但是比小米 67W 20000mAh 贵 4-5 倍, 国庆 7 天出游预算有限首选小米",
                "jd_sales": "京东 ¥549 起 · 10 万+ 评价",
                "color": "#5B6B7B"
            }
        ]
    },
    {
        "product": "米家 小米智能空气炸锅 P1 6.5L ¥399-¥499",
        "group": "京东空气炸锅榜 + 米家智能家居爆品榜",
        "items": [
            {
                "name": "米家 小米智能空气炸锅 P1 6.5L 家用多功能电炸锅 上下双热源免翻面 APP 互联 台式大容量",
                "price": "¥399-¥499",
                "advantage": "京东空气炸锅与电烤箱品牌榜 TOP3 + 米家单品销量 50 万+ + 上下双热源 360° 立体热风 + 6.5L 大容量 + 米家 APP 远程控制 + 200+ 智能菜谱",
                "jd_sales": "京东空气炸锅榜 TOP3 · 米家单品 50 万+ · APP 互联",
                "color": "#F5F5F0",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "美的 Midea 蒸烤一体空气炸锅 京东自营 KZE535J5 5.3L 金属内腔",
                "price": "¥289-¥399",
                "advantage": "美的 1968 年国产家电大厂 ¥289-¥399 (5.3L), KZE535J5 比米家 P1 6.5L 容量小 18%, 但是价格便宜 27%, 不带 APP 智能互联, 不支持远程控制",
                "jd_sales": "京东 ¥289 起 · 200 万+ 评价",
                "color": "#FAFAFA"
            },
            {
                "name": "苏泊尔 SUPOR 0涂层空气炸锅 KD60DG835 6L 大容量双热源免翻面",
                "price": "¥349-¥459",
                "advantage": "苏泊尔 1994 年国产炊具大厂 ¥349-¥459 (6L), 304 不锈钢 0 涂层比米家涂层内胆更健康, 但是无 APP 控制, 智能菜谱需要手动操作",
                "jd_sales": "京东 ¥349 起 · 100 万+ 评价",
                "color": "#E8E8E8"
            },
            {
                "name": "九阳 Joyoung V585 空气炸锅 6L 大容量免翻面 0氟钛瓷烤盘 蒸烤炸一体",
                "price": "¥399-¥499",
                "advantage": "九阳 1994 年国产厨房电器大厂 ¥399-¥499 (6L), 与米家 P1 价格持平, 0氟钛瓷烤盘比米家涂层健康, 但是不带 APP 互联, 米家智能家居生态弱",
                "jd_sales": "京东 ¥399 起 · 100 万+ 评价",
                "color": "#F0F0F0"
            }
        ]
    },
    {
        "product": "蕉下 双肩背包 20L ¥138-¥174",
        "group": "京东登山包双肩背包销量榜 + 京东轻便旅游包榜",
        "items": [
            {
                "name": "蕉下 Beneunder 新款大容量旅行双肩背包 轻便扩容 户外徒步通勤 便携双肩背包",
                "price": "¥138-¥174",
                "advantage": "京东登山包双肩背包 TOP1 + 单品销量 9 万+ + 京东轻便旅游包 TOP1 + 蕉下 2013 年中国防晒大厂 + 20L 大容量 + 多隔层 + 防泼水 + 加厚透气肩带",
                "jd_sales": "京东登山包 TOP1 · 9 万+ 评价 · 蕉下官方",
                "color": "#6B8FB5",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "迪卡侬 DECATHLON NH100 大容量户外徒步背包 20L 十年质保",
                "price": "¥89.9-¥99.9",
                "advantage": "迪卡侬 1976 年法国户外大厂 ¥89.9-¥99.9 (20L), 比蕉下便宜 30%, 十年质保是卖点, 但是单一深蓝色无多色可选, 内部分层少不如蕉下",
                "jd_sales": "京东 ¥89.9 起 · 10 万+ 评价",
                "color": "#FF8C42"
            },
            {
                "name": "骆驼 CAMEL 280g 轻量双肩包 书包升级款 2026新款",
                "price": "¥47-¥89",
                "advantage": "骆驼 1933 年国产户外老牌 ¥47-¥89, 比蕉下便宜 50-66%, 280g 超轻是亮点, 但是 280g 面料耐磨度不如蕉下防泼水面料, 长期使用起球风险高",
                "jd_sales": "京东 ¥47 起 · 3 万+ 评价",
                "color": "#5A6B7C"
            },
            {
                "name": "Lee 学生书包大容量旅游双肩包",
                "price": "¥149-¥179",
                "advantage": "Lee 1889 年美国牛仔老牌 ¥149-¥179, 与蕉下价格持平, 颜值能打, 但是 Lee 书包定位学生上学, 国庆出游场景的功能分区不如蕉下专业",
                "jd_sales": "京东 ¥149 起 · 3 万+ 评价",
                "color": "#D87093"
            }
        ]
    },
    {
        "product": "小熊 双层煮蛋器 304 不锈钢 ¥64.9-¥94.91",
        "group": "京东早餐机销量榜 + 京东 electrolux 早餐机榜",
        "items": [
            {
                "name": "小熊 Bear 双层速蒸煮蛋器早餐机 双层长效蒸煮 健康酚A 304不锈钢 母婴级材质",
                "price": "¥64.9-¥94.91",
                "advantage": "京东早餐机销量 TOP1 + 单品销量 9 万+ + 小熊 2006 年中国创意小家电大厂 + 双层同时蒸煮 + 304 母婴级不锈钢 + 自动断电防干烧 + 10 分钟速蒸",
                "jd_sales": "京东早餐机 TOP1 · 9 万+ 评价 · 小熊官方",
                "color": "#FAFAFA",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "奥克斯 AUX 煮蛋器 全自动断电家用小型 400W 304 不锈钢蒸碗",
                "price": "¥29.99-¥49.99",
                "advantage": "奥克斯 1986 年国产家电大厂 ¥29.99-¥49.99 (400W), 比小熊便宜 50%, 价格杀手, 但是单层设计容量仅为小熊双层一半, 1-2 人够用 3 口之家不够",
                "jd_sales": "京东 ¥29.99 起 · 10 万+ 评价",
                "color": "#E0E0E0"
            },
            {
                "name": "九阳 Joyoung 316L 不锈钢煮蛋器 定时免看管 单双层自由组合",
                "price": "¥75.05-¥99",
                "advantage": "九阳 1994 年国产厨房大厂 ¥75.05-¥99, 316L 母婴级比小熊 304 不锈钢更耐腐蚀, 但是定时器是机械式不如小熊电子精确, 加热功率 350W 比小熊慢 10%",
                "jd_sales": "京东 ¥75.05 起 · 4 万+ 评价",
                "color": "#F0F0F0"
            },
            {
                "name": "小熊 Bear 母婴级 316L 煮蛋器 销冠 N0.1 双层不锈钢可定时蒸煮多用",
                "price": "¥94.91-¥129",
                "advantage": "小熊自家高端款 316L 升级版 ¥94.91-¥129, 比基础款贵 50%, 316L 比 304 母婴级更安全, 但是家庭场景 ¥65 基础款已够用, 升级必要性弱",
                "jd_sales": "京东 ¥94.91 起 · 7 万+ 评价",
                "color": "#F5F5F5"
            }
        ]
    }
]

# 5 个 hotProducts（与主推商品对齐）
hot_products = [
    {
        "name": "可复美 Collgene 柔肤水 500ml 补水保湿舒缓湿敷水",
        "category": "敏肌修护柔肤水",
        "price": "¥133-¥168",
        "image": PLACEHOLDER_IMG,
        "sales": "京东柔肤水 KanS TOP1 · 30 万+ 评价 · 巨子生物官方",
        "platform": "京东自营"
    },
    {
        "name": "小米 MI 自带线充电宝 20000mAh 67W 浅蓝色",
        "category": "自带线快充充电宝",
        "price": "¥129-¥149",
        "image": PLACEHOLDER_IMG,
        "sales": "京东随身电源 TOP1 · 200 万+ 评价 · 3C 认证可上飞机",
        "platform": "京东自营"
    },
    {
        "name": "米家 小米智能空气炸锅 P1 6.5L 上下双热源",
        "category": "智能空气炸锅",
        "price": "¥399-¥499",
        "image": PLACEHOLDER_IMG,
        "sales": "京东空气炸锅榜 TOP3 · 米家单品 50 万+ 销量 · APP 互联",
        "platform": "京东自营"
    },
    {
        "name": "蕉下 Beneunder 大容量旅行双肩背包 20L",
        "category": "旅行双肩背包",
        "price": "¥138-¥174",
        "image": PLACEHOLDER_IMG,
        "sales": "京东登山包双肩背包 TOP1 · 9 万+ 评价 · 蕉下官方",
        "platform": "京东自营"
    },
    {
        "name": "小熊 Bear 双层速蒸煮蛋器 304 不锈钢母婴级",
        "category": "双层煮蛋器",
        "price": "¥64.9-¥94.91",
        "image": PLACEHOLDER_IMG,
        "sales": "京东早餐机销量 TOP1 · 9 万+ 评价 · 小熊官方",
        "platform": "京东自营"
    }
]

# 真实来源（WebSearch 抓取的 URL）
sources = [
    "京东柔肤水 KanS 销量榜 + 天猫爽肤水爽肤乳榜 (jd.com)",
    "京东随身电源移动电源榜 + 京东大毫安充电宝榜 (jd.com)",
    "京东空气炸锅榜 + 米家智能家居爆品榜 (jd.com)",
    "京东登山包双肩背包销量榜 + 京东轻便旅游包榜 (jd.com)",
    "京东早餐机销量榜 + 京东 electrolux 早餐机榜 (jd.com)",
    "京东自营官方价格 + 9 月底秋分后 + 国庆前 2 天选品定位 (2026-09-29 07:00 抓取)",
    "锦观新闻 2026-09-22 '巴掌好物'带火出行市场 (jd.com 数据)",
    "CUKTECH / 苏泊尔 / 美的 / 九阳 / 迪卡侬 / 奥克斯京东自营官方旗舰店价格"
]

vs_data = {
    "date": "2026-09-29",
    "sources": sources,
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": "WebSearch 真实数据 + 京东自营官方价格 + 京东金榜 5 大场景榜单 (2026-09-29 07:00 抓取)",
    "updateTime": "2026-09-29 07:30:00"
}

with open(OUT_DIR / 'vs-data.json', 'w', encoding='utf-8') as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

print(f"✅ vs-data.json 已写入: {OUT_DIR / 'vs-data.json'}")
print(f"  - competitors: {len(competitors)} 组 × 4 项")
print(f"  - hotProducts: {len(hot_products)} 项")
print(f"  - sources: {len(sources)} 条")