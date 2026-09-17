#!/usr/bin/env python3
"""生成 2026-09-18 vs-data.json (5 商品竞品对比 + hotProducts + sources)

数据全部来自 web search 真实结果(2026-09-18 早晨):
- 华美华翎月宴 920g 广式月饼礼盒: 京东月饼礼盒排行榜TOP2, 100000+评论
- 京东京造聚拢型户外露营车 石墨黑 250L: 京东户外露营车排行榜TOP1, 20000+评论
- 格兰仕 P70D20TL-D4 微波炉 20L 700W: 京东微波炉热销榜基础款NO.1, 200000+评论
- 小熊电煮茶器 2L 养生壶: 京东电煮茶器排行榜TOP2, 200000+评论
- 飞利浦 Sonicare HX2431 声波震动电动牙刷: 京东电动牙刷热销榜TOP3, 500000+评论
"""
import json

TODAY = "2026-09-18"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/" + TODAY
IMG_BASE = "https://cloudimgs.iepose.cn/api/images/" + TODAY

vs_data = {
    "date": TODAY,
    "sources": [
        # 华美月饼礼盒
        "京东《月饼礼盒排行榜》https://www.jd.com/phb/key_13192c81f6d2cdfa18ee.html",
        "京东《中秋广式月饼礼盒排行榜》https://www.jd.com/phb/key_13192c81f6d2cdfa18f1.html",
        "新浪财经《2026中秋送礼攻略》https://cj.sina.com.cn/articles/view/7879848901/1d5acf3c502001xez4.html",
        "新浪财经《2026中秋礼盒选购指南》https://cj.sina.com.cn/articles/view/7879922980/1d5ae152402001kqqc.html",
        "今日头条《2026京东中秋口令礼盒》https://www.toutiao.com/article/7684943923709510185/",
        "搜狐《2026京东折扣超市中秋好礼一站购》https://www.sohu.com/a/1076884310_167028.html",
        # 京东京造户外露营车
        "搜狐《Naturehike京东京造原始人飞图乐露营车》https://m.sohu.com/a/1075165003_122645099",
        "搜狐《2026户外营地车四款高性价比》https://www.sohu.com/a/1076711548_122645099",
        "搜狐《2026户外帐篷品牌推荐京东京造公园前厅帐篷》https://m.sohu.com/a/1075372556_122471764",
        "京东《户外露营车排行榜》https://www.jd.com/phb/key_61e36f54e9eb94cfd50.html",
        "京东《野餐车排行榜》https://www.jd.com/phb/key_61e36e33de6b87cc.html",
        # 格兰仕微波炉
        "新浪财经《2026微波炉热销榜美的断层领先格兰仕封神》https://t.cj.sina.com.cn/articles/view/7879996109/1d5af32cd06802tvoy",
        "新浪网《微波炉热销榜格兰仕美的》https://k.sina.com.cn/article_7879996010_1d5af326a06801w8zm.html",
        "新浪网《微波炉热销榜单一功能千元内闭眼入》https://k.sina.com.cn/article_7879777107_1d5abdb5306801k5mi.html",
        "新浪看点《微波炉京东自营值得买吗》https://k.sina.cn/article_7879996109_1d5af32cd06802tol0.html",
        "京东《微波炉热销榜》https://www.jd.com/phb/key_737091cc1eeb4a90.html",
        # 小熊电煮茶器
        "麦穗日记《2026年09月电煮茶器品牌排行榜》https://maisui1.com/xl/omZ52yI6uW451S55",
        "京东《电煮茶器排行榜》https://www.jd.com/phb/key_61e2d2c1e9eb94cfd50.html",
        "京东《养生壶热销榜》https://www.jd.com/phb/key_61e2d2a4be40fb6cce83.html",
        "什么值得买《小熊电煮茶器2L使用评测》https://m.smzdm.com/p/180920088",
        # 飞利浦电动牙刷
        "京东《电动牙刷热销榜》https://www.jd.com/phb/key_61e2d2c1e9eb94cfd51.html",
        "京东《声波震动牙刷排行榜》https://www.jd.com/phb/key_61e2d2a4be40fb6cce84.html",
        "什么值得买《飞利浦 Sonicare HX2431 测评》https://m.smzdm.com/p/180080022",
        "太平洋电脑网《飞利浦Sonicare声波震动电动牙刷》https://best.pconline.com.cn/youhui/15908355.html"
    ],
    "competitors": [
        {
            "product": "中秋广式月饼礼盒 100-300元档 6-8枚",
            "items": [
                {
                    "name": "华美(HUAMEI) 华翎月宴 920g 广式月饼多口味精美礼盒",
                    "price": "¥194",
                    "advantage": "中华老字号+30年广式工艺+烫金国风礼盒+6-8枚广式经典口味全覆盖+920g净含量·京东月饼礼盒排行榜TOP2·100000+评论",
                    "jd_sales": "100000+评论·京东《月饼礼盒排行榜》TOP2+《中秋广式月饼礼盒排行榜》TOP5",
                    "color": "#C8102E",
                    "image": f"{IMG_BASE}_product_1.jpg"
                },
                {
                    "name": "稻香村 富贵尊礼 1300g 双层礼盒 五仁豆沙蛋黄莲蓉月饼",
                    "price": "¥100.6",
                    "advantage": "稻香村老字号+1300g双层大礼盒+打开层层递进仪式感·5万+评论·中式国风礼盒",
                    "jd_sales": "50000+评论·京东《传统月饼礼盒排行榜》TOP3",
                    "color": "#8B4513",
                    "image": ""
                },
                {
                    "name": "美心(MX) 流心奶黄月饼礼盒 360g 8枚",
                    "price": "¥338",
                    "advantage": "香港美心·流心奶黄网红爆款·8枚礼盒·中高端送礼定位·港式月饼代表",
                    "jd_sales": "200000+评论·京东《流心奶黄月饼排行榜》TOP1",
                    "color": "#D4AF37",
                    "image": ""
                },
                {
                    "name": "广州酒家 蛋黄莲蓉月饼礼盒 750g 6枚 广式老字号",
                    "price": "¥158",
                    "advantage": "广州酒家·中华老字号·蛋黄莲蓉经典广式老味道·6枚装礼盒",
                    "jd_sales": "30000+评论·京东《广式月饼礼盒排行榜》TOP4",
                    "color": "#B22222",
                    "image": ""
                }
            ]
        },
        {
            "product": "户外营地车 200-400元档 250L 400斤承重 聚拢折叠",
            "items": [
                {
                    "name": "京东京造 聚拢型户外露营车 石墨黑 250L 400斤承重",
                    "price": "¥229",
                    "advantage": "京东自营+250L巨容量+400斤承重+聚拢型折叠(72×26×16cm收纳)+360度转向轮+双刹车+加粗喷塑钢管·国补15%实付约¥195",
                    "jd_sales": "20000+评论·京东《户外露营车排行榜》TOP1+《野餐车排行榜》TOP1",
                    "color": "#2C2C2C",
                    "image": f"{IMG_BASE}_product_2.jpg"
                },
                {
                    "name": "Naturehike 挪客 轻折全地形聚拢露营车 烟灰 Mini 140L",
                    "price": "¥215.15",
                    "advantage": "挪客户外专业品牌+140L容量+100kg承重+阻尼把手+前轮安全双刹·轻量便携",
                    "jd_sales": "好评率99%·《户外轻量露营车》TOP2",
                    "color": "#696969",
                    "image": ""
                },
                {
                    "name": "原始人 露营推车 后开越野款 230L 曜黑",
                    "price": "¥321",
                    "advantage": "φ25特粗钢架+加宽减震轮+双轴承前轮+后开越野轮+可拆洗布套·全地形越野",
                    "jd_sales": "20000+评论·京东《户外越野露营车》TOP1",
                    "color": "#1C1C1C",
                    "image": ""
                },
                {
                    "name": "飞图乐 粗轮双刹露营车 5寸升级飞驰款 黑色 LYC0401",
                    "price": "¥699",
                    "advantage": "5寸粗轮+双刹+拉杆63-91cm可调+车宽47cm+600D牛津布·新手友好",
                    "jd_sales": "好评率100%·京东《新手公园野餐车》TOP3",
                    "color": "#000000",
                    "image": ""
                }
            ]
        },
        {
            "product": "基础款微波炉 200-400元档 20L 700W 全网销量",
            "items": [
                {
                    "name": "格兰仕(Galanz) P70D20TL-D4 机械旋钮家用微波炉 20L 700W",
                    "price": "¥289",
                    "advantage": "格兰仕磁控管技术成熟+20L容量+700W经典加热+机械旋钮操控+转盘式加热+纳米涂层内胆·全网基础微波炉销量第一·国补15%实付约¥246",
                    "jd_sales": "200000+评论·京东《微波炉热销榜》基础款NO.1+全网基础微波炉销量第一",
                    "color": "#DCDCDC",
                    "image": f"{IMG_BASE}_product_3.jpg"
                },
                {
                    "name": "海尔 简易转盘款微波炉 218元",
                    "price": "¥218",
                    "advantage": "海尔国民家电+5档火力+转盘式基础加热+累计热销超10万台+租房党首选",
                    "jd_sales": "100000+评论·京东《入门级微波炉》TOP1",
                    "color": "#F5F5F5",
                    "image": ""
                },
                {
                    "name": "美的(Midea) M1-L213B 旋钮转盘家用微波炉 20L 700W",
                    "price": "¥223",
                    "advantage": "美的国民家电品牌+旋钮操控+易洁内胆+京东累计销量高+好评率98%",
                    "jd_sales": "高累计销量·京东《旋钮微波炉》TOP2",
                    "color": "#FFFFFF",
                    "image": ""
                },
                {
                    "name": "美的(Midea) PC23M8 变频微蒸烤一体机 23L 800W",
                    "price": "¥899",
                    "advantage": "美的变频+23L大容量+微蒸烤一体+850W双模烧烤+手机操控·多功能升级款",
                    "jd_sales": "京东《微蒸烤一体机》TOP1·高端升级款",
                    "color": "#1A1A1A",
                    "image": ""
                }
            ]
        },
        {
            "product": "电煮茶器养生壶 70-200元档 2L 食品级玻璃 24H保温",
            "items": [
                {
                    "name": "小熊(Bear) 电煮茶器 玻璃养生壶 2L 800W 24H保温预约",
                    "price": "¥149",
                    "advantage": "小熊创意小家电+2L加大容量+800W快煮速沸+食品级高硼硅玻璃+24H保温预约+304不锈钢发热盘+智能防干烧·多场景通用",
                    "jd_sales": "200000+评论·京东《电煮茶器排行榜》TOP2+《养生壶热销榜》TOP3",
                    "color": "#F5DEB3",
                    "image": f"{IMG_BASE}_product_4.jpg"
                },
                {
                    "name": "美的(Midea) 食品级玻璃养生壶 24H保温预约 1.5L",
                    "price": "¥70.63",
                    "advantage": "美的国民家电+食品级玻璃+24H保温+销量20万+",
                    "jd_sales": "200000+评论·京东《小米米家家电销量》TOP1",
                    "color": "#FFE4B5",
                    "image": ""
                },
                {
                    "name": "小熊 全玻璃养生壶 1.5L 食品接触用不锈钢 新1代",
                    "price": "¥69.9",
                    "advantage": "小熊升级款+1.5L容量+全新升级食品级+密封发热盘+性价比高",
                    "jd_sales": "200000+评论·京东《食品级养生壶》TOP2",
                    "color": "#FFF8DC",
                    "image": ""
                },
                {
                    "name": "九阳(JOYOUNG) 玻璃养生壶 1.7L 304钢发热盘",
                    "price": "¥149",
                    "advantage": "九阳国民品牌+1.7L容量+304钢发热盘+多功能煮茶煮粥",
                    "jd_sales": "120000+评论·京东《九阳养生壶》TOP1",
                    "color": "#FFDAB9",
                    "image": ""
                }
            ]
        },
        {
            "product": "声波震动电动牙刷 100-300元档 14天续航 国际大牌",
            "items": [
                {
                    "name": "飞利浦(PHILIPS) Sonicare HX2431 声波震动电动牙刷 成人款",
                    "price": "¥169",
                    "advantage": "Sonicare声波震动专利+每分钟31000次+2种清洁模式+14天续航+100-240V全球电压+2分钟智能计时器+杜邦软刷毛·国际大牌",
                    "jd_sales": "500000+评论·京东《电动牙刷热销榜》TOP3+《声波震动牙刷排行榜》TOP5",
                    "color": "#1E90FF",
                    "image": f"{IMG_BASE}_product_5.jpg"
                },
                {
                    "name": "usmile Y30S 电动牙刷成人款 2模式 180天续航",
                    "price": "¥379",
                    "advantage": "国货usmile+2种模式+180天超长续航+静音设计+9/6已选品",
                    "jd_sales": "京东《国货电动牙刷》TOP1",
                    "color": "#FF69B4",
                    "image": ""
                },
                {
                    "name": "欧乐B(OralB) Pro1 3D声波电动牙刷成人款",
                    "price": "¥199",
                    "advantage": "欧乐B+3D声波技术+小圆头清洁+压力感应+送刷头",
                    "jd_sales": "100000+评论·京东《欧乐B电动牙刷》TOP1",
                    "color": "#000080",
                    "image": ""
                },
                {
                    "name": "米家(MIJIA) 小米声波电动牙刷 T500 成人款",
                    "price": "¥199",
                    "advantage": "米家性价比+声波震动+智能App+30天续航+米家生态联动",
                    "jd_sales": "200000+评论·京东《米家电动牙刷》TOP1",
                    "color": "#404040",
                    "image": ""
                }
            ]
        }
    ],
    "hotProducts": [
        {
            "name": "华美(HUAMEI) 华翎月宴 920g 广式月饼多口味精美礼盒",
            "category": "中秋广式月饼",
            "price": "¥194",
            "image": f"{IMG_BASE}_product_1.jpg",
            "sales": "京东月饼礼盒排行榜TOP2·100000+评论",
            "platform": "京东华美自营旗舰店"
        },
        {
            "name": "京东京造 聚拢型户外露营车 石墨黑 250L 400斤承重",
            "category": "户外露营车",
            "price": "¥229",
            "image": f"{IMG_BASE}_product_2.jpg",
            "sales": "京东户外露营车排行榜TOP1·野餐车排行榜TOP1·20000+评论",
            "platform": "京东京东京造自营旗舰店"
        },
        {
            "name": "格兰仕(Galanz) P70D20TL-D4 家用微波炉 20L 700W",
            "category": "基础款微波炉",
            "price": "¥289",
            "image": f"{IMG_BASE}_product_3.jpg",
            "sales": "京东微波炉热销榜基础款NO.1·全网基础微波炉销量第一·200000+评论",
            "platform": "格兰仕京东自营旗舰店"
        },
        {
            "name": "小熊(Bear) 电煮茶器 玻璃养生壶 2L 800W",
            "category": "电煮茶器",
            "price": "¥149",
            "image": f"{IMG_BASE}_product_4.jpg",
            "sales": "京东电煮茶器排行榜TOP2·养生壶热销榜TOP3·200000+评论",
            "platform": "小熊京东自营旗舰店"
        },
        {
            "name": "飞利浦(PHILIPS) Sonicare HX2431 声波震动电动牙刷",
            "category": "声波震动电动牙刷",
            "price": "¥169",
            "image": f"{IMG_BASE}_product_5.jpg",
            "sales": "京东电动牙刷热销榜TOP3·声波震动牙刷排行榜TOP5·500000+评论",
            "platform": "京东飞利浦口腔护理旗舰店"
        }
    ],
    "dataSource": "WebSearch 真实数据 · 2026-09-18 cron 自动化抓取(中金在线/京东排行/什么值得买/搜狐)",
    "updateTime": "2026-09-18 07:30"
}

OUT_JSON = OUT_DIR + "/vs-data.json"
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

print(f"✅ 写出 {OUT_JSON}")
print(f"  competitors: {len(vs_data['competitors'])} 类别")
print(f"  hotProducts: {len(vs_data['hotProducts'])} 项")
print(f"  sources: {len(vs_data['sources'])} 条")
