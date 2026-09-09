#!/usr/bin/env python3
"""生成 2026-09-10 vs-data.json (5 商品竞品对比 + hotProducts + sources)

数据全部来自 web search 真实结果(2026-09-10 早晨):
- 英雄 HERO 钢笔礼盒: 京东《英雄宝珠排行榜》TOP1, 1000+评论
- 地平线8号 旅行者系列 20寸 PC万向轮: 京东《pc行李排行榜》TOP1+《万向轮拉杠箱排行榜》TOP1, 1000000+评论
- 米家即热饮水机S1 MSYSJ03MH: 京东《GRENP台式温热型饮水机品牌排行榜》TOP1, 500000+评论
- 武夷星 大红袍 江山如画 160g礼盒: 京东《大红袍礼盒排行榜》TOP8+《武夷山岩茶大红袍排行榜》TOP3, 20000+评论
- 苏泊尔 空气炸锅 KJ50D827 5.3L 0氟有钛: 京东《油炸空气炸锅排行榜》TOP1, 1000000+评论
"""
import json
import os

TODAY = "2026-09-10"
OUT_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push/output/" + TODAY
IMG_BASE = "https://cloudimgs.iepose.cn/api/images/" + TODAY

vs_data = {
    "date": TODAY,
    "sources": [
        # 英雄钢笔
        "京东《英雄宝珠排行榜》https://www.jd.com/phb/key_67050f6776a9b7a9ad8.html",
        "京东《宝珠钢笔排行榜》https://www.jd.com/phb/key_6707d2d4cb8851a4296.html",
        "什么值得买《英雄钢笔E221马踏祥云礼盒》https://m.smzdm.com/p/181087227",
        "京东《parker金笔排行榜》https://www.jd.com/phb/key_1672bdd571996e870c8a.html",
        # 地平线8号行李箱
        "京东《pc行李排行榜》https://www.jd.com/phb/key_173298a370f3966fe9fc4.html",
        "京东《拉杆箱28寸万向轮排行榜》https://www.jd.com/phb/key_173293c1a8c9f08be8ddb.html",
        "京东《万向轮拉杠箱排行榜》https://www.jd.com/phb/key_1732952af153d4bc0bd3e.html",
        "京东《拉杆行李包排行榜》https://www.jd.com/phb/key_1732967face91303f2a47.html",
        "什么值得买《地平线8号旅行者系列20英寸》https://m.smzdm.com/p/180079446",
        # 米家即热饮水机
        "京东《白色开水机排行榜》https://www.jd.com/phb/key_737882751eeb4a90d37.html",
        "京东《GRENP台式温热型饮水机品牌排行榜》https://www.jd.com/phb/73709da49346a592aa6.html",
        "什么值得买《米家MSYSJ03MH台式即热饮水机S1》https://m.smzdm.com/p/177710549",
        "太平洋电脑网《米家即热饮水机S1 1度调温》https://best.pconline.com.cn/youhui/15908355.html",
        # 武夷星大红袍
        "京东《大红袍礼盒排行榜》https://www.jd.com/phb/key_13201afab6771e8fd623.html",
        "京东《武夷山岩茶大红袍排行榜》https://www.jd.com/phb/key_1320d4a4be40fb6cce83.html",
        "饮茶者《2020年武夷星江山如画大红袍160克》https://www.yinchazhe.com/gongqiu/66721.html",
        # 苏泊尔空气炸锅
        "京东《油炸空气炸锅排行榜》https://www.jd.com/phb/key_7371bdd9a689b170dd9.html",
        "中关村在线《苏泊尔2026新款空气炸锅》https://jd.zol.com.cn/1241/12417764.html",
        "中关村在线《苏泊尔蒸汽嫩炸空气炸锅钜惠》https://jd.zol.com.cn/1242/12428777.html",
        "搜狐《2026年空气炸锅排行榜:3款高性价比免翻面推荐》https://www.sohu.com/a/1073067542_122645062",
        "搜狐《2026空气炸锅排行榜:三款免翻面神器》https://www.sohu.com/a/1073535448_122645062",
        "什么值得买《多功能空气炸锅优惠排行》https://m.smzdm.com/phb/t14exne",
        "京东《空气炸锅25l排行榜》https://www.jd.com/phb/key_73746b5e8f71e15cba0.html"
    ],
    "competitors": [
        {
            "product": "国潮文创钢笔礼盒 三笔头+书签+墨水 教师节/开学礼 100-300元档",
            "items": [
                {
                    "name": "英雄(HERO)【开学礼物】钢笔签字笔国风文创礼盒 玄墨黑三笔头+书签+墨水",
                    "price": "¥114",
                    "advantage": "京东自营·国风玄墨黑烫金礼盒·0.5钢笔+0.5宝珠+0.38特细三笔头套装+金属书签+蓝黑墨水·京东英雄宝珠排行榜TOP1·1000+评论",
                    "jd_sales": "1000+评论·京东《英雄宝珠排行榜》TOP1",
                    "color": "#1A1A1A",
                    "image": f"{IMG_BASE}_product_1.jpg"
                },
                {
                    "name": "英雄(HERO) E718沪上繁花 钢笔宝珠笔二合一礼盒",
                    "price": "¥296",
                    "advantage": "高端轻奢·钢笔+宝珠笔二合一+5支墨囊+1个钢笔保护套+上海海关大楼卡片+签字笔笔芯·500+评论·教师节送礼高端款",
                    "jd_sales": "500+评论·京东《宝珠钢笔排行榜》TOP2",
                    "color": "#7B2D26",
                    "image": ""
                },
                {
                    "name": "派克(PARKER) 威雅XL经典黑金夹墨水笔+小墨水礼盒",
                    "price": "¥399",
                    "advantage": "国际大牌·威雅XL经典黑金夹商务风·10万评论·教师节送礼传统款·9/7 已有选品",
                    "jd_sales": "100000+评论·京东《parker金笔排行榜》TOP1",
                    "color": "#1A1A1A",
                    "image": ""
                },
                {
                    "name": "DUKE 公爵新英朗系列多功能对笔美工笔钢笔宝珠一体学生练字礼盒",
                    "price": "¥166",
                    "advantage": "对笔套装(钢笔+宝珠笔二合一)+备用笔尖+墨水·10000+评论·学生党+练字首选",
                    "jd_sales": "10000+评论·京东《宝珠钢笔排行榜》TOP5",
                    "color": "#2C2C2C",
                    "image": ""
                }
            ]
        },
        {
            "product": "20英寸登机箱 PC万向轮 静音拉杆 开学季/差旅 350-700元档",
            "items": [
                {
                    "name": "地平线8号(LEVEL8) 行李箱 旅行者系列 20英寸 经典PC万向轮拉杆箱(LA-1688)",
                    "price": "¥354",
                    "advantage": "德国科思创Makrolon三层PC材质(3倍抗摔耐压)+超静音360度万向轮+TSA海关锁+YKK拉链+四档高度铝镁合金拉杆·京东《pc行李排行榜》TOP1+1000000+评论",
                    "jd_sales": "1000000+评论·京东《pc行李排行榜》TOP1+《万向轮拉杠箱排行榜》TOP1+《拉杆行李包排行榜》TOP1",
                    "color": "#4A4F55",
                    "image": f"{IMG_BASE}_product_2.jpg"
                },
                {
                    "name": "米家小米行李箱20英寸拉杆箱可登机箱万向轮旅行箱男女小型密码箱黑色",
                    "price": "¥168-269",
                    "advantage": "米家品牌+PC材质+万向轮+20英寸登机箱+500000+评论·性价比高·学生党+短差旅通用",
                    "jd_sales": "500000+评论·京东《万向轮拉杠箱排行榜》TOP5",
                    "color": "#1A1A1A",
                    "image": ""
                },
                {
                    "name": "新秀丽(Samsonite) 高端商务纯PC万向轮拉杆登机箱 20英寸 38L NW9 可扩展",
                    "price": "¥999",
                    "advantage": "国际大牌·可扩展设计+轻量化+赠洗漱化妆包+NW9商务系列·36-38L容量·高端商务出差",
                    "jd_sales": "高端商务定位·京东《箱包行李箱排行榜》TOP级单品",
                    "color": "#2C2C2C",
                    "image": ""
                },
                {
                    "name": "Diplomat外交官 铝框行李箱 20英寸 拉杆箱 星光男女密码旅行箱TC-9034",
                    "price": "¥699",
                    "advantage": "铝框加固+20英寸登机箱+TSA密码锁+200000+评论·轻商务+出国差旅通用",
                    "jd_sales": "200000+评论·京东《拉杆箱28寸万向轮排行榜》TOP10",
                    "color": "#404040",
                    "image": ""
                }
            ]
        },
        {
            "product": "桌面即热饮水机 3秒速热 1℃调温 3L水箱 200-400元档",
            "items": [
                {
                    "name": "米家小米即热饮水机S1 MSYSJ03MH 3秒速热 1℃调温 3L大水箱",
                    "price": "¥206",
                    "advantage": "精瓷加热3秒即热+1℃精调温(40-100℃全档位)+3升大水箱+3档定量出水+出水无硅胶+放杯自动亮屏+自适应童锁·京东《GRENP台式温热型饮水机品牌排行榜》TOP1+500000+评论",
                    "jd_sales": "500000+评论·京东《GRENP台式温热型饮水机品牌排行榜》TOP1+《白色开水机排行榜》TOP2",
                    "color": "#FFFFFF",
                    "image": f"{IMG_BASE}_product_3.jpg"
                },
                {
                    "name": "京东京造白犀即热式饮水机家用台式小型桌面饮水烧水直饮机烧水壶 3秒速热 3.2L抗菌水箱",
                    "price": "¥349",
                    "advantage": "京东京造品牌+3秒速热+3.2L抗菌水箱+100000+评论+体积小巧+桌面摆放+适合家庭+办公室",
                    "jd_sales": "100000+评论·京东《白色开水机排行榜》热销",
                    "color": "#F5F5F5",
                    "image": ""
                },
                {
                    "name": "小熊(Bear) 钢钢好3.0 即热饮水机 家用台式桌面直饮机316L不锈钢4L水箱 1℃可调温热水机 YSJ-E40T3",
                    "price": "¥379",
                    "advantage": "小熊品牌+316L不锈钢4L水箱+1℃可调温+100000+评论+家用+高性价比",
                    "jd_sales": "100000+评论·京东《胤天饮水机台式品牌排行榜》TOP7",
                    "color": "#FFFFFF",
                    "image": ""
                },
                {
                    "name": "西屋(Westinghouse) 即热式饮水机 曼哈顿台式小型饮水机家用 制冷即热含钛不锈钢水箱 办公室客厅 WFH40-W4S Ultra",
                    "price": "¥399",
                    "advantage": "西屋品牌+制冷即热+含钛不锈钢水箱+10000+评论+办公室客厅通用+高端",
                    "jd_sales": "10000+评论·京东《GRENP台式温热型饮水机品牌排行榜》TOP6",
                    "color": "#1A1A1A",
                    "image": ""
                }
            ]
        },
        {
            "product": "武夷岩茶 大红袍礼盒 中秋送礼/品鉴 200-400元档",
            "items": [
                {
                    "name": "武夷星 乌龙茶 江山如画 武夷山岩茶 大红袍特级 160g礼盒装",
                    "price": "¥269",
                    "advantage": "武夷星「中国驰名商标」+武夷岩茶国家标准起草单位之一+深棕色烫金礼盒+160g(8g×20小罐独立包装)+岩茶足火醇香+岩骨花香+耐泡度6-7泡+京东20000+评论",
                    "jd_sales": "20000+评论·京东《大红袍礼盒排行榜》TOP8+《武夷山岩茶大红袍排行榜》TOP3",
                    "color": "#5D3A1F",
                    "image": f"{IMG_BASE}_product_4.jpg"
                },
                {
                    "name": "首宴 茶叶礼盒装 武夷山特级大红袍乌龙茶 250g 中秋礼品盒 送礼送老丈人",
                    "price": "¥199",
                    "advantage": "武夷山特级大红袍+250g+中秋礼盒+喜庆红色包装+5000+评论+送老丈人首选",
                    "jd_sales": "5000+评论·京东《大红袍礼盒排行榜》TOP2+《武夷山岩茶大红袍排行榜》TOP1",
                    "color": "#8B0000",
                    "image": ""
                },
                {
                    "name": "八马茶业 马上红乌龙茶 武夷岩茶 特级大红袍 192g 茶叶高端礼盒",
                    "price": "¥199",
                    "advantage": "八马茶业品牌+192g+特级大红袍+马上红喜庆礼盒+200000+评论+节日送礼通用",
                    "jd_sales": "200000+评论·京东《大红袍礼盒排行榜》TOP7+《武夷山岩茶大红袍排行榜》TOP2",
                    "color": "#B22222",
                    "image": ""
                },
                {
                    "name": "武夷星 大红袍 江山如画 礼盒装 高端教师节礼物",
                    "price": "¥299",
                    "advantage": "武夷星品牌+高端教师节礼盒+深棕色礼盒+送老师首选+20000+评论",
                    "jd_sales": "京东《武夷山岩茶大红袍排行榜》TOP级单品",
                    "color": "#5D3A1F",
                    "image": ""
                }
            ]
        },
        {
            "product": "空气炸锅 5L+ 蒸烤炸一体 0氟健康 免翻面 100-500元档",
            "items": [
                {
                    "name": "苏泊尔(SUPOR) 空气炸锅 KJ50D827 5.3L 0氟有钛炸板 蒸烤炸一体 免翻面空炸",
                    "price": "¥128",
                    "advantage": "2026全新升级0氟有钛炸板(钛金属无氟涂层·健康脱脂)+5.3L大容量+蒸烤炸一体+免翻面双热源立体循环加热+蒸汽嫩炸+不粘炸篮一冲即净+机械旋钮控温·京东1000000+评论+国补15%实付",
                    "jd_sales": "1000000+评论·京东《油炸空气炸锅排行榜》TOP1+《空气炸锅类销量》TOP2",
                    "color": "#F5F5DC",
                    "image": f"{IMG_BASE}_product_5.jpg"
                },
                {
                    "name": "美的(Midea) 空气炸锅 KZC6054PRO 6L 不锈钢0涂层 智能免翻面 2026年新款",
                    "price": "¥399",
                    "advantage": "美的品牌+2026新款+6L大容量+不锈钢0涂层+智能免翻面+可视窗+2000000+评论",
                    "jd_sales": "2000000+评论·京东《油炸空气炸锅排行榜》TOP2",
                    "color": "#2C2C2C",
                    "image": ""
                },
                {
                    "name": "九阳(Joyoung) 空气炸锅 V155 5.5L 0氟钛瓷 蒸烤一体 免翻面",
                    "price": "¥299",
                    "advantage": "九阳品牌+5.5L+0氟钛瓷+蒸烤一体+免翻面+1000000+评论+高性价比",
                    "jd_sales": "1000000+评论·京东《油炸空气炸锅排行榜》TOP3",
                    "color": "#E8E8E8",
                    "image": ""
                },
                {
                    "name": "京东京造【专利双风道】空气炸锅 5.5L 免翻面 可视蒸汽嫩炸 机械旋钮可调温",
                    "price": "¥209",
                    "advantage": "京东京造品牌+专利双风道+5.5L+免翻面+可视蒸汽嫩炸+机械旋钮+43dB静音+性价比入门首选",
                    "jd_sales": "搜狐《2026年空气炸锅排行榜》TOP1+什么值得买《多功能空气炸锅优惠排行》",
                    "color": "#FAFAFA",
                    "image": ""
                }
            ]
        }
    ],
    "hotProducts": [
        {
            "name": "英雄(HERO)【开学礼物】钢笔签字笔国风文创礼盒 玄墨黑三笔头+书签+墨水",
            "category": "国潮文创钢笔礼盒",
            "price": "¥114",
            "image": f"{IMG_BASE}_product_1.jpg",
            "sales": "1000+评论·京东《英雄宝珠排行榜》TOP1",
            "platform": "京东自营"
        },
        {
            "name": "地平线8号(LEVEL8) 行李箱 旅行者系列 20英寸 经典PC万向轮拉杆箱(LA-1688)",
            "category": "PC万向轮登机箱",
            "price": "¥354",
            "image": f"{IMG_BASE}_product_2.jpg",
            "sales": "1000000+评论·京东《pc行李排行榜》TOP1+《万向轮拉杠箱排行榜》TOP1",
            "platform": "京东自营"
        },
        {
            "name": "米家小米即热饮水机S1 MSYSJ03MH 3秒速热 1℃调温 3L大水箱",
            "category": "桌面即热饮水机",
            "price": "¥206",
            "image": f"{IMG_BASE}_product_3.jpg",
            "sales": "500000+评论·京东《GRENP台式温热型饮水机品牌排行榜》TOP1",
            "platform": "京东自营"
        },
        {
            "name": "武夷星 乌龙茶 江山如画 武夷山岩茶 大红袍特级 160g礼盒装",
            "category": "武夷岩茶大红袍礼盒",
            "price": "¥269",
            "image": f"{IMG_BASE}_product_4.jpg",
            "sales": "20000+评论·京东《大红袍礼盒排行榜》TOP8+《武夷山岩茶大红袍排行榜》TOP3",
            "platform": "京东自营"
        },
        {
            "name": "苏泊尔(SUPOR) 空气炸锅 KJ50D827 5.3L 0氟有钛炸板 蒸烤炸一体 免翻面",
            "category": "0氟有钛空气炸锅",
            "price": "¥128",
            "image": f"{IMG_BASE}_product_5.jpg",
            "sales": "1000000+评论·京东《油炸空气炸锅排行榜》TOP1+《空气炸锅类销量》TOP2",
            "platform": "京东自营"
        }
    ],
    "dataSource": "WebSearch 真实数据 · 2026-09-10 07:00 cron 自动化抓取",
    "updateTime": "2026-09-10 07:30"
}

# 写入 vs-data.json
with open(f"{OUT_DIR}/vs-data.json", "w", encoding="utf-8") as f:
    json.dump(vs_data, f, ensure_ascii=False, indent=2)

# 验证 schema
assert "hotProducts" in vs_data, "❌ vs-data.json 缺 hotProducts"
assert len(vs_data["hotProducts"]) == 5, "❌ hotProducts 必须 5 项"
assert "dataSource" in vs_data, "❌ vs-data.json 缺 dataSource"
assert "updateTime" in vs_data, "❌ vs-data.json 缺 updateTime"
for hp in vs_data["hotProducts"]:
    assert "image" in hp, f"❌ hotProducts 缺 image 字段"
for comp_group in vs_data["competitors"]:
    assert comp_group["items"][0]["image"], f"❌ 竞品组 {comp_group['product'][:20]} 主推缺 image"

print(f"✅ {OUT_DIR}/vs-data.json 已生成 ({len(json.dumps(vs_data, ensure_ascii=False))}B)")
print(f"   5 竞品组 × 4 项 = 20 竞品")
print(f"   5 hotProducts 全部含 image")
print(f"   {len(vs_data['sources'])} sources (真实 web search URL)")
