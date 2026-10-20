#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_data_20261013.py — 生成 output/2026-10-13/data.json

选品主题: 国庆消费数据验证 + 深秋换季刚需 (双11 长尾期)
5 大场景 (与近 10 天选品完全不重复):
  1. 户外徒步    — 迪卡侬 MH500 三合一冲锋衣
  2. 智能穿戴    — Amazfit 跃我 GTR 3 Pro 智能手表
  3. 厨房小电    — 九阳 小旋风 B70 变频轻音破壁机
  4. 家居环境    — 格力 DH40EF 40L 家用除湿机
  5. 美妆护肤    — 欧莱雅 小蜜罐 4.0 胶原面霜

选品依据: 商务部国庆黄金周消费数据 — 户外运动装备销售额同比 +10.4%,
智能穿戴 +1.2 倍, 智能眼镜 +1 倍; 美团"妆造旅拍"搜索量环比 +200%。

数据来源: WebSearch 真实搜索结果
  - https://www.smzdm.com/p/183344576 (京东京造冲锋衣对比)
  - https://post.smzdm.com/talk/p/a70p2k85 (伯希和冲锋衣实测)
  - https://www.dh3g.com/youxi-99572 (Amazfit GTR 3 Pro)
  - https://mobile.zol.com.cn/1255/12554332.html (ZOL 智能手表榜)
  - https://www.smzdm.com/p/183685138 (九阳 B70 实锤价)
  - https://finance.sina.com.cn/roll/2026-10-05/doc-iniuciqr4800196.shtml (格力 DH40EH)
  - https://www.smzdm.com/p/183670073 (欧莱雅小蜜罐实锤价)
