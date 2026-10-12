#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_vs_data_20261012.py — 生成 output/2026-10-12/vs-data.json

⚠️ 所有价格/销量数据均来自 2026-10-12 WebSearch 真实搜索结果,严禁编造
数据来源:
  - jd.com 京东排行榜 (纸尿裤 M 码榜 / 抽真空压缩袋榜 / 提花保暖内衣榜)
  - xing73.com 2026年10月淘宝猫粮销量排行榜
  - post.smzdm.com 什么值得买 日归露营四件核心装备横评 (2026年5月行情)
  - cnpp.cn 十大品牌网 2026 十大受欢迎纸尿裤品牌
  - h5detail.yiyouliao.com 易有料 2026 保暖内衣选购指南 (京东9月比价)
"""
import json
import os

DATE = "2026-10-12"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{DATE}"
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{DATE}"
os.makedirs(OUT_DIR, exist_ok=True)

sources = [
    "京东排行榜 jd.com/phb/key_1319cdc2709cb641a24f.html (纸尿裤M码榜)",
    "京东排行榜 jd.com/phb/key_16204117b92b2bfaf15e.html (抽真空压缩袋榜)",
    "京东排行榜 jd.com/phb/key_131591b4b419dea995a3.html (提花保暖内衣女榜)",
    "淘宝销量榜 xing73.com (2026年10月20斤/10斤猫粮销量排行)",
    "什么值得买 post.smzdm.com/p/ak8el999 (日归露营核心装备横评, 2026年5月行情)",
    "十大品牌网 cnpp.cn/focus/3529570 (2026十大受欢迎纸尿裤品牌)",
    "易有料 yiyouliao.com (2026秋衣秋裤保暖内衣选购指南, 京东2026年9月比价数据)",
]

competitors = [
    {
        "product": "宠物主粮 · 冻干猫粮 ¥200-400 段",
        "items": [
            {
                "name": "汪喵星球 天然低敏冻干主食餐 小方粒型 猫咪冻干 500g",
                "price": "¥350（500g）",
                "advantage": "天然低敏、小方粒型泡水 30 秒软化、常温保存免冷藏",
                "jd_sales": "淘宝 2026年10月销量榜冻干猫粮 TOP1 品类销量 40万+",
                "color": "#C97B4A",
                "image": f"{IMG_BASE}_product_1.jpg",
            },
            {
                "name": "怪獸部落 98%慢烘乾燥鮮肉主食糧 800g",
                "price": "¥980（800g）",
                "advantage": "98% 高肉含量慢烘工艺,台湾 momo 总销量 >1.5万",
                "jd_sales": "momo購物網 好评 1769 笔, 总销量 >1.5万",
                "color": "#8B5E3C",
            },
            {
                "name": "麦富迪 MYFOODIE 天然鱼油成猫粮 10kg",
                "price": "¥169（10kg 官方旗舰店）",
                "advantage": "国民品牌大包装性价比路线,鱼油美毛",
                "jd_sales": "淘宝销量榜 TOP8 麦富迪天然鱼油成猫粮 10kg 销量 6万+",
                "color": "#D4A574",
            },
            {
                "name": "醇粹 金标无谷低敏冻干成幼猫粮 10斤",
                "price": "¥75-161（10斤, 活动区间）",
                "advantage": "无谷低敏冻干,618/双11 活动价波动大",
                "jd_sales": "淘宝销量榜 TOP5/TOP8, 销量 9万-10万+",
                "color": "#C8A165",
            },
        ],
    },
    {
        "product": "家居收纳 · 真空压缩袋 ¥50-200 段",
        "items": [
            {
                "name": "京东京造 真空压缩收纳袋 家庭20件套 加厚棉被羽绒服 带电泵",
                "price": "¥69-159（20件套）",
                "advantage": "PA+PE 加厚 10-12 丝, 自带电泵, 20 件套一次搞定全家换季",
                "jd_sales": "京东压缩袋排行榜 TOP4, 已有 200000 人评论",
                "color": "#4A7C9E",
                "image": f"{IMG_BASE}_product_2.jpg",
            },
            {
                "name": "太力 真空压缩收纳袋 电动气泵抽真空 大容量11件",
                "price": "京东销量 NO.1 价位段",
                "advantage": "品类销量冠军, 11 件套 + 电动气泵组合",
                "jd_sales": "京东抽真空压缩袋榜 TOP1, 已有 1000000 人评论",
                "color": "#3D6B8E",
            },
            {
                "name": "收纳博士 真空压缩收纳袋 手泵9件套",
                "price": "手泵款",
                "advantage": "特厚材质, 放两个月不漏气回弹",
                "jd_sales": "京东压缩袋榜 TOP6, 已有 2000000 人评论 (评论量最高)",
                "color": "#5A8AA8",
            },
            {
                "name": "京东京造 真空封口机 双泵大吸力 80kPa 触屏款",
                "price": "配真空袋*10",
                "advantage": "双泵 80kPa 大吸力, 干湿两用, 但真空袋是后续消费大头",
                "jd_sales": "京东压缩袋榜 TOP9, 已有 20000 人评论",
                "color": "#6B8FA8",
            },
        ],
    },
    {
        "product": "秋冬季着 · 德绒保暖内衣 ¥60-180 段",
        "items": [
            {
                "name": "猫人 MiiOW 优品德绒羊毛蚕丝保暖内衣女套装 加厚无痕打底",
                "price": "¥80.9-119.9",
                "advantage": "羊毛+蚕丝+德绒三层复合, 无痕剪裁, 膝盖加厚",
                "jd_sales": "京东比价数据 2026年9月; 麦米网同款已抢 1万+",
                "color": "#B08968",
                "image": f"{IMG_BASE}_product_3.jpg",
            },
            {
                "name": "雅鹿 yaloo 女士德绒发热保暖内衣 2套",
                "price": "¥33.9-69.9（2套）",
                "advantage": "无痕发热 7A 抗菌, 性价比极高",
                "jd_sales": "淘宝 2026年9月榜单 TOP6/TOP8, 销量 700-800+",
                "color": "#9E7B5B",
            },
            {
                "name": "都市丽人 德绒含羊绒蚕丝保暖内衣",
                "price": "¥69.9（活动价）",
                "advantage": "德绒 + 羊绒蚕丝复合, 活动价性价比突出",
                "jd_sales": "易有料 2026 京东9月比价数据",
                "color": "#C4A484",
            },
            {
                "name": "蕉内 热皮系列 男女抗菌保暖套装",
                "price": "¥166（热皮 5 系背心 ¥107）",
                "advantage": "无痕剪裁和版型是强项, 年轻人复购率高",
                "jd_sales": "麦米网 蕉内热皮5系抗菌保暖背心已抢 4万+",
                "color": "#6B5B4F",
            },
        ],
    },
    {
        "product": "户外露营 · 黑胶天幕 ¥150-350 段",
        "items": [
            {
                "name": "挪客 Naturehike 20平黑胶天幕 速开遮阳挡雨",
                "price": "¥239",
                "advantage": "5分钟搭建, 3.2kg, 黑胶涂层防晒强五六度",
                "jd_sales": "什么值得买 2026年5月 日归露营横评主力款",
                "color": "#5B7C3F",
                "image": f"{IMG_BASE}_product_4.jpg",
            },
            {
                "name": "牧高笛 Mobi Garden 20平天幕",
                "price": "¥279",
                "advantage": "2.9kg 最轻, 保冷 36 小时保温箱配套, 整套 <10kg",
                "jd_sales": "什么值得买横评: 轻量化组合 ¥1045 整套",
                "color": "#6B8E4E",
            },
            {
                "name": "原始人 20平速开天幕",
                "price": "¥219",
                "advantage": "3分钟速开 (最快), 亲子家庭组合 ¥903 起点",
                "jd_sales": "什么值得买横评: 亲子家庭方案 ¥903 整套",
                "color": "#4F7040",
            },
            {
                "name": "探险者 20平天幕",
                "price": "¥199（最低价）",
                "advantage": "预算有限新手首选, 3.8kg 偏重适合开车去营地",
                "jd_sales": "什么值得买横评: 新手组合 ¥476 整套",
                "color": "#7A9455",
            },
        ],
    },
    {
        "product": "母婴护理 · 超薄纸尿裤 ¥80-260 段",
        "items": [
            {
                "name": "好奇 Huggies 铂金装小桃裤纸尿裤 M144片 透爽散热",
                "price": "¥199-259",
                "advantage": "花苞围腰不勒肚, 透爽散热表层, 京东 M 码榜 TOP1",
                "jd_sales": "京东纸尿裤 M 码榜 TOP1, 已有 5000000 人评论",
                "color": "#E8839A",
                "image": f"{IMG_BASE}_product_5.jpg",
            },
            {
                "name": "好奇 Huggies 小森林纸尿裤 M50片 心钻",
                "price": "心钻系列",
                "advantage": "透氧顶配, 更低敏",
                "jd_sales": "京东纸尿裤 M 码榜 TOP3, 已有 4000000 人评论",
                "color": "#7FB8A4",
            },
            {
                "name": "babycare 皇室狮子王国 弱酸纸尿裤 M50片",
                "price": "弱酸系列",
                "advantage": "弱酸配方亲肤透气",
                "jd_sales": "京东纸尿裤 M 码榜 TOP2, 已有 3000000 人评论",
                "color": "#F0B429",
            },
            {
                "name": "花王 妙而舒 Merries 纸尿裤 M64片",
                "price": "双11 80片装可降至百元以内",
                "advantage": "pH5.5 弱酸性面层中和尿液碱性刺激, 3D 透气膜",
                "jd_sales": "京东纸尿裤 M 码榜 TOP5, 已有 5000000 人评论",
                "color": "#D98CA0",
            },
        ],
    },
]

hot_products = [
    {
        "name": "汪喵星球 天然低敏冻干主食餐 小方粒型 500g",
        "category": "宠物主粮",
        "price": "¥350（500g）",
        "image": f"{IMG_BASE}_product_1.jpg",
        "sales": "淘宝 2026年10月冻干猫粮销量榜 TOP1 品类, 销量 40万+",
        "platform": "天猫旗舰店 / 京东旗舰店",
    },
    {
        "name": "京东京造 真空压缩收纳袋 家庭20件套 带电泵",
        "category": "家居收纳",
        "price": "¥69-159（20件套）",
        "image": f"{IMG_BASE}_product_2.jpg",
        "sales": "京东压缩袋排行榜 TOP4, 已有 200000 人评论",
        "platform": "京东自营",
    },
    {
        "name": "猫人 MiiOW 优品德绒羊毛蚕丝保暖内衣女套装",
        "category": "秋冬季着",
        "price": "¥80.9-119.9",
        "image": f"{IMG_BASE}_product_3.jpg",
        "sales": "京东 2026年9月比价 ¥80.9; 同款已抢 1万+",
        "platform": "京东自营 / 天猫旗舰店",
    },
    {
        "name": "挪客 Naturehike 20平黑胶天幕 速开遮阳挡雨",
        "category": "户外露营",
        "price": "¥239",
        "image": f"{IMG_BASE}_product_4.jpg",
        "sales": "什么值得买日归露营横评基准款 (3.2kg / 5分钟搭建)",
        "platform": "京东自营 / 天猫旗舰店",
    },
    {
        "name": "好奇 Huggies 铂金装小桃裤纸尿裤 M144片",
        "category": "母婴护理",
        "price": "¥199-259",
        "image": f"{IMG_BASE}_product_5.jpg",
        "sales": "京东纸尿裤 M 码排行榜 TOP1, 已有 5000000 人评论",
        "platform": "京东自营 / 京东旗舰店",
    },
]

vs_data = {
    "date": DATE,
    "theme": "深秋换季 + 双11 预售前夜(10/15 天猫预售)",
    "sources": sources,
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": "WebSearch 真实数据 · 2026-10-12 cron 自动化抓取",
    "updateTime": f"{DATE} 07:30",
}

out_path = f"{OUT_DIR}/vs-data.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

# ---- Schema 校验 ----
d = json.load(open(out_path, encoding="utf-8"))
assert d["dataSource"], "❌ 缺 dataSource"
assert d["updateTime"], "❌ 缺 updateTime"
assert len(d["hotProducts"]) == 5, f"❌ hotProducts 应为 5 项,实际 {len(d['hotProducts'])}"
for h in d["hotProducts"]:
    assert h.get("image", "").startswith("https://"), f"❌ hotProduct {h['name'][:20]} image 必须 CDN URL"
    assert h.get("sales"), f"❌ hotProduct {h['name'][:20]} 缺 sales"
for i, c in enumerate(d["competitors"]):
    assert c["items"], f"❌ competitors[{i}] items 为空"
    assert c["items"][0].get("image", "").startswith("https://"), f"❌ competitors[{i}] 第1项(主推)必须带 image"
assert len(d["sources"]) >= 5, "❌ sources 少于 5 条"

print(f"✅ vs-data.json schema 校验通过 → {out_path}")
print(f"   competitors: {len(d['competitors'])} 组, sources: {len(d['sources'])} 条, hotProducts: {len(d['hotProducts'])} 项")