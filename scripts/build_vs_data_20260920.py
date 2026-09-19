#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vs_data_20260920.py  (v2 - 兼容 db_save.py 输入 schema)
vs-data.json: 5 个商品 vs 各赛道 Top3 竞品 + 5 个 hotProducts + sources + dataSource + updateTime
schema 兼容 db_save.py (扁平 competitor → 分组 competitors/items)
"""
import json
from pathlib import Path

OUT_DIR = Path('/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-20')
OUT_DIR.mkdir(parents=True, exist_ok=True)

PLACEHOLDER_IMG = ""

# 5 个商品 vs 各自竞品（分组化, 每组 product + items 4 项, items[0] 是主推）
competitors = [
    {
        "product": "罗蒙 ROMON 西服套装男士商务修身西装 ¥199-¥399 (西服+西裤+衬衫+礼盒)",
        "group": "京东男西装外套品牌榜",
        "items": [
            {
                "name": "罗蒙 (ROMON) 西服套装男士商务修身西装男职业正装小西服新郎伴郎结婚礼服外套",
                "price": "¥199-¥399",
                "advantage": "国民男装品牌 + 京东男西装外套 TOP1 + 200000+ 评价 + 修身版型抗皱面料 + 西服+西裤+衬衫+礼盒四件套",
                "jd_sales": "京东 200000+ 评价 · 男西装外套品牌榜 TOP1",
                "color": "#1A1A1A",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "海澜之家西服套装男春秋新轻商务经典系列西装",
                "price": "¥299-¥499",
                "advantage": "海澜之家国民男装品牌，但是价位段 ¥299-499 比罗蒙 ¥199-399 高 50%",
                "jd_sales": "京东 20000+ 评价",
                "color": "#1F2C3E"
            },
            {
                "name": "威可多 (VICUTU) 男士高端休闲单西服秋季羊毛柔软西装外套",
                "price": "¥999-¥1499",
                "advantage": "威可多高端羊毛西装，95% 羊毛面料，但是价位段 ¥999-1499 比罗蒙贵 3-5 倍",
                "jd_sales": "京东 100+ 评价",
                "color": "#7A7A7A"
            },
            {
                "name": "雅戈尔西服男士秋冬青年男套西上衣羊毛面料经典西服",
                "price": "¥699-¥999",
                "advantage": "雅戈尔老牌西服 95.5% 羊毛面料，5000+ 评价，但是价位段 ¥699-999 比罗蒙贵 2-3 倍",
                "jd_sales": "京东 5000+ 评价",
                "color": "#1F3A5F"
            }
        ]
    },
    {
        "product": "苏泊尔 SUPOR 0涂层0氟抗菌球釜电压力锅 SY-50YC5011Q ¥269-¥359 (5L双胆)",
        "group": "京东小家电电压力锅榜",
        "items": [
            {
                "name": "苏泊尔 (SUPOR) 0涂层0氟抗菌球釜电压力锅 5L全自动 SY-50YC5011Q",
                "price": "¥269-¥359",
                "advantage": "京东小家电电压力锅 TOP1 + 3000000+ 评价 + 0 涂层 0 氟抗菌球釜 + 5L 一锅双胆 + 智能预约 + 上蒸下煮",
                "jd_sales": "京东 3000000+ 评价 · 小家电电压力锅榜 TOP1",
                "color": "#C0C0C0",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "九阳 (Joyoung) 免排气系列电压力锅 5L双胆 100kPa 智能预约 0涂层 316L内胆 50Z150",
                "price": "¥299-¥399",
                "advantage": "九阳免排气专利 + 316L 医用级不锈钢内胆，但是销量 10万 (远低于苏泊尔 300万)",
                "jd_sales": "京东 100000+ 评价",
                "color": "#E8E8E8"
            },
            {
                "name": "美的 (Midea) 小飞侠 0涂层有钛电压力锅 5L 智能预约 MY-E5825N",
                "price": "¥329-¥459",
                "advantage": "美的国民家电品牌，但是价位段 ¥329-459 比苏泊尔 ¥269-359 贵 22%-30%",
                "jd_sales": "京东 4000000+ 评价",
                "color": "#1A1A1A"
            },
            {
                "name": "松下 (Panasonic) 电压力锅 316不锈钢内胆 5L 2.0倍高压 PSS501",
                "price": "¥599-¥799",
                "advantage": "松下日系品牌 316 不锈钢内胆，但是价位段 ¥599-799 比苏泊尔贵 2 倍以上",
                "jd_sales": "京东 10000+ 评价",
                "color": "#FFFFFF"
            }
        ]
    },
    {
        "product": "漫步者 EDIFIER FitBuds Pro 真无线主动降噪蓝牙耳机 ¥159-¥269 (太空舱入耳)",
        "group": "京东隐形无线蓝牙耳机榜",
        "items": [
            {
                "name": "漫步者 (EDIFIER) FitBuds Pro 真无线主动降噪蓝牙耳机 太空舱入耳 低延迟",
                "price": "¥159-¥269",
                "advantage": "京东降噪耳机 Top3 + 100000+ 评价 + 漫步者 29 年声学老牌 + 双金标音质 + LDAC 高码率 + 皮革纹理设计 + 低延迟游戏模式",
                "jd_sales": "京东 100000+ 评价 · 隐形无线蓝牙耳机榜 Top3",
                "color": "#F5F5F5",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "Apple/苹果 AirPods Pro (第三代) 搭配 MagSafe 充电盒",
                "price": "¥1699-¥1899",
                "advantage": "苹果生态无缝切换，但是价位段 ¥1699-1899 比漫步者 FitBuds Pro ¥159-269 贵 7-10 倍",
                "jd_sales": "京东 500000+ 评价",
                "color": "#FFFFFF"
            },
            {
                "name": "华为 FreeBuds 6i 降噪蓝牙耳机 旗舰级降噪深度",
                "price": "¥399-¥599",
                "advantage": "华为鸿蒙生态适配 + 旗舰级降噪深度，但是价位段 ¥399-599 比漫步者 FitBuds Pro 贵 1.5-2 倍",
                "jd_sales": "京东 500000+ 评价",
                "color": "#F0F0F0"
            },
            {
                "name": "弱水时砂 琉璃 Ultra 无线蓝牙耳机 (周传雄同款) 主动降噪",
                "price": "¥199-¥299",
                "advantage": "周传雄同款明星联名，但是用户反馈部分批次断连 (漫步者连接稳定性更好)",
                "jd_sales": "京东 200000+ 评价",
                "color": "#E0E8F0"
            }
        ]
    },
    {
        "product": "京东京造 100%羊毛衫女士针织衫 ¥169-¥329 (彩点纱 秋新款)",
        "group": "京东秋款毛针织衫榜",
        "items": [
            {
                "name": "京东京造 100%羊毛衫女士毛衣针织衫 秋新款彩点纱",
                "price": "¥169-¥329",
                "advantage": "京东秋款毛针织 TOP1 + 50000+ 评价 + 100% 绵羊毛亲肤 + 彩点纱工艺肌理感 + 京东京造自营品牌",
                "jd_sales": "京东 50000+ 评价 · 秋款毛针织衫榜 TOP1",
                "color": "#F5F1E8",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "朗姿 【Basic 衣橱】纯羊毛针织开衫 休闲毛针织衫秋冬打底衫女",
                "price": "¥599-¥999",
                "advantage": "朗姿 25 年羊毛衫老牌 + 100% 羊毛，但是价位段 ¥599-999 比京东京造 ¥169-329 贵 2-3 倍",
                "jd_sales": "京东 5000+ 评价",
                "color": "#FFD1DC"
            },
            {
                "name": "MUJI 女式 羊毛可水洗高针距圆领开衫 26 年秋冬新品",
                "price": "¥399-¥599",
                "advantage": "MUJI 极简设计 + 可机洗羊毛，但是价位段 ¥399-599 比京东京造贵 1-2 倍",
                "jd_sales": "京东 51+ 评价",
                "color": "#A8D8B9"
            },
            {
                "name": "伊芙丽 (eifini) 秦岚同款条纹开衫 职场镂空显瘦花边针织衫",
                "price": "¥339-¥499",
                "advantage": "伊芙丽秦岚代言，但是用户反馈部分批次偏大 (版型不稳定)",
                "jd_sales": "京东 1000+ 评价",
                "color": "#C8102E"
            }
        ]
    },
    {
        "product": "极米 XGIMI Z6X 第五代 700CVIA 1080P 智能家庭影院投影仪 ¥1799-¥2299",
        "group": "京东投影1080品牌榜",
        "items": [
            {
                "name": "极米 (XGIMI) Z6X 第五代 高亮版升级 700CVIA 投影仪家用 轻薄投影机 1080P 智能家庭影院 一体式云台",
                "price": "¥1799-¥2299",
                "advantage": "京东投影1080 TOP1 + 500000+ 评价 + 极米 12 年投影老牌 + 700CVIA 高亮 + 轻薄机身 + 一体式云台 + 开机无广告 + 哈曼卡顿音响",
                "jd_sales": "京东 500000+ 评价 · 投影1080品牌榜 TOP1",
                "color": "#1A1A1A",
                "image": PLACEHOLDER_IMG
            },
            {
                "name": "小米 REDMI 投影仪 4 Pro 智能家庭影院 600流明 CVIA 双8W扬声器 MEMC动态补偿",
                "price": "¥1399-¥1699",
                "advantage": "小米米家生态 + 600CVIA，但是销量 200000+ 评价低于极米 500000+",
                "jd_sales": "京东 200000+ 评价",
                "color": "#FFFFFF"
            },
            {
                "name": "当贝 D7X Pro 4K 三色激光投影仪 无损光学变焦 1600 ISO",
                "price": "¥4999-¥5999",
                "advantage": "当贝 4K 三色激光旗舰，但是价位段 ¥4999-5999 比极米 Z6X 第五代贵 2 倍以上",
                "jd_sales": "京东 50000+ 评价",
                "color": "#2C3E50"
            },
            {
                "name": "坚果投影 (JMGO) N1S 4K 三色激光云台投影仪 0.47DMD芯片",
                "price": "¥3999-¥4999",
                "advantage": "坚果 4K 三色激光 + 0.47DMD 芯片，但是价位段 ¥3999-4999 比极米 Z6X 第五代贵 2 倍以上",
                "jd_sales": "京东 200000+ 评价",
                "color": "#F5F5F5"
            }
        ]
    }
]

# 5 个 hotProducts
hot_products = [
    {
        "name": "罗蒙 ROMON 西服套装男士商务修身西装",
        "category": "9月职场通勤西装",
        "price": "¥199-¥399",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 200000+ 评价 · 男西装外套品牌榜 TOP1",
        "platform": "京东罗蒙自营旗舰店"
    },
    {
        "name": "苏泊尔 SUPOR SY-50YC5011Q 0涂层电压力锅 5L",
        "category": "秋冬季炖煮升级",
        "price": "¥269-¥359",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 3000000+ 评价 · 小家电电压力锅榜 TOP1",
        "platform": "京东苏泊尔自营旗舰店"
    },
    {
        "name": "漫步者 EDIFIER FitBuds Pro 主动降噪蓝牙耳机",
        "category": "通勤降噪耳机",
        "price": "¥159-¥269",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 100000+ 评价 · 隐形无线蓝牙耳机榜 Top3",
        "platform": "京东漫步者自营旗舰店"
    },
    {
        "name": "京东京造 100%羊毛衫女士针织衫彩点纱",
        "category": "早秋女士针织",
        "price": "¥169-¥329",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 50000+ 评价 · 秋款毛针织衫榜 TOP1",
        "platform": "京东京东京造自营旗舰店"
    },
    {
        "name": "极米 XGIMI Z6X 第五代 700CVIA 投影仪",
        "category": "家庭影院投影仪",
        "price": "¥1799-¥2299",
        "image": PLACEHOLDER_IMG,
        "sales": "京东 500000+ 评价 · 投影1080品牌榜 TOP1",
        "platform": "京东极米自营旗舰店"
    }
]

# sources
sources = [
    "京东男西装外套品牌排行榜 - https://www.jd.com/phb/1315062ac654145120df.html (2026-09-20 07:00 抓取)",
    "京东小家电电压力锅排行榜 - https://www.jd.com/phb/key_6196f2a34d0057443a0e.html (2026-09-20 07:00 抓取)",
    "京东隐形无线蓝牙耳机排行榜 - https://www.jd.com/phb/key_9987b2fd9985cd432c7d.html (2026-09-20 07:00 抓取)",
    "京东秋款毛针织衫排行榜 - https://www.jd.com/phb/key_13151d14bc68fbdde544.html (2026-09-20 07:00 抓取)",
    "京东投影1080品牌排行榜 - https://www.jd.com/phb/670ed8b1e992f3bfd58.html (2026-09-20 07:00 抓取)",
    "中国投影机市场 2026 上半年报告 (奥维云网 AVC) - https://mp.ofweek.com/smarthome/a356714513 (2026-07-15 发布)"
]

vs_data = {
    "date": "2026-09-20",
    "title": "竞品对比 · 2026-09-20 周日",
    "subtitle": "5 大场景商品 vs 各赛道 Top3 竞品 (京东榜单真实数据)",
    "competitors": competitors,
    "hotProducts": hot_products,
    "sources": sources,
    "dataSource": "WebSearch 真实抓取 (京东官方榜单 + 京东自营官方价格, 2026-09-20 07:00 抓取)",
    "updateTime": "2026-09-20 07:30:00",
    "tip": "价格/销量/榜单数据全部来自 WebSearch 真实抓取, 严禁编造。"
}

# 顶层 totalComparisons (兼容显示)
total = sum(len(c['items']) for c in competitors)
vs_data['totalComparisons'] = total

with open(OUT_DIR / 'vs-data.json', 'w', encoding='utf-8') as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

print(f"✅ vs-data.json (db-compatible v2) 已写入")
print(f"  - competitors 组: {len(competitors)} (每组 {len(competitors[0]['items'])} items)")
print(f"  - 总竞品数: {total}")
print(f"  - hotProducts: {len(hot_products)}")
print(f"  - sources: {len(sources)}")
print(f"  - dataSource: {vs_data['dataSource']}")