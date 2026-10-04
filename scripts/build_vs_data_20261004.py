#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vs_data_20261004.py — 生成 2026-10-04 的 vs-data.json

竞品数据全部来自 WebSearch 真实抓取, 无编造数字。
每个 competitor group 的 items[0] = 今日主推商品(与 data.json 一致)。
"""
import json
import os

TODAY = "2026-10-04"
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{TODAY}"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"

sources = [
    f"小红书电商学习中心《小红书种草学:2026 年小红书双11 趋势分析》(187 页) sgpjbg.com/labels/xiaohongshushuang11qushifenxi/1/7605461.html ({TODAY} 抓取)",
    "爱美日记《2026年10月可卸内羽绒服销量排行榜》 am10.com/Nyp5Su759675FaY542Y5v_Y5/xl (2026-10 抓取)",
    "爱美日记《2026年10月恒源祥新款羊毛衫女旗舰店销量排行榜》 am10.com/Xqb5wiI6Xep5zWa5rGK6b_q5K675_yq5wap5lW65Qqr5SGo5/xl (2026-10 抓取)",
    "爱美日记《2026年10月女羊绒衫V领加厚销量排行榜前10名》 am10.com/gmOWOoKWOIGKa62Byqhiuk7eui_eOIzWa5/xl (2026-10 抓取)",
    "什么值得买 澳佳宝深海鱼油券后 ¥205 smzdm.com/p/183334012 · smzdm.com/p/183332236 (2026-10 抓取)",
    "什么值得买 沃隆每日坚果万福心意礼券后 ¥69.9 smzdm.com/p/183354910 (2026-10 抓取)",
    "什么值得买 良品铺子每日坚果纯坚果礼盒券后 ¥69 smzdm.com/p/183375301 · smzdm.com/p/183243719 (2026-10 抓取)",
    "腾讯新闻《2026 高性能除螨仪大盘点，有线无线全覆盖》 new.qq.com/rain/a/20261001A06UP300 (2026-10-01 抓取)",
    "腾讯搜一搜《除螨仪吸力要多大才能有用？2026 年十款除螨仪实测》 ·《2026年家用除螨仪十大排名榜》 (2026-10-02 抓取)",
    "CNPP《2026 十大受欢迎的羊毛衫品牌》 m.cnpp.cn/focus/3529553.html (2026 榜单)",
    "新浪财经《冲锋衣质量耐用内行人道出实情》cj.sina.com.cn/articles/view/7880068200/1d5b04c6802001pbis (2026-10 抓取)",
    "什么值得买《十月金秋囤货指南：这8件平价好物闭眼入》post.m.smzdm.com/p/aom98x2n (2026-10 抓取)",
]

competitors = [
    {
        "product": "可拆卸内胆羽绒服 / 三合一冲锋衣  ¥280-960 档",
        "items": [
            {
                "name": "雪中飞 连帽内胆可脱卸鹅绒羽绒服 新国标90鹅绒 一衣三穿",
                "price": "¥429",
                "advantage": "新国标 90 鹅绒 + 内胆可拆卸，一衣三穿从 10 月穿到次年 2 月；月销 1万+",
                "jd_sales": "爱美日记 2026年10月可卸内羽绒服销量榜 TOP2 · 月销 1万+",
                "color": "#1C3A5F",
                "image": f"{IMG_BASE}_product_1.jpg",
            },
            {
                "name": "骆驼 CAMEL 羽绒内胆三合一防水加绒三防冲锋衣 AD22263513Y 幻影黑",
                "price": "¥958",
                "advantage": "羽绒内胆 + 收腰版型对女性友好，防水面料无噪音，适合南方湿冷",
                "jd_sales": "京东月销量 4000 · 好评率 97%",
                "color": "#3A3A3A",
                "image": None,
            },
            {
                "name": "拓路者 青鸟冲锋衣三合一 抓绒内胆 户外防风防水登山服",
                "price": "¥699",
                "advantage": "硬壳面料防刮耐磨，内胆肉眼可见的厚，零度环境单穿够用，口袋多且深",
                "jd_sales": "京东月销量 2000 · 好评率 99%",
                "color": "#4A5D3A",
                "image": None,
            },
            {
                "name": "思凯乐 SCALER 破域Warm 软壳衣 内胆加绒连帽外套",
                "price": "¥539",
                "advantage": "软壳面料弹性好不束缚，抗静电，秋冬穿脱不噼里啪啦",
                "jd_sales": "京东好评率 100%",
                "color": "#2F4858",
                "image": None,
            },
        ],
    },
    {
        "product": "深海鱼油 Omega-3 补充剂  ¥160-490 档",
        "items": [
            {
                "name": "澳佳宝 Blackmores 深海鱼油胶囊 无腥味 Omega-3 400粒*2瓶",
                "price": "¥205 (约 ¥102.5/瓶)",
                "advantage": "无腥味工艺好吞，400 粒大瓶×2 券后单粒不到 0.26 元，澳洲 80 年+ 品牌",
                "jd_sales": "京东全球购好评率 98% · 京东自营好评率 100% · 500+ 条评论",
                "color": "#0F4C81",
                "image": f"{IMG_BASE}_product_2.jpg",
            },
            {
                "name": "澳佳宝 高浓度迷你鱼油 400粒 柠檬味无腥",
                "price": "¥180 (历史低价 ¥165)",
                "advantage": "单粒 0.45 元，柠檬味无腥适合怕鱼腥的长辈，历史低价常在 165 元",
                "jd_sales": "京东自营好评率 100%",
                "color": "#B8860B",
                "image": None,
            },
            {
                "name": "GNC 健安喜 Omega-3 四倍铂金深海鱼油 240粒*3件",
                "price": "¥387 (约 ¥129/瓶)",
                "advantage": "rTG 形式鱼油三倍吸收率，每份 EPA+DHA 高达 1200mg，四倍浓缩",
                "jd_sales": "京东国际自营旗舰店白菜价 387 元包邮",
                "color": "#8B0000",
                "image": None,
            },
            {
                "name": "诺特兰德 DHA 藻油 ARA 专研版 100粒",
                "price": "¥169",
                "advantage": "藻油纯度 53% 属行业上游，每粒 DHA 100mg + ARA 100mg，无鱼腥无重金属富集",
                "jd_sales": "贾乃亮推荐版 · 老爸评测母婴店渠道",
                "color": "#1E6F5C",
                "image": None,
            },
        ],
    },
    {
        "product": "羊毛衫 / 针织衫 女  ¥130-350 主力段",
        "items": [
            {
                "name": "恒源祥 套头女士羊毛衫 绵羊毛半高领针织衫",
                "price": "¥236",
                "advantage": "半高领套头打底外穿两用，套大衣不显臃肿；同价位段月销 6000+",
                "jd_sales": "爱美日记 2026年10月恒源祥女装旗舰店销量榜 TOP2 · 月销 6000+",
                "color": "#C4A484",
                "image": f"{IMG_BASE}_product_3.jpg",
            },
            {
                "name": "恒源祥 绵羊毛针织开衫 V领上衣",
                "price": "¥198",
                "advantage": "开衫版型可当外套单穿，V 领显脸小，同店月销 300+",
                "jd_sales": "爱美日记 2026年10月恒源祥女装旗舰店销量榜 TOP6 · 月销 300+",
                "color": "#9C8B7A",
                "image": None,
            },
            {
                "name": "鄂尔多斯市 100% 纯羊毛衫女 秋冬半高领修身毛衣",
                "price": "¥138",
                "advantage": "纯羊毛修身款，品牌背书强，价格是恒源祥套头款的六折",
                "jd_sales": "爱美日记 2026年10月恒源祥女装旗舰店销量榜 TOP4 · 月销 1000+",
                "color": "#6B7B8C",
                "image": None,
            },
            {
                "name": "春竹世家 羊绒衫女 V领加厚打底衫 2026新款",
                "price": "¥348",
                "advantage": "真羊绒材质，CNPP 2026 羊毛衫品牌榜春竹品牌指数 88.5 排第 5",
                "jd_sales": "爱美日记 2026年10月女羊绒衫V领加厚榜 TOP4 · 月销 20+",
                "color": "#A0522D",
                "image": None,
            },
        ],
    },
    {
        "product": "每日坚果 / 混合坚果礼盒  ¥30-130 段",
        "items": [
            {
                "name": "沃隆 每日坚果 万福心意礼 1330g 大礼包",
                "price": "¥69.9 (活动价 ¥79.9, 满 49 减 10)",
                "advantage": "1330g 大规格，¥69.9 档单位克数比同类多出近一倍，囤货送礼两用",
                "jd_sales": "京东好评率 98%",
                "color": "#C1440E",
                "image": f"{IMG_BASE}_product_4.jpg",
            },
            {
                "name": "良品铺子 每日坚果纯坚果礼盒 750g/箱",
                "price": "¥69 (活动价 ¥109, 叠加满 99 减 10 + 99-30 券)",
                "advantage": "纯坚果无添加，规格 750g 略小但品牌自营口碑稳",
                "jd_sales": "京东自营好评率 100%",
                "color": "#D32F2F",
                "image": None,
            },
            {
                "name": "沃隆 团圆臻礼 1.4kg 混合零食大礼包",
                "price": "¥124 (活动价 ¥134, 满 49 减 10)",
                "advantage": "1.4kg 超大份量走中客单路线，适合节前囤一整箱",
                "jd_sales": "京东什么值得买实测好评",
                "color": "#B71C1C",
                "image": None,
            },
            {
                "name": "良品铺子 5款纯坚果 500g 罐装 干果礼盒",
                "price": "¥34.9 (降价前 ¥49, 降幅 29%)",
                "advantage": "罐装设计开口即食，复购型低价走量款",
                "jd_sales": "京东自营好评率 100%",
                "color": "#F57C00",
                "image": None,
            },
        ],
    },
    {
        "product": "除螨仪 无线/有线  ¥300-600 主力段",
        "items": [
            {
                "name": "米家 小米除螨仪 3Pro 无线 17000Pa LED数显",
                "price": "¥499",
                "advantage": "17000Pa + 72000 次/分三区拍打，LED 数显实时看尘螨数值，尘杯滤芯均可水洗",
                "jd_sales": "腾讯新闻 2026-10-01 除螨仪实测盘点 10 款主推机型之一",
                "color": "#5B6B7B",
                "image": f"{IMG_BASE}_product_5.jpg",
            },
            {
                "name": "希亦 RM1Pro 双擎震吸有线除螨仪",
                "price": "¥499",
                "advantage": "42000 次/分高频双滚刷 + 13000Pa，65℃ 恒温热风祛湿，有线动力不衰减",
                "jd_sales": "腾讯搜一搜 2026 实测天梯榜 深层除螨率评分 9.8 居首",
                "color": "#37474F",
                "image": None,
            },
            {
                "name": "云鲸 U50 除螨仪 58.5℃ 热熨灭螨",
                "price": "¥499",
                "advantage": "65000 次/分金属滚刷 + 15000Pa，月抛尘袋免洗不脏手，抗菌率超 99.99%",
                "jd_sales": "腾讯搜一搜 2026 除螨仪实测榜 推荐机型",
                "color": "#00838F",
                "image": None,
            },
            {
                "name": "美的 BC7 有线除螨仪 13800Pa 加宽吸口",
                "price": "¥495",
                "advantage": "204mm 加宽吸口单次覆盖面积大，42000 次/分拍打，大品牌售后网点多",
                "jd_sales": "腾讯搜一搜 2026 实测天梯榜 300-500 元段推荐",
                "color": "#1565C0",
                "image": None,
            },
        ],
    },
]

hot_products = [
    {
        "name": "雪中飞 连帽内胆可脱卸鹅绒羽绒服 新国标90鹅绒 一衣三穿",
        "category": "运动户外·深秋预热",
        "price": "¥429",
        "image": f"{IMG_BASE}_product_1.jpg",
        "sales": "爱美日记 2026年10月可卸内羽绒服销量榜 TOP2 · 月销 1万+ · 什么值得买同系列三合一款券后 ¥299",
        "platform": "天猫雪中飞旗舰店 / 京东自营",
    },
    {
        "name": "澳佳宝 Blackmores 深海鱼油胶囊 无腥味 Omega-3 400粒*2瓶",
        "category": "大健康·开门红蓄水",
        "price": "¥205 (约 ¥102.5/瓶)",
        "image": f"{IMG_BASE}_product_2.jpg",
        "sales": "京东全球购好评率 98% · 京东自营好评率 100% · 500+ 条评论 · 大健康双11 爆发系数 1.50x 居五大行业之首",
        "platform": "京东全球购 澳佳宝Blackmores海外旗舰店",
    },
    {
        "name": "恒源祥 套头女士羊毛衫 绵羊毛半高领针织衫",
        "category": "女装·秋冬修身廓形",
        "price": "¥236",
        "image": f"{IMG_BASE}_product_3.jpg",
        "sales": "爱美日记 2026年10月恒源祥女装旗舰店销量榜 TOP2 · 月销 6000+ · CNPP 2026 羊毛衫品牌指数 92.3 列第 2",
        "platform": "天猫恒源祥羊绒服饰旗舰店",
    },
    {
        "name": "沃隆 每日坚果 万福心意礼 1330g 大礼包",
        "category": "休食·10.12 双峰",
        "price": "¥69.9",
        "image": f"{IMG_BASE}_product_4.jpg",
        "sales": "京东好评率 98% · 什么值得买活动价 ¥79.9 → 满 49 减 10 → 实付 ¥69.9 · 休食双11 GMV 10.3 亿居第一",
        "platform": "京东沃隆旗舰店 / 天猫沃隆官方旗舰店",
    },
    {
        "name": "米家 小米除螨仪 3Pro 无线 17000Pa LED数显",
        "category": "家生活·换季焕新",
        "price": "¥499",
        "image": f"{IMG_BASE}_product_5.jpg",
        "sales": "腾讯新闻 2026-10-01 除螨仪实测盘点主推机型 · 17000Pa / 72000 次每分钟 / 6 重旋风过滤",
        "platform": "小米京东自营旗舰店 / 小米商城",
    },
]

vs_data = {
    "date": TODAY,
    "sources": sources,
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": "WebSearch 真实数据 · 2026-10-04 cron 自动化抓取",
    "updateTime": f"{TODAY} 07:30",
}

os.makedirs(OUT_DIR, exist_ok=True)
path = f"{OUT_DIR}/vs-data.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

# schema 校验
assert "hotProducts" in vs_data, "❌ 缺 hotProducts"
assert len(vs_data["hotProducts"]) == 5, "❌ hotProducts 必须 5 项"
assert "dataSource" in vs_data, "❌ 缺 dataSource"
assert "updateTime" in vs_data, "❌ 缺 updateTime"
for hp in vs_data["hotProducts"]:
    assert "image" in hp and hp["image"].startswith("https://"), f"❌ hotProducts 缺 image: {hp.get('name')}"
for c in vs_data["competitors"]:
    assert c["items"][0].get("image", "").startswith("https://"), f"❌ {c['product']} 主推商品缺 image"

print(f"✅ vs-data.json 已生成: {path}")
print(f"  sources: {len(sources)} 条")
print(f"  competitors: {len(competitors)} 组, 共 {sum(len(c['items']) for c in competitors)} 个竞品")
print(f"  hotProducts: {len(hot_products)} 项 (全部含 image)")
print("✅ vs-data.json schema 校验通过")
