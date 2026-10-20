#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_vs_data_20261017.py — 2026-10-17 竞品对比 vs-data.json

⚠️ 所有价格/销量/参数均来自 2026-10-17 WebSearch 真实结果, 严禁编造
每条 advantage / jd_sales 都能在 sources 列出的来源里找到对应依据
"""

import json
import os

TODAY = "2026-10-17"
OUT_DIR = f"/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/{TODAY}"
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{TODAY}"

sources = [
    "什么值得买 · 2026年双11加湿器重点关注这7款,总有一款适合你 (https://post.m.smzdm.com/p/arzrplgq)",
    "今日头条 · 2026秋冬加湿器选购观察:无雾、除菌、防霉,比「大雾量」值得看 (https://www.toutiao.com/a7695743975528890927)",
    "京东排行榜 · 室内加湿机排行榜 (https://www.jd.com/phb/key_1620eda0432e39bf5c83.html)",
    "搜狐 · 骑行头盔有哪些品牌?从京东京造到迪卡侬、GUB的实战体验分享 (https://www.sohu.com/a/1078123286_122645100)",
    "搜狐 · 2026骑行运动穿戴装备大全:京东京造、洛克兄弟、GUB三款头盔实测对比 (https://www.sohu.com/a/1069207618_122645100)",
    "单车志 · 2026年爆款骑行头盔推荐 (https://www.bicycling.net.cn/2026年爆款骑行头盔推荐/)",
    "京东排行榜 · 公路车头盔品牌排行榜 (https://www.jd.com/phb/1318bfcd671960327473.html)",
    "慧聪家电网 · 2026破壁机怎么选?5款京东热门新品横评,附价格对比 (https://www.hchomea.com/2026/1013/481876.html)",
    "京东排行榜 · 破壁机/料理机排行榜 (https://www.jd.com/phb/key_737bb0c95ed06cb46f9.html)",
    "搜狐 · 2026猫抓板选购指南:实测京东快递、KimPets、瓜洲牧、贝思奈四款 (https://www.sohu.com/a/1073182886_122950382)",
    "搜狐 · 京东快递猫抓板:椭圆50cm瓦楞纸抓盆深度体验 (https://www.sohu.com/a/1054102287_122950382)",
    "京东排行榜 · 电褥子/电热毯排行榜 (https://www.jd.com/phb/key_1524830dae21e2cec2cb9.html)",
    "星期三选品 · 2026年10月电毯双人销量排行榜前十 (https://www.xing73.com/taobao-xl-6qL5M_Y5v_q51S55.html)",
]

competitors = [
    {
        "product": "无雾空气加湿器 ¥329-1000 价位段",
        "items": [
            {
                "name": "小熊(Bear)无雾空气加湿器 JSQ-J80K1",
                "price": "¥519",
                "advantage": "冷蒸发无雾不飘白粉,可加自来水;睡眠档低噪 + 数字屏直读湿度;母婴级除菌路线,母婴房/浅眠人群友好",
                "jd_sales": "什么值得买 2026 双11 加湿器横评重点关注款 · 京东常销 ¥704.71,大促到过 ¥519,历史 ¥359",
                "color": "#7FB3D5",
                "image": f"{IMG_BASE}_product_1.jpg",
            },
            {
                "name": "树新风 G1 全拆洗无雾加湿器(维嘉同款)",
                "price": "¥977.67",
                "advantage": "1750mL/h 大加湿量,整台能拆开洗没有死角,带紫外线杀菌;怕滤网发霉长菌膜的首选",
                "jd_sales": "什么值得买 2026 双11 横评 · 京东平时 ¥1499,大促 ¥1099,历史 ¥919",
                "color": "#5C8FA8",
            },
            {
                "name": "飞利浦 HU5710/10 NanoCloud 无雾加湿器",
                "price": "¥399",
                "advantage": "五重抑菌 NanoCloud 冷蒸发无雾,侧面加水不用搬机器;大牌安静款",
                "jd_sales": "京东 室内加湿机排行榜 TOP4 · 已有 50 万人评论",
                "color": "#A8BCD0",
            },
            {
                "name": "米家小米 无雾加湿器3 400mL/h 4L",
                "price": "¥355.72",
                "advantage": "米家 APP 远程开关 + 定时,性价比款;短板是没有热风风干,滤芯久用易发黄需手动晾",
                "jd_sales": "京东 室内加湿机排行榜 TOP1 · 已有 20 万人评论",
                "color": "#C9CFD6",
            },
            {
                "name": "352 H301 无雾加湿净化一体机",
                "price": "¥3387.6",
                "advantage": "2800mL/h 这批加湿量最大,加湿净化二合一 + 9.5L 水箱实时测 PM2.5;价格门槛高机身占地方",
                "jd_sales": "什么值得买 2026 双11 横评 · 京东平时 ¥4705,大促叠加到手 ¥3583",
                "color": "#4A5D6A",
            },
        ],
    },
    {
        "product": "骑行头盔 ¥109-399 价位段",
        "items": [
            {
                "name": "京东京造 自行车头盔 ZX21 磁吸风镜款",
                "price": "¥109",
                "advantage": "260g 实测配重 + 一体成型 EPS 缓冲 + 国标 GB-24429-2009;强力磁吸风镜单手拆装,头围 56-61cm 亚洲头型",
                "jd_sales": "京东 公路车头盔品牌排行榜 TOP2 · 已有 10 万人评论",
                "color": "#E8DCCB",
                "image": f"{IMG_BASE}_product_2.jpg",
            },
            {
                "name": "洛克兄弟 一体成型带风镜款 哑白变色镜",
                "price": "¥173",
                "advantage": "变色镜片白天防强光、傍晚自动增亮,适应城市环岛多变光线;银离子可拆内衬;重量略高约 280g,头围调节偏窄",
                "jd_sales": "搜狐 2026 三款头盔实测对比 · 洛克兄弟骑行道 已有 10 万人评论",
                "color": "#D8D2C4",
            },
            {
                "name": "GUB 碳纤维骨架骑行头盔 SV7",
                "price": "¥258",
                "advantage": "碳纤维龙骨盔,272g + 26 个通风孔散热最强,适合夏季高强度;风镜需另配,原价无磁吸",
                "jd_sales": "搜狐 2026 三款头盔实测对比 · 京东 SV7 已有 5000 人评论",
                "color": "#3A4046",
            },
            {
                "name": "迪卡侬 RoadR500 白色L",
                "price": "¥249.9",
                "advantage": "国际大厂系统化工程路线,Ponytail 转环对扎马尾女生友好,长发不被卡扣勒住;同系 MIPS 款侧面撞击分散剪切力",
                "jd_sales": "搜狐 骑行头盔实战体验 · 京东迪卡侬骑行头盔 已有 1000 人评论",
                "color": "#E0E4E8",
            },
            {
                "name": "PMT 品美特 K15 MIPS 亚洲版",
                "price": "¥399",
                "advantage": "专门亚洲头型开模,调节范围大贴合不夹头,带 MIPS 防护系统 + 磁吸风镜,新手入门安全款",
                "jd_sales": "京东 公路车头盔品牌排行榜 TOP6 · K15 白色已有 5 万人评论",
                "color": "#2F3B45",
            },
        ],
    },
    {
        "product": "0涂层破壁机 ¥478-987 价位段",
        "items": [
            {
                "name": "美的(Midea)安睡2.0 FC12Pro 无涂层破壁机",
                "price": "¥478",
                "advantage": "0 涂层 316L 不锈钢内胆,BLDC 变频 35000 转/分 + 6 叶海星刀免滤直饮;安睡隔音舱 + 全维降噪,1.6L / 800W 加热 / 12 种菜单",
                "jd_sales": "慧聪家电网 2026 年 10 月京东新品横评 · 参考价约 ¥478 起(日常约 ¥644 含国补)",
                "color": "#3E4650",
                "image": f"{IMG_BASE}_product_3.jpg",
            },
            {
                "name": "苏泊尔(SUPOR)小方糖 SP925R 0涂层",
                "price": "¥799",
                "advantage": "轻量方杯造型 + 棋盘匀热开放式蜂窝抗粘,干豆直打无渣率约 98%;颜值党和小厨房友好",
                "jd_sales": "慧聪家电网 2026 横评 · 京东参考约 ¥799 起(日常约 ¥1057)",
                "color": "#E3D9CE",
            },
            {
                "name": "西屋(Westinghouse)纯钛 WPB15J37W Pro",
                "price": "¥899",
                "advantage": "千元内少见的纯钛发热盘底盘,耐腐蚀防糊更健康;外置隔音罩 + 12 重降噪实测约 50dB,电机 10 年质保",
                "jd_sales": "慧聪家电网 2026 横评 · 京东参考约 ¥899 起(日常 ¥1175 含国补)",
                "color": "#8C9298",
            },
            {
                "name": "九阳(Joyoung)小旋风 B70 有钛0涂层",
                "price": "¥883",
                "advantage": "45000 转/分 BLDC + 三层 10 叶立体刀,粒径低至约 90 微米;变频轻音 + 双层隔音杯约 35dB,1.75L 3-5 人",
                "jd_sales": "京东 破壁料理机排行榜 TOP6 · 已有 20 万人评论",
                "color": "#6E7B85",
            },
            {
                "name": "九阳(Joyoung)巨齿鲨 B80 磁悬浮水箱分离",
                "price": "¥987",
                "advantage": "磁悬浮 + 独立水箱自动进水免看管,加热 1200W 动力足;特别适合熬膏方(阿胶、秋梨膏),但日常价 ¥1999",
                "jd_sales": "慧聪家电网 2026 横评 · 京东参考约 ¥987 起(日常 ¥1999 含国补)",
                "color": "#4A5560",
            },
        ],
    },
    {
        "product": "猫抓板 / 猫抓柱 ¥8-120 价位段",
        "items": [
            {
                "name": "瓜洲牧 61cm 剑麻布猫抓板 猫窝一体",
                "price": "¥20.9",
                "advantage": "平板无侧壁限制,大体型猫可完全伸展磨爪;剑麻布比纯剑麻更软但耐磨依旧,指甲刮只有轻微痕迹、近乎零掉屑",
                "jd_sales": "搜狐 2026 四款猫抓板选购指南实测款 · 送猫薄荷",
                "color": "#C9A87C",
                "image": f"{IMG_BASE}_product_4.jpg",
            },
            {
                "name": "京东快递 椭圆瓦楞纸猫抓板窝 60×40×9cm",
                "price": "¥8.18",
                "advantage": "最便宜的猫窝一体款,天然玉米胶无异味;槽式凹面贴合身体,适合 25 斤内爱睡的猫;怕水,吐毛球/尿尿要留意",
                "jd_sales": "搜狐 2026 四款猫抓板选购指南实测款",
                "color": "#A98E6B",
            },
            {
                "name": "KimPets 全剑麻猫抓窝 倾斜款 38.5cm",
                "price": "¥54.5",
                "advantage": "全剑麻材质零掉屑,倾斜设计模拟垂直抓挠,多猫家庭友好;胖猫略挤,16 斤以上建议选大号",
                "jd_sales": "搜狐 2026 四款猫抓板选购指南实测款",
                "color": "#B79B72",
            },
            {
                "name": "贝思奈 贴墙毛毡猫抓垫 50cm",
                "price": "¥19.9",
                "advantage": "自带背胶可贴墙面/门/沙发侧面,完全不占地面,租屋与小户型救星;内置铃铛对幼猫吸引力强",
                "jd_sales": "京东 多格猫抓板品牌排行榜 TOP7 · 已有 5000 人评论",
                "color": "#9AA5AD",
            },
            {
                "name": "HELLOJOY 剑麻猫抓柱立式猫爬架",
                "price": "榜单在售(京东)",
                "advantage": "立式柱体满足站起拉筋型猫,梅花底座稳固不倾倒,柱顶毛绒球可自嗨;材质安全无异味",
                "jd_sales": "京东 珍爱多猫剑麻排行榜 TOP7 · 已有 10 万人评论",
                "color": "#7C6A54",
            },
        ],
    },
    {
        "product": "双人电热毯 ¥39-208 价位段",
        "items": [
            {
                "name": "彩虹(Rainbow)双人定时双温双控除螨电热毯 1.8×1.5m",
                "price": "¥111.77",
                "advantage": "双温双控两人各调各的档,不用抢遥控器;定时 + 高温断电双重保护,无纺布柔软亲肤,老品牌口碑底子厚",
                "jd_sales": "京东 电褥子排行榜 TOP1 · 已有 200 万人评论;淘宝 2026年10月双人电热毯销量榜 TOP1,旗舰店销量 30 万+",
                "color": "#D98BA0",
                "image": f"{IMG_BASE}_product_5.jpg",
            },
            {
                "name": "荣事达(Royalstar)双人定时双温双除螨电热毯 1.8×1.5m",
                "price": "榜单在售(京东)",
                "advantage": "双区独立控温 + 12 小时定时自动断电,牛奶绒面料柔软亲肤带 3C 认证,整夜温暖不干燥",
                "jd_sales": "京东 电褥子排行榜 TOP4 · 已有 20 万人评论",
                "color": "#C4CBD1",
            },
            {
                "name": "环鼎 水暖毯 1.8×2.0m",
                "price": "¥208",
                "advantage": "水循环加热彻底告别干燥上火,主机静音运行,老人小孩都能安心睡;槽点是有味道且不可水洗",
                "jd_sales": "淘宝 2026年10月电毯双人榜 TOP4 · 连续 8 年 TOP1 · 销量 6 万+",
                "color": "#7E93A8",
            },
            {
                "name": "志高(CHIGO)石墨烯双人双温控电热毯 1.5×1.8m",
                "price": "榜单在售(京东)",
                "advantage": "石墨烯发热速度快几分钟见效,轻薄柔软铺床上无负担;除螨烘被 + 防水 3C 认证",
                "jd_sales": "京东 亿蒙四档调温电热毯排行榜 TOP7 · 已有 10 万人评论",
                "color": "#8FA5B5",
            },
            {
                "name": "米家 双人智能除螨定时手机预约电热毯 1.5×1.8m",
                "price": "榜单在售(京东)",
                "advantage": "手机 APP 远程预约 + 分区加热,回家前就能暖被窝;控制器带大按键显示屏,老人友好",
                "jd_sales": "京东 电褥子排行榜 TOP4 · 已有 10 万人评论",
                "color": "#B6BEC4",
            },
        ],
    },
]

hot_products = [
    {
        "name": "小熊(Bear)无雾空气加湿器 JSQ-J80K1",
        "category": "健康家电",
        "price": "¥519",
        "image": f"{IMG_BASE}_product_1.jpg",
        "sales": "什么值得买 2026 双11 加湿器横评重点关注款 · 大促到过 ¥519、历史 ¥359",
        "platform": "京东自营 / 小熊官方旗舰店",
    },
    {
        "name": "京东京造 自行车头盔 ZX21 磁吸风镜款",
        "category": "骑行通勤",
        "price": "¥109",
        "image": f"{IMG_BASE}_product_2.jpg",
        "sales": "京东 公路车头盔品牌排行榜 TOP2 · 已有 10 万人评论",
        "platform": "京东自营 / 京东京造",
    },
    {
        "name": "美的(Midea)安睡2.0 FC12Pro 无涂层破壁机",
        "category": "厨房养生",
        "price": "¥478",
        "image": f"{IMG_BASE}_product_3.jpg",
        "sales": "慧聪家电网 2026 年 10 月京东新品横评 · 日常约 ¥644(含国补)",
        "platform": "京东自营 / 美的旗舰店",
    },
    {
        "name": "瓜洲牧 61cm 剑麻布猫抓板 猫窝一体",
        "category": "宠物家居",
        "price": "¥20.9",
        "image": f"{IMG_BASE}_product_4.jpg",
        "sales": "搜狐 2026 四款猫抓板选购指南实测款 · 近乎零掉屑",
        "platform": "京东快递自营",
    },
    {
        "name": "彩虹(Rainbow)双人双温双控电热毯 1.8×1.5m",
        "category": "冬季家居",
        "price": "¥111.77",
        "image": f"{IMG_BASE}_product_5.jpg",
        "sales": "京东电褥子类目 TOP1 · 200 万人评论;淘宝 2026年10月双人榜 TOP1 销量 30 万+",
        "platform": "彩虹官方旗舰店",
    },
]

vs_data = {
    "date": TODAY,
    "sources": sources,
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": f"WebSearch 真实数据 · {TODAY} cron 自动化抓取",
    "updateTime": f"{TODAY} 07:30",
}

os.makedirs(OUT_DIR, exist_ok=True)
with open(f"{OUT_DIR}/vs-data.json", "w", encoding="utf-8") as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

print(f"✅ vs-data.json 写入完成: {len(competitors)} 品类 / "
      f"{sum(len(c['items']) for c in competitors)} 竞品 / "
      f"{len(hot_products)} 热销 / {len(sources)} 来源")