"""
import json
import os

DATE = "2026-10-13"
OUT_DIR = f"/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/{DATE}"
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{DATE}"
os.makedirs(OUT_DIR, exist_ok=True)

products = [
    {
        "id": 1,
        "name": "迪卡侬 DECATHLON MH500 三合一冲锋衣 男户外防风防水硬壳",
        "category": "户外服饰",
        "price": "¥330-375(大促档·京东/线下门店)",
        "desc": (
            "深秋降温 + 户外风当道，一件能扛住山风的冲锋衣比什么都实在。迪卡侬 MH500 "
            "走的是 3L 三层压胶硬壳路线，接缝全压胶，防水指数约 20000mm 级，"
            "什么值得买实测里被值友称为「这个价位段里难找对手」。上身硬壳挡风、下身软壳裤的"
            "经典搭配，配合抓绒或排骨羽绒内胆，零下几度也扛得住。三个尺码建议线下试，"
            "MH500 版型偏欧码、袖子偏长，抬手和下蹲各来一遍最保险。"
        ),
        "highlights": [
            "3L 三层压胶硬壳，接缝全压胶，防水约 20000mm 级",
            "大促价 330-375 元，硬壳里少见的同价位竞争力",
            "防风优先级高于防水，山脊大风环境更实用",
            "内胆另配，单壳三季可用，通勤徒步都能穿",
            "线下门店可试版型，MH500 偏欧码需现场试穿",
        ],
        "tags": ["冲锋衣", "户外徒步", "硬壳", "防风防水", "三合一"],
        "suitable": "秋季徒步、露营、通勤防风的男性用户",
        "price_note": "大促档 330-375 元；1000 元以上档可选伯希和北极星 eVent 膜、凯乐石 MONT X",
        "color": "#2E5A4E",
    },
    {
        "id": 2,
        "name": "Amazfit 跃我 GTR 3 Pro 智能手表 曜石黑 双频五星定位 21天续航",
        "category": "智能穿戴",
        "price": "¥999(曜石黑·京东自营)",
        "desc": (
            "国庆假期智能穿戴设备销售额同比涨了 1.2 倍，手表这波热度是真的。"
            "跃我 GTR 3 Pro 是京东双十一智能手表畅销榜里的常客，专业级双频五星定位、"
            "150 米防水、21 天典型续航，150+ 运动模式全天候监测心率血氧和睡眠分期。"
            "机身厚 10.7mm、重 32g，比 Apple Watch S7 轻一大截，戴一整天不累。"
            "同价位里少数能把续航和定位同时做扎实的一档，适合刚开始认真跑步的人。"
        ),
        "highlights": [
            "双频五星 GPS 定位，跑步轨迹记录稳定不漂移",
            "21 天典型续航，不用天天摘下来充电",
            "10.7mm 厚度 + 32g 重量，比 Apple Watch S7 轻一半",
            "150 米防水，游泳洗漱都不用摘",
            "150+ 运动模式 + 全天候心率血氧睡眠分期监测",
        ],
        "tags": ["智能手表", "运动健康", "长续航", "GPS定位", "双十一"],
        "suitable": "跑步健身人群、需要长续航健康监测的用户",
        "price_note": "京东自营 999 元；同价位对比荣耀 X5i 209 元（功能少）、Apple Watch SE 2199 元",
        "color": "#1F2937",
    },
    {
        "id": 3,
        "name": "九阳 Joyoung 小旋风 B70(PB-UL5B70) 变频轻音 1.75L 破壁机",
        "category": "厨房小电",
        "price": "¥448.89(多券叠加实付·历史低价480.37)",
        "desc": (
            "早上五点全家还在睡，破壁机能把人吵醒就不是好机器。九阳小旋风 B70 用变频轻音方案，"
            "声音低至 35 分贝，平均制浆 47.6 分贝，45000 转/分三层 10 叶立体刀把豆浆粒径打到 90 微米，"
            "喝不出渣。1.75L 大容量适配 3-5 口人，双重自清洁 + 有钛 0 涂层发热盘，除菌率 99.9999%。"
            "什么值得买 10 月 7 日刚创下 480.37 元历史低价，当前 448.89 元是可核对的实付价。"
        ),
        "highlights": [
            "变频轻音低至 35 分贝，清晨打浆不吵醒家人",
            "45000 转/分三层 10 叶立体刀，豆浆粒径 90 微米",
            "1.75L 大容量，3-5 口之家一次搞定",
            "慧瞳遥感持续沸腾不溢出 + 有钛 0 涂层发热盘",
            "双重自清洁，除菌率 99.9999%，刀盘可拆",
        ],
        "tags": ["破壁机", "厨房小家电", "轻音", "豆浆机", "自清洁"],
        "suitable": "爱喝豆浆米糊、注重噪音和清洗便利的家庭",
        "price_note": "smzdm 实付 448.89 元（10/07 历史低价 480.37）；官方参考价 399-499 元",
        "color": "#8B5CF6",
    },
    {
        "id": 4,
        "name": "格力 GREE DH40EF 家用除湿机 40L/天 大容量 干衣防霉 智能恒湿",
        "category": "家居环境",
        "price": "¥1200-1500(40L旗舰档·可叠加以旧换新)",
        "desc": (
            "南方回南天最难受的不是冷，是墙面出汗、衣柜长霉、被子潮乎乎拧出水来。"
            "格力 DH40EF 日除湿量 40L，适合 70-120㎡ 户型，压缩机除湿可以设定目标湿度，"
            "达标自动停机、高于设定值自动启动。7L 大水箱不用频繁倒水，支持外接排水管持续直排，"
            "内置独立干衣模式，阴雨天关窗在室内晾衣也能烘干。万向轮加低噪运行，卧室开着不吵。"
        ),
        "highlights": [
            "日除湿量 40L，覆盖 70-120㎡ 南方回南天户型",
            "智能恒湿，达标自动停机不反复启停",
            "7L 大水箱 + 支持外接排水管连续直排",
            "独立干衣模式，阴雨天室内晾衣加速烘干",
            "万向轮 + 低噪运行，卧室夜间使用不打扰",
        ],
        "tags": ["除湿机", "回南天", "南方湿冷", "干衣", "家居电器"],
        "suitable": "南方潮湿地区、一楼/顶楼、衣帽间易发霉家庭",
        "price_note": "40L 旗舰档 1200-1500 元（新浪测评）；京东专卖店 DH40EF 2880 元、天猫官旗 2180 元",
        "color": "#0EA5E9",
    },
    {
        "id": 5,
        "name": "巴黎欧莱雅 小蜜罐 4.0 胶原面霜 滋润版 60ml 超分子重组胶原",
        "category": "美妆护肤",
        "price": "¥259.95(60ml 赠 60ml·需用券)",
        "desc": (
            "换季脸干起皮、上妆卡粉、熬夜后面部松垮暗沉，这罐面霜针对的就是这几件事。"
            "第四代小蜜罐用丝缎乳霜质地，上脸化开快，润而不腻不会黏枕头；核心是超分子重组胶原，"
            "搭配玻色因 PRO 和黄金胜肽做深层滋养 + 紧致淡纹。干皮适配度高，"
            "膏体像融化的蜂蜜，推开吸收快，第二天早上摸起来软嫩。什么值得买近期实付 259.95 元、"
            "到手 120ml，单罐折算非常香。"
        ),
        "highlights": [
            "超分子重组胶原 + 玻色因 PRO + 黄金胜肽三重复配",
            "丝缎乳霜质地，润而不腻不沾枕头",
            "第四代升级，主打紧致淡纹与深层滋养",
            "60ml 正装赠 60ml，到手共 120ml",
            "干皮秋冬适配，熬夜后暗沉黄气可改善",
        ],
        "tags": ["面霜", "抗初老", "换季护肤", "小蜜罐", "欧莱雅"],
        "suitable": "25-40 岁干皮/混干皮，有抗初老和换季保湿需求",
        "price_note": "smzdm 实付 259.95 元（京东 339 元，需用券）；官方正装约 300-399 元",
        "color": "#F59E0B",
    },
]

for p in products:
    pid = p["id"]
    p["image"] = f"{IMG_BASE}_product_{pid}.jpg"
    p["images"] = [
        p["image"],
        f"{IMG_BASE}_product_slice_{pid}.jpg",
    ]

data = {
    "date": DATE,
    "totalProducts": len(products),
    "products": products,
}

path = os.path.join(OUT_DIR, "data.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# schema 校验 (失败 raise)
for p in data["products"]:
    assert "image" in p, f"❌ product {p['id']} 缺 image"
    assert p["image"].startswith("https://"), f"❌ product {p['id']} image 必须 CDN URL"
    assert "images" in p and len(p["images"]) >= 1, f"❌ product {p['id']} 缺 images"
    assert len(p["highlights"]) == 5, f"❌ product {p['id']} highlights 必须 5 个"
    assert len(p["tags"]) == 5, f"❌ product {p['id']} tags 必须 5 个"
    assert 120 <= len(p["desc"]) <= 260, f"❌ product {p['id']} desc 长度 {len(p['desc'])} 不在 120-260"

print(f"✅ data.json 写入 {path}")
print(f"   products: {len(products)}")
for p in products:
    print(f"   #{p['id']} {p['name'][:34]} | {p['price'][:28]} | desc {len(p['desc'])}字")
print("✅ data.json schema 校验通过")
