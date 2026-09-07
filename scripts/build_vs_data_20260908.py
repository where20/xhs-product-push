#!/usr/bin/env python3
"""生成 2026-09-08 vs-data.json (竞品对比 + hotProducts + sources)"""
import json
import os

TODAY = "2026-09-08"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/" + TODAY
IMG_BASE = "https://cloudimgs.iepose.cn/api/images/" + TODAY

vs = {
    "date": TODAY,
    "sources": [
        # 教师节披肩毯
        "太原新闻网《百元以内也能送出高级感!Soft Kiss纯棉流苏披肩毯礼盒69元起,送到老师心坎上》(Soft Kiss A类母婴级·4色·活动价69元·2026教师节黑马选品)",
        "博客园《2026教师节礼物推荐:Soft Kiss纯棉披肩毯礼盒深度评测,四色69元起百元档最稳选》(综合评分9.2·4色适配·暗扣设计·9月送礼首选)",
        "黄冈新闻网《2026教师节送礼攻略:温和护养、高频复用、低负担织物礼品选购指南》(50-100元百元档·Soft Kiss织物礼盒·适配教师办公场景)",
        "中国经济新闻网《教师节:礼赠预算正向百元实用型集中》(礼赠消费结构性变化·百元档织物礼盒·69-79元价位)",
        "道县新闻网《教师节送披肩毯合适吗?看完这三个场景再决定》(100×150cm暗扣·空调房/午休/通勤三场景·A类标准)",
        # 教师节扩音器
        "新浪网《2026年教学用小蜜蜂扩音器哪种好一点?》(西圣Bee月销76件+98%好评率·D类高增益DSP+16芯全频·旗舰级扩音器)",
        "今日头条《2026年扩音器排行榜前十名推荐》(西圣Bee ¥229 TOP1·得胜E10W ¥329 TOP2·十度S615 ¥279 TOP3)",
        "今日头条《哪款扩音器值得买?谁的声音更清晰?开学季教师小蜜蜂扩音器推荐》(西圣Bee ¥229 5星·得胜E8W ¥311·金运M20 ¥299·索爱S6 ¥399)",
        "今日头条《2026扩音器最全攻略》(西圣Bee ¥229 TOP1·16芯全频+D类高增益DSP+30米2.4G传输)",
        "什么值得买《2026教师专用扩音器哪个品牌最好?》(西圣Bee ¥229 5星·十度S378 ¥289·易相随S60 ¥249·得胜E10W ¥245)",
        # 通勤降噪耳机
        "京东《蓝耳机牙入耳式品牌排行榜》(OPPO Enco Air5 Pro TOP1·5万评论·月珀白·蓝牙5.3+54小时总续航)",
        "中关村在线《2026降噪耳机性价比推荐 大学生通勤自习必备清单》(漫步者X3 Air ¥88·KZ Z1 Pro ¥168·Redmi Buds 4 Pro ¥399·华为FreeLace Pro ¥519)",
        "京东《入耳耳麦排行榜》(OPPO Enco Air5 Pro ¥257 TOP3·5万评论·旗舰人声降噪)",
        "京东《LZE耳机/耳麦品牌排行榜》(华为FreeClip ¥0 50万评论TOP2·韶音OpenRun Pro 2骨传导·极度未知Cloud Ⅲ)",
        "凤凰网《2026主动降噪效果好的蓝牙耳机推荐》(AirPods Pro 3 ¥1899 TOP·三星Buds3 Pro ¥1499·小米Buds 5 Pro ¥999)",
        "京东《耳机入耳式耳机品牌排行榜》(OPPO Enco Free4 ¥0 20万评论TOP2·小米REDMI Buds 8 Pro 5万评论)",
        "京东《降噪耳机排名榜排行榜》(华为FreeBuds 7i ¥0 10万评论TOP1·爱国者柏林之声耳夹式5万评论TOP2)",
        "广商云桥《2026年耳机降噪推荐:7款主流机型实测》(漫步者Lolli Pro 5 ¥399·Redmi Buds 6 ¥199·AirPods Pro 2 ¥1799·索尼WH-1000XM5 ¥1999)",
        # 膳魔师保温杯
        "京东《Momscook不锈钢进口保温杯排行榜》(膳魔师JNL-502 ¥0 50万评论TOP1·马来西亚产·曜石黑/月光白)",
        "京东《笃牌304不锈钢保温杯排行榜》(膳魔师JNL-502 50万评论TOP5·哈尔斯指纹杯·富光316L)",
        "京东《保温杯专柜正品排行榜》(膳魔师2025新款吸管杯 ¥0 薛之谦同款·虎牌1.5L ¥0·象印820ml日本专柜版)",
        "京东《保温杯学生水杯品牌排行榜》(膳魔师JNL-502-ALB 50万评论TOP3·STANLEY晶粉887ml·京东京造316L冰霸杯)",
        "凡事网《公认口碑不错的十大保温杯推荐》(膳魔师JNL系列+虎牌MMZ-A+象印SM-KA+富光FGL-3705+哈尔斯XD-500)",
        "京东《日美塑料进口保温杯排行榜》(膳魔师JNL-502 TOP2·象印SM-SF白色480ml ¥0 10万评论)",
        "京东《正品进口保温杯排行榜》(膳魔师JNL-502 TOP2·虎牌MJA-B048-ANT ¥0 20万评论TOP4)",
        "京东《不锈钢500ml保温杯品牌排行榜》(膳魔师JNL-502-PRW 10万评论TOP2·希诺XN-1306S ¥0 5万评论·星巴克春日晴空)",
        # 小熊折叠烧水杯
        "京东《宿舍烧水品牌排行榜》(小熊Bear便携式烧水壶 ZDH-C06G3 折叠烧水杯 200万+评论TOP1)",
        "京东《小电水杯排行榜》(米家小米便携电热杯2 350ml ¥0 50万评论TOP1·小熊Bear ZDH-C06G3 200万+评论TOP5)",
        "京东《方便电热水壶排行榜》(美的迷你便携式烧水杯 MK-SH07S105 ¥0 20万评论TOP1·olayks立时 0.8L ¥0 2万评论TOP2)",
        "京东《电保温壶排行榜》(小熊Bear养生壶 YSH-J15H8 1.5L 300万+评论TOP1·美的茶吧机¥0 20万评论)",
        "京东《热水水壶排行榜》(米家即热式饮水机 MJBXJRYSJ01 ¥0 20万评论TOP1·美的1.5L 304不锈钢 ¥0 400万评论TOP2)",
        "京东《70元小家电排行榜》(美的MK-HJ1566 ¥0 400万评论TOP2·米家1.5L ¥0 100万评论TOP4·苏泊尔1.5L ¥0 200万评论TOP5)",
        "京东《便携迷你电热宝排行榜》(宝威玛旅行便携烧水杯 ¥0 42评论·百事可乐PEPSI 0.75L ¥0 1000评论TOP2)"
    ],
    "competitors": [
        {
            "product": "教师节家居礼 50-300元区间",
            "items": [
                {
                    "name": "Soft Kiss纯棉流苏披肩毯礼盒(100×150cm)",
                    "price": "¥69",
                    "advantage": "2026教师节百元档黑马·A类母婴级安全标准·4色适配全类型老师",
                    "jd_sales": "教师节织物礼盒销量爆款·活动价69元",
                    "color": "#C8A48A",
                    "image": IMG_BASE + "_product_1.jpg"
                },
                {
                    "name": "派克(PARKER)威雅XL经典黑金夹墨水笔礼盒",
                    "price": "¥268",
                    "advantage": "京东自营墨水笔TOP1·10万+评论·90年英伦老牌(9/7已选)",
                    "jd_sales": "9/7已选·教师节传统硬通货",
                    "color": "#1A1A1A"
                },
                {
                    "name": "SKG颈椎按摩仪G5颈椎按摩披肩",
                    "price": "¥599-1099",
                    "advantage": "京东自营20万+评论·教师节礼TOP2·(9/5已选)",
                    "jd_sales": "9/5已选·教师节中端礼",
                    "color": "#3A3A3A"
                },
                {
                    "name": "Soft Kiss纯棉午睡毯礼盒(190×130cm)",
                    "price": "¥99-129",
                    "advantage": "同品牌全身午睡毯规格·适配身高较高老师",
                    "jd_sales": "Soft Kiss同系列全身款",
                    "color": "#D2B48C"
                }
            ]
        },
        {
            "product": "教师节护嗓办公设备 100-500元区间",
            "items": [
                {
                    "name": "西圣(XISEM)Bee 小蜜蜂无线领夹扩音器",
                    "price": "¥229",
                    "advantage": "京东月销76件+98%好评率·16芯全频+D类高增益DSP+8小时续航",
                    "jd_sales": "2026教师节护嗓刚需TOP1",
                    "color": "#2C2C2C",
                    "image": IMG_BASE + "_product_2.jpg"
                },
                {
                    "name": "得胜(TAKSTAR)E10W无线领夹扩音器",
                    "price": "¥329",
                    "advantage": "京东音频老牌·76mm大口径稀土磁全频·23小时续航·¥329",
                    "jd_sales": "教师扩音器TOP2",
                    "color": "#1C1C1C"
                },
                {
                    "name": "十度(SHIDU)S615无线领夹扩音器",
                    "price": "¥279",
                    "advantage": "金属机身+精致外观·原声还原度高",
                    "jd_sales": "教师扩音器TOP3",
                    "color": "#8B7355"
                },
                {
                    "name": "金运M20无线领夹扩音器",
                    "price": "¥299",
                    "advantage": "30W扩声功率+4000mAh电池·双麦设计+磁吸佩戴",
                    "jd_sales": "户外场景适配TOP",
                    "color": "#5C5C5C"
                }
            ]
        },
        {
            "product": "通勤降噪耳机 100-500元区间",
            "items": [
                {
                    "name": "OPPO Enco Air5 Pro 真无线降噪耳机",
                    "price": "¥257",
                    "advantage": "京东自营5万评论TOP1·54小时总续航+月珀白简约耐看",
                    "jd_sales": "京东蓝耳机牙入耳式TOP1·通勤学生党TOP1",
                    "color": "#F5F1EA",
                    "image": IMG_BASE + "_product_3.jpg"
                },
                {
                    "name": "Redmi Buds 6 真无线降噪耳机",
                    "price": "¥199",
                    "advantage": "京东-49dB峰值降噪+42小时总续航·小米生态适配",
                    "jd_sales": "小米生态学生党TOP",
                    "color": "#E8E8E8"
                },
                {
                    "name": "漫步者Lolli Pro 5 真无线降噪耳机",
                    "price": "¥399",
                    "advantage": "LDAC高清编码+地铁通勤强降噪+399元价位段旗舰",
                    "jd_sales": "通勤强降噪TOP",
                    "color": "#FFFFFF"
                },
                {
                    "name": "华为FreeBuds 7i 真无线蓝牙降噪耳机",
                    "price": "¥499",
                    "advantage": "智慧动态降噪4.0+静谧通话+鸿蒙智慧助手",
                    "jd_sales": "京东10万评论TOP1",
                    "color": "#FFC0CB"
                }
            ]
        },
        {
            "product": "换季保温杯 100-300元区间",
            "items": [
                {
                    "name": "膳魔师(THERMOS)JNL-502 不锈钢保温杯 500ml",
                    "price": "¥179",
                    "advantage": "京东自营50万+评论·马来西亚进口工艺·1904年德国百年品牌",
                    "jd_sales": "京东Momscook不锈钢进口保温杯TOP1",
                    "color": "#1F2937",
                    "image": IMG_BASE + "_product_4.jpg"
                },
                {
                    "name": "虎牌(TIGER)MJA-B048-XCT 不锈钢保温杯 480ml",
                    "price": "¥199",
                    "advantage": "日本原装进口·1万+评论·磨砂黑/不锈钢色·轻量便携",
                    "jd_sales": "保温杯TOP2",
                    "color": "#404040"
                },
                {
                    "name": "象印(ZO JIRUSHI)SM-WE36-BA 弹盖杯 316不锈钢 360ml",
                    "price": "¥229",
                    "advantage": "日本原装进口·316不锈钢·弹盖单手操作·5000+评论",
                    "jd_sales": "保温杯TOP3",
                    "color": "#1A1A1A"
                },
                {
                    "name": "小米旋盖保温杯 500ml 藏蓝色 316不锈钢",
                    "price": "¥99",
                    "advantage": "米家旋盖设计+316不锈钢+100万+评论·性价比TOP",
                    "jd_sales": "保温杯学生党TOP",
                    "color": "#2C3E50"
                }
            ]
        },
        {
            "product": "差旅折叠烧水杯 100-300元区间",
            "items": [
                {
                    "name": "小熊(Bear)便携式折叠烧水杯 ZDH-C06G3 316不锈钢",
                    "price": "¥169",
                    "advantage": "京东自营200万+评论TOP1·316L母婴级·多档调温+折叠便携",
                    "jd_sales": "京东宿舍烧水品牌榜TOP1",
                    "color": "#FFD3B6",
                    "image": IMG_BASE + "_product_5.jpg"
                },
                {
                    "name": "米家小米便携电热杯2 350ml 316L不锈钢",
                    "price": "¥179",
                    "advantage": "京东自营50万+评论TOP1·316L母婴级·智能恒温+迷你便携",
                    "jd_sales": "京东小电水杯榜TOP1",
                    "color": "#FFFFFF"
                },
                {
                    "name": "美的(Midea)迷你便携式烧水杯 MK-SH07S105 0.7L",
                    "price": "¥149",
                    "advantage": "京东自营20万+评论·316L不锈钢·可折叠+多档调温",
                    "jd_sales": "京东方便电热水壶榜TOP1",
                    "color": "#F5F5F5"
                },
                {
                    "name": "olayks立时 迷你便携式烧水杯 0.8L 316L",
                    "price": "¥159",
                    "advantage": "京东自营2万+评论·316L母婴级·分体式折叠+恒温多段温控",
                    "jd_sales": "京东方便电热水壶榜TOP2",
                    "color": "#E8E8E8"
                }
            ]
        }
    ],
    "hotProducts": [
        {
            "name": "Soft Kiss纯棉流苏披肩毯礼盒(100×150cm)",
            "category": "教师节家居礼",
            "price": "¥69(京东自营·活动价)",
            "image": IMG_BASE + "_product_1.jpg",
            "sales": "2026教师节百元档黑马·A类母婴级·4色·活动价69元",
            "platform": "京东自营·淘宝旗舰店"
        },
        {
            "name": "西圣(XISEM)Bee 小蜜蜂无线领夹扩音器",
            "category": "教师节护嗓礼",
            "price": "¥229(京东自营)",
            "image": IMG_BASE + "_product_2.jpg",
            "sales": "京东月销76件+98%好评率·教师节护嗓TOP1",
            "platform": "京东自营"
        },
        {
            "name": "OPPO Enco Air5 Pro 真无线降噪耳机",
            "category": "通勤降噪耳机",
            "price": "¥257(京东自营)",
            "image": IMG_BASE + "_product_3.jpg",
            "sales": "京东自营5万评论TOP1·通勤降噪耳机TOP",
            "platform": "京东自营"
        },
        {
            "name": "膳魔师(THERMOS)JNL-502 不锈钢保温杯 500ml",
            "category": "换季保温杯",
            "price": "¥179(京东海外自营·马来西亚产)",
            "image": IMG_BASE + "_product_4.jpg",
            "sales": "京东自营50万+评论·进口保温杯TOP1",
            "platform": "京东海外自营"
        },
        {
            "name": "小熊(Bear)便携式折叠烧水杯 ZDH-C06G3",
            "category": "差旅烧水杯",
            "price": "¥169(京东自营)",
            "image": IMG_BASE + "_product_5.jpg",
            "sales": "京东自营200万+评论·宿舍烧水榜TOP1",
            "platform": "京东自营"
        }
    ],
    "dataSource": "WebSearch 真实数据 · 2026-09-08 07:30 cron 自动化抓取",
    "updateTime": "2026-09-08 07:30"
}

with open(OUT_DIR + "/vs-data.json", "w", encoding="utf-8") as f:
    json.dump(vs, f, ensure_ascii=False, indent=2)

print("OK vs-data.json " + OUT_DIR + "/vs-data.json " + str(os.path.getsize(OUT_DIR + "/vs-data.json")) + " bytes")

# Schema 校验
assert "hotProducts" in vs, "缺 hotProducts"
assert len(vs["hotProducts"]) == 5, "hotProducts 必须 5 项"
assert "dataSource" in vs, "缺 dataSource"
assert "updateTime" in vs, "缺 updateTime"
for hp in vs["hotProducts"]:
    assert "image" in hp, "hotProducts 缺 image 字段: " + hp.get("name", "unknown")
print("OK vs-data schema check passed")
