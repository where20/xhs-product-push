#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vs_data_20261011.py — 生成 2026-10-11 的 vs-data.json (竞品对比)

所有竞品价格/销量均来自 2026 年 10 月真实搜索结果:
  - IT之家 ithome.com (2026-10-09: 小米智能门锁5C猫眼版预售 999.6 元国补后)
  - 新浪网 sina.cn / k.sina.com.cn (2026-10: 智能门锁 3 维度横评 + 电动牙刷京东自营横评)
  - 天极网 dh.yesky.com (双11 电动牙刷 200-400 元档 5 款横评)
  - 新浪网 k.sina.com.cn (2026-10-10: 2026双11扫地机器人热销榜)
  - 头条文章 k.sina.cn (2026-10-10: 科沃斯石头追觅三强争霸, 开源证券/IDC/Runto 2026H1 份额)
  - 腾讯搜一搜 (2026-10-07: 双11 十款最推荐日用好物 - 南卡OE GT2 开放式耳机)
  - 凡事网 / 咖啡工房 makecoffee.cn (双11 耳机横评 + 半自动意式咖啡机分档实测)
严禁编造, 所有数字可回溯到上述来源。
"""
import json
import os

TODAY = "2026-10-11"
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{TODAY}"
OUT_DIR = f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{TODAY}"
os.makedirs(OUT_DIR, exist_ok=True)

competitors = [
    {
        "product": "智能门锁 · 千元档 ¥659-1400",
        "items": [
            {
                "name": "小米智能门锁5C猫眼版 自弹锁体 关门自动上锁 11种开锁方式",
                "price": "¥999.6",
                "advantage": "国补后到手价,较京东日常价 1176 元立省 176 元;自弹锁体关门自动上锁,"
                            "门内大屏访客按铃自动亮屏+手机变声可视对讲",
                "jd_sales": "IT之家 2026-10-09 上架预售 · 京东日常售价 1176 元",
                "color": "#2F6B4F",
                "image": f"{IMG_BASE}_product_1.jpg",
            },
            {
                "name": "小米智能门锁 E30",
                "price": "¥499-699(国补低至629)",
                "advantage": "米家生态性价比入口,AI 指纹自学习+双电池续航 12 个月;"
                            "短板是无猫眼门铃、无法可视对讲",
                "jd_sales": "新浪网 2026-10 横评 · 截至 2026 年 10 月综合评估",
                "color": "#C9A227",
            },
            {
                "name": "格行 GX-8 智能门锁 3D双目人脸+内外双摄",
                "price": "¥999",
                "advantage": "千元唯一配齐 3D双目人脸+内外双摄+C级锁芯+5年质保,"
                            "刷新千元级配置天花板,老房换新首选",
                "jd_sales": "新浪网 2026-10 · 千元人脸锁黑马",
                "color": "#E07A5F",
            },
            {
                "name": "凯迪仕 Q20F PRO 智能门锁 上下双摄",
                "price": "¥1200",
                "advantage": "专业品牌中端标杆,上下双摄+红外夜视,门外异常随时监控;"
                            "线下服务网点覆盖全国",
                "jd_sales": "新浪网 2026-10 · 德施曼/凯迪仕合计市占超 30%",
                "color": "#81B29A",
            },
        ],
    },
    {
        "product": "电动牙刷 · 扫振/声波主力档 ¥180-389",
        "items": [
            {
                "name": "徕芬扫振电动牙刷 i2 伺服电机 66000次/分钟 三维十级调节",
                "price": "¥389起",
                "advantage": "自研伺服系统+0-60°大范围扫动,App 三维各 10 档可组合上千种模式;"
                            "毫秒级过压提醒+无线磁吸充电+60天续航+IPX8",
                "jd_sales": "天极网 2026 双11横评 · 五款中价格最高、可调空间最大",
                "color": "#3A6EA5",
                "image": f"{IMG_BASE}_product_2.jpg",
            },
            {
                "name": "扉乐 Major 声波电动牙刷 15档调节",
                "price": "¥369",
                "advantage": "京东自营 20000 条评论 99% 好评率,15档调节适合全家不同牙齿;"
                            "实测约 20 天续航,按键式充电 3 小时",
                "jd_sales": "新浪网 2026 京东自营实测 · 京东自营旗舰店",
                "color": "#3D5A80",
            },
            {
                "name": "飞利浦 HX5181 钻石3系 声波电动牙刷",
                "price": "¥271(京东自营249)",
                "advantage": "五款中唯一国际品牌声波款,31000次/分钟+5种模式+微泡水流科技,"
                            "震动细腻噪音小,从手动换过来更容易接受",
                "jd_sales": "天极网 2026 双11横评 · 参考价 271 元",
                "color": "#6C757D",
            },
            {
                "name": "Usmile P20 PRO 扫振电动牙刷 最大摆幅60°",
                "price": "¥289",
                "advantage": "灯环分区漏刷提示(红灯未刷净/白灯清洁到位),标配缓震刷头,"
                            "IPX8+续航90天+充电4-5小时;usmile 2025 年以 32.3% 份额居中国市场第一",
                "jd_sales": "天极网 2026 双11横评 · 智研咨询市占数据",
                "color": "#B5838D",
            },
        ],
    },
    {
        "product": "扫地机器人 · 2026双11 ¥598-2899",
        "items": [
            {
                "name": "追觅 S60 Pro 33000Pa飓风吸力 4cm越障 100℃基站",
                "price": "¥1560",
                "advantage": "33000Pa+4700Pa 压强+27cm 加长滚筒,全场景 0缠双滚刷+梳齿刮条防缠绕,"
                            "全地形五轮 4cm 越障,双滚刷实测几乎不缠绕;短板是基站体积偏大",
                "jd_sales": "新浪网 2026-10-10 双11榜单 · 实测博主 @阿泰的深夜评测 等",
                "color": "#1F5C8B",
                "image": f"{IMG_BASE}_product_3.jpg",
            },
            {
                "name": "石头 P10 Pro AI结构光避障 全胶刷",
                "price": "¥899-999(清仓/官翻)",
                "advantage": "千元内有娃家庭唯一靠谱选择,识别超300种家庭物体、2cm 以上小物件"
                            "毫米级绕行,5500Pa+全胶刷+银离子抗菌拖布,实测菌落从 1200 降至 50CFU/cm²",
                "jd_sales": "新浪网 2026-10 双11 · 清仓/官翻机口径",
                "color": "#DDA15E",
            },
            {
                "name": "云鲸 S2 Island 90℃熨干除菌 0缠绕",
                "price": "¥598(国补+返E卡后)",
                "advantage": "双11 叠加国补后到手不到 600 元(原价约 1488 元),今年最便宜的扫地机之一;"
                            "短板是需手动倒尘盒、无自清洁基站,适合小户型/出租屋",
                "jd_sales": "新浪网 2026-10-10 榜单 · 2025双11 曾低至 1335 元",
                "color": "#7FB069",
            },
            {
                "name": "科沃斯 T80S 毛发0缠绕 全能基站",
                "price": "约¥2871(优惠后)",
                "advantage": "2026H1 国内销额份额第一约 33%(开源证券/IDC/Runto);"
                            "标配毛发 0 缠绕滚刷,养宠家庭实测有效,但价格中高端",
                "jd_sales": "新浪网 2026-10-10 · 2026H1 线上份额口径",
                "color": "#4A7C59",
            },
        ],
    },
    {
        "product": "开放式蓝牙耳机 · 百元至千元档 ¥149-1000",
        "items": [
            {
                "name": "南卡 OE GT2 开放式耳机 18×11mm巨幕动圈",
                "price": "¥200出头",
                "advantage": "Tri-Boost 三腔体空气增压结构正面解决开放式低频单薄问题,"
                            "官方标称保真度 98.6%;单耳 8g+液态硅胶包裹,万人测试舒适满意度 99%",
                "jd_sales": "腾讯搜一搜 2026-10-07《双11 十款最推荐日用好物》· 百元档代表",
                "color": "#4A4E8C",
                "image": f"{IMG_BASE}_product_4.jpg",
            },
            {
                "name": "华为 FreeClip 耳夹式开放式耳机",
                "price": "中高端档",
                "advantage": "耳夹式设计单耳仅 5.6g,36 小时续航+双设备连接;"
                            "10.8mm 双磁高灵敏度单元配合逆声场声学技术减少漏音",
                "jd_sales": "凡事网 2026 双11 耳机横评 · 旗舰款定位",
                "color": "#C1121F",
            },
            {
                "name": "Redmi Buds 6 真无线蓝牙耳机",
                "price": "约¥200",
                "advantage": "12.4mm 镀钛单元+5.5mm 微压陶瓷单元双单元架构,49 分贝降噪满足日常通勤,"
                            "42 小时续航,支持小米澎湃智联",
                "jd_sales": "凡事网 2026 双11 耳机横评 · 性价比款两百元级",
                "color": "#F77F00",
            },
            {
                "name": "漫步者 ZeroBuds 半入耳蓝牙耳机",
                "price": "一百多元",
                "advantage": "半入耳式佩戴舒适,蓝牙 5.3 连接稳定,26 小时续航满足日常,"
                            "65ms 低延迟适合游戏和视频,学生党基础听音够用",
                "jd_sales": "凡事网 2026 双11 耳机横评 · 百元级入门",
                "color": "#4361EE",
            },
        ],
    },
    {
        "product": "意式半自动咖啡机 · 分档 ¥800-9000",
        "items": [
            {
                "name": "德龙 EC156 半自动意式咖啡机 锅炉式",
                "price": "¥800以内",
                "advantage": "德龙唯一一款锅炉式咖啡机,三位数价格+锅炉相较加热块的水温优势,"
                            "小型水箱保证水质新鲜;短板是自带粉锤喷嘴一般、锅炉小、粉碗非标",
                "jd_sales": "咖啡工房 makecoffee.cn 分档实测 · 入门机不二选择",
                "color": "#7A5230",
                "image": f"{IMG_BASE}_product_5.jpg",
            },
            {
                "name": "迈拓 EM-18 半自动咖啡机 黄铜单锅炉 300ml",
                "price": "约¥1600(另一篇记2000元以内)",
                "advantage": "外形仿兰奇里奥小S 被称「仿S」,性能接近但便宜近 2/3;"
                            "黄铜单锅炉保温性和蒸汽时长优于 EC156,更好拉花",
                "jd_sales": "咖啡工房 makecoffee.cn · 咖啡论坛新手欢迎款",
                "color": "#A68A64",
            },
            {
                "name": "惠家 KD-210S2 双泵双加热块 半自动咖啡机",
                "price": "约¥3500-4000",
                "advantage": "双水泵双加热块可边萃取边打奶泡,功能相当商用机;"
                            "冲煮头带预浸功能+定量出杯+水位预警,但温控稍逊于锅炉式",
                "jd_sales": "咖啡工房 makecoffee.cn · 咖友公认性价比极高",
                "color": "#5F7161",
            },
            {
                "name": "爱宝 E61 双锅炉旋转泵版 半自动咖啡机",
                "price": "京东¥8560(淘宝约9000)",
                "advantage": "万元内家用顶峰,双锅炉各 1.5 升+旋转泵压力比震动泵更稳定、噪音小;"
                            "E61 冲煮头自动预浸,部分小型咖啡馆也在用",
                "jd_sales": "咖啡工房 makecoffee.cn · 京东商城实价 8560 元",
                "color": "#606C38",
            },
        ],
    },
]

# === hotProducts: 5 项, 从 5 个主推商品衍生 ===
hot_products = [
    {
        "name": "小米智能门锁5C猫眼版 国补后999.6元起 关门自动上锁",
        "category": "家居安防·入户门锁",
        "price": "¥999.6",
        "image": f"{IMG_BASE}_product_1.jpg",
        "sales": "IT之家 2026-10-09 上架预售,国补后 999.6 元起(京东日常 1176 元);"
                 "2026 市占:德施曼 20.1% 销额 / 小米 18.1% 销量 / 凯迪仕 10.0%,前三超 55%",
        "platform": "京东自营 / 小米官方",
    },
    {
        "name": "徕芬扫振电动牙刷 i2 66000次/分钟 三维十级调节",
        "category": "口腔个护·扫振牙刷",
        "price": "¥389起",
        "image": f"{IMG_BASE}_product_2.jpg",
        "sales": "天极网 2026 双11 200-400 元档横评五款中价格最高、可调空间最大;"
                 "京东自营第一梯队(usmile/飞利浦/欧乐B/米家/徕芬)市占率合计超 70%",
        "platform": "天猫 / 唯品会自营（京东自营暂未上架 i2）",
    },
    {
        "name": "追觅 S60 Pro 扫地机器人 33000Pa 4cm越障 双11到手1560元",
        "category": "清洁家电·扫地机器人",
        "price": "¥1560",
        "image": f"{IMG_BASE}_product_3.jpg",
        "sales": "新浪网 2026-10-10 双11榜单推荐;2026H1 国内销额份额:科沃斯约33%、石头约25%、"
                 "追觅约17%,前三合计超 75%(开源证券/IDC/Runto)",
        "platform": "京东自营 / 追觅官方旗舰",
    },
    {
        "name": "南卡 OE GT2 开放式蓝牙耳机 18×11mm巨幕动圈 单耳8g",
        "category": "数码音频·开放式耳机",
        "price": "¥200出头",
        "image": f"{IMG_BASE}_product_4.jpg",
        "sales": "腾讯搜一搜 2026-10-07 双11 百元档代表机型,官方标称保真度 98.6%、"
                 "佩戴舒适满意度 99%(官方口径,非平台销量)",
        "platform": "天猫 / 京东自营",
    },
    {
        "name": "德龙 EC156 半自动意式咖啡机 锅炉式 800元内入门",
        "category": "厨房咖啡·意式半自动",
        "price": "¥800以内",
        "image": f"{IMG_BASE}_product_5.jpg",
        "sales": "咖啡工房 makecoffee.cn 分档实测:800 元以内入门机不二选择;"
                 "德龙为唯一一款锅炉式机型,家用电器大厂出品",
        "platform": "天猫 / 京东自营",
    },
]

vs = {
    "date": TODAY,
    "sources": [
        "IT之家 ithome.com（2026-10-09：小米智能门锁5C猫眼版预售，国补后 999.6 元起，京东日常 1176 元）",
        "新浪网 sina.cn / k.sina.com.cn（2026-10：智能门锁 3 维度横评，德施曼20.1%/小米18.1%/凯迪仕10.0% 市占）",
        "天极网 dh.yesky.com（双11 电动牙刷 200-400 元档：舒客G5 Pro+ ¥180、Usmile P20 PRO ¥289、美的YM6Pro ¥249、飞利浦HX5181 ¥271、徕芬i2 ¥376起）",
        "新浪网 k.sina.com.cn（2026 京东自营电动牙刷：usmile P10 ¥149、小米T300 ¥71、徕芬扫振SE ¥214、扉乐Major ¥369 99%好评）",
        "新浪网 k.sina.com.cn（2026-10-10：2026双11扫地机器人热销榜，云鲸S2 Island 国补后 598 元 / 追觅S60 Pro 1560 元）",
        "头条文章 k.sina.cn（2026-10-10：科沃斯/石头/追觅三强争霸，开源证券+IDC+Runto 2026H1 份额 33%/25%/17%）",
        "新浪网（2026-09：扫地机国际标准 11 项测试发布；科沃斯 10/7 京东101HOME 品牌日旗舰 4000-6000 元）",
        "腾讯搜一搜（2026-10-07：双11 十款最推荐日用好物，南卡OE GT2 开放式耳机 200 出头）",
        "凡事网 fan-pin.com（2026 双11 蓝牙耳机横评：华为FreeClip / Redmi Buds 6 ¥200 / 漫步者ZeroBuds 百元级）",
        "咖啡工房 makecoffee.cn（半自动意式咖啡机分档实测：德龙EC156 800内 / 迈拓EM-18 约1600 / 惠家210S 约3500 / 爱宝E61 京东8560）",
    ],
    "competitors": competitors,
    "hotProducts": hot_products,
    "dataSource": "WebSearch 真实数据 · 2026-10-11 cron 自动化抓取",
    "updateTime": f"{TODAY} 07:30",
}

# === Schema 校验 (与 validate_schema.py 对齐) ===
assert len(competitors) == 5, "competitors 必须 5 组"
for g in competitors:
    assert len(g["items"]) == 4, f"{g['product']} 应 4 项"
    assert g["items"][0].get("image", "").startswith("https://"), "每组第 1 项(主推)必须有 image"
assert len(hot_products) == 5, "hotProducts 必须 5 项"
for hp in hot_products:
    assert "image" in hp and hp["image"].startswith("https://"), "hotProducts 缺 image"
assert "dataSource" in vs and "updateTime" in vs

path = f"{OUT_DIR}/vs-data.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(vs, f, ensure_ascii=False, indent=2)

print(f"✅ vs-data.json 已生成: {path}")
print(f"   对比品类: {len(competitors)} 个 | 竞品条目: {sum(len(c['items']) for c in competitors)} 条")
print(f"   来源: {len(vs['sources'])} 个 | hotProducts: {len(hot_products)} 项")
