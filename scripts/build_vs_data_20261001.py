#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-01 xhs-product-push vs-data.json 生成器
竞品数据全部来自 2026-10-01 WebSearch 真实抓取的京东排行榜页, 严禁编造
"""
import json
import os

TASK_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push"
TODAY = "2026-10-01"
OUT_DIR = os.path.join(TASK_DIR, "output", TODAY)
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{TODAY}"

with open(os.path.join(OUT_DIR, "data.json"), encoding="utf-8") as f:
    data = json.load(f)
by_id = {p["id"]: p for p in data["products"]}

sources = [
    "咸宁网《2026国庆长途游行李箱选购攻略 读懂材质尺寸从容应对长假出行》(xnnews.com.cn, 2026-08-27 刊发, 2026-10-01 抓取)",
    "廊坊新闻网《2026国庆出游行李箱学生党选购指南 平价性价比尺寸避坑》(lfnews.cn, 2026-10-01 抓取)",
    "京东 投影仪1000元品牌排行榜 (jd.com/phb/6700a1aacd99947a3b1.html, 2026-10-01 抓取)",
    "京东 全高清1080p投影排行榜 + 6高清投影机排行榜 (jd.com/phb, 2026-10-01 抓取)",
    "京东 秋衣秋裤加厚女士排行榜 (jd.com/phb/key_1315bfc1e93788b3d315.html, 2026-10-01 抓取)",
    "京东 黄山名茶排行榜 (jd.com/phb/key_1320556f15880721ed35.html, 2026-10-01 抓取)",
    "京东 毛尖茶叶盒排行榜 (jd.com/phb/key_619632c910c041045a9a.html, 2026-10-01 抓取)",
    "京东 开水保温杯排行榜 (jd.com/phb/key_6196368ca98efa7c7da4.html, 2026-10-01 抓取)",
]

competitors = [
    {
        "product": "长途托运行李箱 300-600 元区间",
        "items": [
            {
                "name": by_id[1]["name"],
                "price": by_id[1]["price"],
                "advantage": (
                    "德国科思创100%纯PC + 铝镁合金全铝框，抗摔抗压，曾参与消保委箱包测评；"
                    "全覆盖金属防撞护角 + 铆钉加固边角；加宽TPE橡胶双排静音万向轮；"
                    "铝合金拉杆9000次耐久；嵌入式TSA海关锁；干湿分离仓 + 隐形扩容"
                ),
                "jd_sales": "咸宁网 2026 国庆箱包选购攻略参考款，市场累计销量较高（无公开具体评价数）",
                "color": by_id[1]["color"],
                "image": by_id[1]["image"],
            },
            {
                "name": "90分 商旅两用 90171STZGUN 行李箱 28英寸",
                "price": "¥329-¥559",
                "advantage": "德国科思创PC材质，抗凹陷表现优秀；双排TPE静音万向轮；三段可调铝合金拉杆；标配TSA海关锁",
                "jd_sales": "咸宁网 2026 国庆箱包选购攻略参考款",
                "color": "#3F4A5A",
            },
            {
                "name": "外交官 TC-6012 行李箱 20-28英寸",
                "price": "¥288-¥480",
                "advantage": "老牌旅行用品厂商经典型号，自带隐藏扩容层；加厚铝合金拉杆；双排八轮静音万向轮；独立干湿分离网袋",
                "jd_sales": "咸宁网 2026 国庆箱包选购攻略参考款",
                "color": "#5A5A5A",
            },
            {
                "name": "京东京造 飞行家 拉链硬箱 24英寸",
                "price": "¥218-¥340",
                "advantage": "一体成型PP材质，抗冲击回弹；航空级铝合金拉杆；双排飞机轮通过6倍国标耐久测试；下沉式TSA海关锁",
                "jd_sales": "廊坊新闻网 2026 学生党选购指南推荐款",
                "color": "#4E6E8E",
            },
        ],
    },
    {
        "product": "家用云台投影仪 1000 元以内档",
        "items": [
            {
                "name": by_id[2]["name"],
                "price": by_id[2]["price"],
                "advantage": (
                    "自动对焦快，白墙直投清晰、色彩还原自然；一体式自带音响不用外接；"
                    "系统流畅手机投屏几乎无卡顿；机身小巧噪音低，适配卧室/租房小户型"
                ),
                "jd_sales": "京东投影仪1000元品牌排行榜 TOP7 · 已有5000人评论",
                "color": by_id[2]["color"],
                "image": by_id[2]["image"],
            },
            {
                "name": "大眼橙 C3 Pro 云台投影仪 570CVIA TOF对焦 1080P",
                "price": "京东 1000 元档 TOP2",
                "advantage": "570CVIA 亮度高于追光Pro一档，TOF 自动对焦，用户评价「期待使用效果」",
                "jd_sales": "京东投影仪1000元品牌排行榜 TOP2 · 已有100000人评论",
                "color": "#4B5563",
            },
            {
                "name": "小米投影仪 REDMI 5 400CVIA 一体式金属云台 便携投影仪",
                "price": "京东 1000 元档 TOP1",
                "advantage": "一体式金属云台 360° 调节 + ToF 激光感知；评价称躺着投天花板很爽，自动对焦快",
                "jd_sales": "京东投影仪1000元品牌排行榜 TOP1 · 已有200000人评论",
                "color": "#3B3B3B",
            },
            {
                "name": "哈趣 Q1 Pro 高亮版 570CVIA 云台投影仪",
                "price": "京东 1000 元档 TOP3",
                "advantage": "哈曼联名款，570CVIA 亮度，白墙/开灯效果均清晰，外形小巧美观",
                "jd_sales": "京东投影仪1000元品牌排行榜 TOP3 · 已有10000人评论",
                "color": "#5B5F6B",
            },
        ],
    },
    {
        "product": "加绒保暖内衣套装 100-300 元区间",
        "items": [
            {
                "name": by_id[3]["name"],
                "price": by_id[3]["price"],
                "advantage": "7A抗菌等级；棉感亲肤，薄绒加厚保暖不臃肿；贴身版型套毛衣不鼓包；百搭色系",
                "jd_sales": "京东秋衣秋裤加厚女士排行榜 TOP1 · 已有100000人评论",
                "color": by_id[3]["color"],
                "image": by_id[3]["image"],
            },
            {
                "name": "恒源祥 加绒加厚秋衣秋裤 棉套装 男女",
                "price": "京东 热销 50W 档",
                "advantage": "老牌性价比路线，销量规模最大；有用户反馈领口偏长略透风",
                "jd_sales": "京东秋衣秋裤加厚女士排行榜 · 已有500000人评论（标注【热销50W】）",
                "color": "#8B5A2B",
            },
            {
                "name": "红豆 羊毛加绒加厚抗菌磨毛 中高领保暖内衣套装 女",
                "price": "京东 中端价位",
                "advantage": "羊毛加绒 + 抗菌磨毛中高领，锁温性能好，轻盈不臃肿，洗后不变形",
                "jd_sales": "京东秋衣秋裤加厚女士排行榜 · 已有100000人评论",
                "color": "#9B2C2C",
            },
            {
                "name": "都市丽人 德绒发热保暖内衣 含羊绒蚕丝 加绒加厚套装",
                "price": "京东 中端价位",
                "advantage": "德绒发热面料主打轻薄发热路线，有用户称比去年厚加绒还暖且不臃肿",
                "jd_sales": "京东秋衣秋裤加厚女士排行榜 · 已有20000人评论",
                "color": "#D4A5A5",
            },
        ],
    },
    {
        "product": "中秋国庆茶叶礼盒 150-350 元区间",
        "items": [
            {
                "name": by_id[4]["name"],
                "price": by_id[4]["price"],
                "advantage": "黄山毛峰老字号；茶汤清亮香气清幽持久、入口鲜爽回甘；独立小袋分装；红色窗棂纹样喜庆礼盒",
                "jd_sales": "京东黄山名茶排行榜 / 松德黄茶排行榜多款在榜",
                "color": by_id[4]["color"],
                "image": by_id[4]["image"],
            },
            {
                "name": "天之红 1915 祁门红茶 祁红工夫 特级 200g 茶叶礼盒",
                "price": "京东 中端价位",
                "advantage": "红茶送礼路线，祁门蜜香；评价称「送长辈送领导，不张扬不跌份」",
                "jd_sales": "京东黄山名茶排行榜 TOP1 · 已有50000人评论",
                "color": "#8B4513",
            },
            {
                "name": "福茗源 黄山毛峰 500g 特级二等 明前 2026新茶 头采 茶叶礼盒",
                "price": "京东 中端价位",
                "advantage": "500g 大规格头采春茶，评价称包装精美物美价廉，口粮茶路线",
                "jd_sales": "京东黄山名茶排行榜 · 已有100000人评论",
                "color": "#4F7942",
            },
            {
                "name": "承道铭 信阳毛尖茶 2026新茶 明前特级 300g 中秋送礼礼盒",
                "price": "京东 中端价位",
                "advantage": "信阳毛尖品类送礼款，京东标注评论量级最高（300万+）",
                "jd_sales": "京东毛尖茶叶盒排行榜 · 已有3000000人评论",
                "color": "#556B2F",
            },
        ],
    },
    {
        "product": "便携恒温电热杯 100-250 元区间",
        "items": [
            {
                "name": by_id[5]["name"],
                "price": by_id[5]["price"],
                "advantage": "京东开水保温杯榜 TOP1；350ml 迷你体积 + 316L 不锈钢内胆 + 智能恒温，出差行李箱友好",
                "jd_sales": "京东开水保温杯排行榜 TOP1 · 已有500000人评论",
                "color": by_id[5]["color"],
                "image": by_id[5]["image"],
            },
            {
                "name": "米家 保温杯 316不锈钢 350ml 白色",
                "price": "京东 100 万+ 评价档",
                "advantage": "同门走日常保温杯路线，316 不锈钢内胆，评价量级最高（100万+），倒置不漏水",
                "jd_sales": "京东开水保温杯排行榜 · 已有1000000人评论",
                "color": "#E5E7EB",
            },
            {
                "name": "乐扣乐扣 电热水杯 烧水杯 400ml 便携式烧水壶",
                "price": "京东 中端价位",
                "advantage": "400ml 容量稍大，评价「性价比非常高」，乐扣乐扣品牌锁扣密封口碑好",
                "jd_sales": "京东开水保温杯排行榜 · 已有50000人评论",
                "color": "#4B6B4B",
            },
            {
                "name": "摩动 便携式烧水杯 650ml 316不锈钢 恒温壶",
                "price": "京东 中端价位",
                "advantage": "650ml 大容量适合家庭/多人，评价称同事出差在用、效果不错",
                "jd_sales": "京东开水保温杯排行榜 · 已有100000人评论",
                "color": "#6B7280",
            },
        ],
    },
]

hot_products = [
    {
        "name": by_id[1]["name"],
        "category": "长途托运行李箱",
        "price": by_id[1]["price"],
        "image": by_id[1]["image"],
        "sales": "咸宁网 2026 国庆箱包选购攻略参考款 · 曾参与消保委箱包测评 · 市场累计销量较高",
        "platform": "网易严选官方旗舰店 / 京东自营",
    },
    {
        "name": by_id[2]["name"],
        "category": "家用云台投影仪",
        "price": by_id[2]["price"],
        "image": by_id[2]["image"],
        "sales": "京东投影仪1000元品牌排行榜 TOP7 · 已有5000人评论",
        "platform": "京东自营 / 京东京造官方旗舰店",
    },
    {
        "name": by_id[3]["name"],
        "category": "加绒保暖内衣",
        "price": by_id[3]["price"],
        "image": by_id[3]["image"],
        "sales": "京东秋衣秋裤加厚女士排行榜 TOP1 · 已有100000人评论",
        "platform": "京东自营 / 蕉内官方旗舰店",
    },
    {
        "name": by_id[4]["name"],
        "category": "茶叶礼盒",
        "price": by_id[4]["price"],
        "image": by_id[4]["image"],
        "sales": "京东黄山名茶排行榜 / 松德黄茶排行榜在榜 · 已有20000人评论",
        "platform": "京东自营 / 谢裕大官方旗舰店",
    },
    {
        "name": by_id[5]["name"],
        "category": "便携恒温电热杯",
        "price": by_id[5]["price"],
        "image": by_id[5]["image"],
        "sales": "京东开水保温杯排行榜 TOP1 · 已有500000人评论",
        "platform": "京东自营 / 米家京东旗舰店",
    },
]

vs = {
    "date": TODAY,
    "sources": sources,
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": "WebSearch 真实数据 · 2026-10-01 cron 自动化抓取（京东排行榜 + 咸宁网/廊坊新闻网选购攻略）",
    "updateTime": f"{TODAY} 07:30",
}

out_path = os.path.join(OUT_DIR, "vs-data.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(vs, f, ensure_ascii=False, indent=2)

# schema 校验
with open(out_path, encoding="utf-8") as f:
    v = json.load(f)
assert "hotProducts" in v, "❌ vs-data.json 缺 hotProducts"
assert len(v["hotProducts"]) == 5, "❌ hotProducts 必须 5 项"
assert "dataSource" in v, "❌ vs-data.json 缺 dataSource"
assert "updateTime" in v, "❌ vs-data.json 缺 updateTime"
for hp in v["hotProducts"]:
    assert "image" in hp, f"❌ hotProducts 缺 image 字段: {hp.get('name')}"
    assert hp["image"].startswith("https://"), "❌ hotProducts image 必须 CDN URL"
for c in v["competitors"]:
    assert c["items"][0].get("image"), f"❌ 竞品主推缺 image: {c['product']}"

print(f"✅ vs-data.json 写入成功: {out_path}")
print(f"   来源 {len(v['sources'])} 个 | 竞品类目 {len(v['competitors'])} 个 | hotProducts {len(v['hotProducts'])} 项")
for c in v["competitors"]:
    print(f"   - {c['product']}: {len(c['items'])} 款")
