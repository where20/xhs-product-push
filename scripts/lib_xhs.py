#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lib_xhs.py — xhs-product-push 公共脚手架

存在意义
--------
在这个仓库里, 「代码」和「内容」曾经被混在一起:
  - 每天生成一个 250 行的 build_data_YYYYMMDD.py / build_vs_data_YYYYMMDD.py
  - 其中 ~40 行是每次都一样的样板 (TODAY / OUT_DIR / IMG_BASE / 断言 / main)
  - 样板被复制 58 份, 改一次逻辑要改 58 个文件 → 迟早漏改, 也迟早出事

现在的分工:
  - **内容**(每天不同) → 写进 output/{date}/products.json / vs.json / prompts.txt
  - **代码**(长期不变) → 本模块 + build_data.py / build_vs_data.py / gen_images.sh /
    compose_cards.py, 全部接受日期参数, 每天复用同一份

本模块提供:
  - 日期解析 (argparse / 环境变量 / 默认今天)
  - 路径常量 (OUT_DIR / IMG_BASE / TASK_DIR)
  - schema 断言 (data.json / vs-data.json)
  - JSON 读写
"""
import colorsys
import json
import os
import re
import sys
from datetime import datetime

# === 路径 ===
TASK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_DIR = os.path.join(TASK_DIR, "history")
VERSION_DIR = os.path.join(TASK_DIR, "v")
MEMORY_DIR = os.path.join(TASK_DIR, "memory")
# DB 路径从 TASK_DIR 推导, 不再硬编码绝对路径(2026-10-22 优化)
DB_PATH = os.path.join(TASK_DIR, "xhs_push.db")

# 图床 (与 config/env.json 的 image_hosts.primary 对齐, 勿硬编码其它域名)
IMG_HOST = os.environ.get("IMG_HOST_PRIMARY", "https://cloudimgs.iepose.cn")
IMG_BASE_TMPL = IMG_HOST + "/api/images/{date}"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def resolve_date(argv=None):
    """解析日期参数。支持:
       1) 位置参数  python3 build_data.py 2026-10-21
       2) 环境变量 XHS_DATE=2026-10-21
       3) 默认今天
       会校验格式, 非法日期直接报错退出(而不是悄悄写错目录)。"""
    argv = list(sys.argv[1:] if argv is None else argv)
    for a in argv:
        if a.startswith("--date="):
            argv = [a.split("=", 1)[1]] + [x for x in argv if x != a]
            break
    for a in argv:
        if not a.startswith("-"):
            d = a
            break
    else:
        d = os.environ.get("XHS_DATE") or datetime.now().strftime("%Y-%m-%d")
    if not DATE_RE.match(d):
        die(f"❌ 日期格式非法: {d!r} (应为 YYYY-MM-DD)")
    try:
        datetime.strptime(d, "%Y-%m-%d")
    except ValueError:
        die(f"❌ 日期不存在: {d!r}")
    return d


def out_dir(date):
    return os.path.join(TASK_DIR, "output", date)


def history_count():
    """history/ 下已发布的**每日**数据文件个数(= 已产出天数)。
    注意排除 history.json 本身(它是时间线索引, 不是某一天的数据)。"""
    if not os.path.isdir(HISTORY_DIR):
        return 0
    return len(history_day_files())


def history_day_files():
    """history/ 下形如 2026-10-22.json 的每日数据文件列表(已排序)。"""
    if not os.path.isdir(HISTORY_DIR):
        return []
    out = []
    for fn in os.listdir(HISTORY_DIR):
        if not fn.endswith(".json") or fn == "history.json":
            continue
        if not DATE_RE.match(fn[:-5]):
            continue
        out.append(fn[:-5])
    return sorted(out)


def published_stats(exclude_dates=()):
    """统计已发布数据, 供落地页"运行实况"卡片与 history 时间线共用。

    事实来源 = history/{date}.json(每个已发布日一个文件), 而不是 db.runs:
    2026-09-11 有发布数据但 db 里没有 run 行(历史空档), 只有文件口径才完整。
    """
    exclude = set(exclude_dates)
    days = []
    for d in history_day_files():
        if d in exclude:
            continue
        try:
            obj = read_json(os.path.join(HISTORY_DIR, f"{d}.json"))
        except Exception:
            continue
        days.append((d, len(obj.get("products", []) or [])))
    days.sort()
    return {
        "totalRuns": len(days),
        "totalProductImages": sum(n for _, n in days),
        "lastRunDate": days[-1][0] if days else None,
    }


def build_history_index():
    """从 history/{date}.json 重建 history/history.json(落地页时间线索引)。

    为什么要有这个函数:
      以前 history/history.json 靠 prompt.md 里的一段内联脚本手工追加 ——
      那段脚本还出过错(memory/2026-10-20 记着"prompt.md 里 history.json 的
      内联脚本是坏的"), 结果 38 条记录的 status 全部停在"运行中"。
      现在它由 db_export 自动重建, 单一事实来源 = history/{date}.json。

    返回 (路径, 条目列表)
    """
    import sqlite3
    days = []
    for d in history_day_files():
        path = os.path.join(HISTORY_DIR, f"{d}.json")
        try:
            obj = read_json(path)
        except Exception:
            continue
        prods = obj.get("products", []) or []
        update_time = obj.get("updateTime")
        if not update_time:
            update_time = None
        days.append({
            "date": d,
            "totalRuns": len(days) + 1,
            "productCount": len(prods),
            "updateTime": update_time,
            "status": obj.get("status") or "已完成",
        })

    # updateTime 缺失时从 db.runs 补(历史文件没有这个字段)
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            rows = conn.execute(
                "SELECT date, update_time FROM runs"
            ).fetchall()
            db_map = {r[0]: r[1] for r in rows}
        finally:
            conn.close()
    except Exception:
        db_map = {}
    for e in days:
        if not e["updateTime"]:
            e["updateTime"] = db_map.get(e["date"]) or f"{e['date']} 07:30"

    path = os.path.join(HISTORY_DIR, "history.json")
    write_json(path, days)
    return path, days


def img_base(date):
    return IMG_BASE_TMPL.format(date=date)


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


# === schema 断言 ===

# === 颜色工具 (2026-10-22 深度优化) ===
#
# 背景: products.json 的 `color` 语义是"商品主色"(通常是浅色 pastel:
#       灰垫/金键盘/奶白机/白喂食器/粉香水)。早期 compose_cards.py 直接拿它
#       当底色配白字 —— 实测 155 张历史卡片里 85 张(54.8%)白字对比度 < 4.5:1,
#       40 张(25.8%)< 2.5:1 属严重不可读, 而这 5 张切片正是每天推进飞书群的图。
#
# 方案: 保留"商品主色"语义, 派生一个**可读主题色**(同色相、只压暗 lightness,
#       压到对白字 ≥4.5:1)。派生色同时满足两处用法:
#         · 当底色配白字(色条/标签 chip/价格条)
#         · 当白底上的字色(标题/分隔线/小标题)

DEFAULT_THEME_COLOR = "#1C3A5F"          # 兜底深蓝, 对白字 10.9:1
DEFAULT_THEME_RGB = (0x1C, 0x3A, 0x5F)
WHITE = (255, 255, 255)
HEX_RE = re.compile(r"^[0-9a-fA-F]{6}$")


def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = (_srgb_to_linear(x / 255) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1, rgb2=WHITE):
    """WCAG 2.1 对比度, 取值 1.0 ~ 21.0"""
    l1, l2 = relative_luminance(rgb1), relative_luminance(rgb2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def safe_hex_to_rgb(hexstr, fallback=None):
    """容错解析 #RRGGBB(也接受 3 位 shorthand)。非法值返回 fallback, 不抛异常。

    历史上 35 处 color 是 '中国红礼盒 / 烫金书法字' 这种描述串(旧 schema 遗留),
    曾把 compose_cards 整个打挂。现在由 assert_data 早失败, 这里做二次保险。
    """
    fb = fallback if isinstance(fallback, tuple) else DEFAULT_THEME_RGB
    if isinstance(hexstr, str):
        h = hexstr.strip().lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if HEX_RE.match(h):
            return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return fb


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def derive_theme_color(hex_color, min_ratio=4.5):
    """把"商品主色"派生成"可读主题色"。

    做法: 在 HSL 空间只压暗 lightness(色相与饱和度保持不变), 取第一个
          对白字对比度 >= min_ratio 的颜色。色相不变 → 视觉上仍是"这个商品的颜色",
          但标题/色条/标签/价格条全部可读。已经够深的颜色原样返回。
    """
    rgb = safe_hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(*[c / 255 for c in rgb])
    for i in range(101):
        ll = l * (1 - i / 100.0)
        cand = tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, ll, s))
        if contrast_ratio(cand) >= min_ratio:
            return rgb_to_hex(cand)
    return DEFAULT_THEME_COLOR


def is_hex_color(value):
    """严格判断是否为合法 #RRGGBB / #RGB / RRGGBB。"""
    if not isinstance(value, str):
        return False
    h = value.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return bool(HEX_RE.match(h))


def theme_color_for(product):
    """取某商品的可读主题色。
    优先用已有的 theme_color(由 build_data 写入), 否则从 color 现算。
    这样 compose_cards 对**旧 data.json**(没有 theme_color 字段)也能直接跑。"""
    tc = product.get("theme_color")
    if is_hex_color(tc):
        return tc
    return derive_theme_color(product.get("color", DEFAULT_THEME_COLOR))


def assert_links(links, pid):
    """links 结构校验 —— 带货链路的数据闸门。

    约定:
      {"primary": "https://真实商品页", "source": "苏宁", ...}
    · 必须是 dict
    · primary 必须是 http(s) 真实链接(不允许空串 / 搜索占位 / javascript:)
    · 其余键(jd/taobao/pdd/extra...)若存在也必须是 http(s)
    """
    if links is None:
        return True
    if not isinstance(links, dict):
        raise AssertionError(f"❌ product {pid} links 必须是对象, 实际 {type(links).__name__}")
    for k, v in links.items():
        if k == "source":
            continue
        if isinstance(v, list):
            vals = v
        else:
            vals = [v]
        for item in vals:
            if not isinstance(item, str) or not item.startswith(("http://", "https://")):
                raise AssertionError(
                    f"❌ product {pid} links.{k} 必须是 http(s) 链接, 实际 {item!r}"
                )
    return True


def assert_data(data, expect_products=None):
    """data.json 结构校验。失败即 raise —— 坏数据不许流到落库和发布。"""
    for key in ("date", "totalProducts", "products"):
        if key not in data:
            raise AssertionError(f"❌ data.json 缺字段: {key}")
    prods = data["products"]
    if expect_products is not None and len(prods) != expect_products:
        raise AssertionError(f"❌ 商品数应为 {expect_products}, 实际 {len(prods)}")
    if data["totalProducts"] != len(prods):
        raise AssertionError(
            f"❌ totalProducts({data['totalProducts']}) != len(products)({len(prods)})"
        )
    for p in prods:
        pid = p.get("id")
        if "image" not in p:
            raise AssertionError(f"❌ product {pid} 缺 image 字段")
        if not p["image"].startswith("https://"):
            raise AssertionError(f"❌ product {pid} image 必须 CDN URL: {p['image']!r}")
        if "images" not in p or len(p["images"]) < 1:
            raise AssertionError(f"❌ product {pid} 缺 images 数组")
        if len(p.get("highlights", [])) != 5:
            raise AssertionError(f"❌ product {pid} highlights 必须 5 条")
        if len(p.get("tags", [])) != 5:
            raise AssertionError(f"❌ product {pid} tags 必须 5 个")
        if len(p.get("desc", "")) < 150:
            raise AssertionError(
                f"❌ product {pid} desc 不足 150 字 (实际 {len(p.get('desc', ''))})"
            )
        if not str(p.get("price", "")).strip():
            raise AssertionError(f"❌ product {pid} price 为空")
        # color 早失败: 历史上 35 处 color 写成了 '中国红礼盒 / 烫金书法字' 这种
        # 描述串, 会一路带到合成脚本才炸。这里直接拦住并说清楚该写什么。
        if not is_hex_color(p.get("color")):
            raise AssertionError(
                f"❌ product {pid} color 非法: {p.get('color')!r}\n"
                f"   color 必须是 #RRGGBB 十六进制色值(如 #E8DCC8), "
                f"不能写'中国红'这类中文描述 —— 它会被当成主题色直接刷到卡片上"
            )
        if p.get("theme_color") and not is_hex_color(p["theme_color"]):
            raise AssertionError(
                f"❌ product {pid} theme_color 非法: {p.get('theme_color')!r}"
            )
        assert_links(p.get("links"), pid)
    return True


def assert_vs_data(vs, expect_hot=5, min_competitors=4):
    """vs-data.json 结构校验。

    ⚠️ min_competitors=4 是 validate_schema.py 的硬约束, 每组竞品必须 ≥4 项。
       (10-19 曾因只写 3 项被 validate 拦下)
    """
    for key in ("date", "sources", "competitors", "hotProducts", "dataSource", "updateTime"):
        if key not in vs:
            raise AssertionError(f"❌ vs-data.json 缺字段: {key}")
    if len(vs["hotProducts"]) != expect_hot:
        raise AssertionError(
            f"❌ hotProducts 必须 {expect_hot} 项, 实际 {len(vs['hotProducts'])}"
        )
    for hp in vs["hotProducts"]:
        if "image" not in hp or not hp["image"].startswith("https://"):
            raise AssertionError(f"❌ hotProducts 缺 CDN image: {hp.get('name')}")
    for i, g in enumerate(vs["competitors"], 1):
        n = len(g.get("items", []))
        if n < min_competitors:
            raise AssertionError(
                f"❌ 竞品组 {i} 仅 {n} 项, 至少需 {min_competitors} 项"
            )
        for it in g["items"]:
            if "image" not in it or not it["image"].startswith("https://"):
                raise AssertionError(f"❌ 竞品缺 CDN image: {it.get('name')}")
    if len(vs["sources"]) < 10:
        raise AssertionError(f"❌ sources 仅 {len(vs['sources'])} 条, 至少 10 条")
    return True


def attach_images(data, date):
    """给每个 product 补 image / images (CDN URL 模板), 幂等。"""
    base = img_base(date)
    for p in data["products"]:
        pid = p["id"]
        p["image"] = f"{base}_product_{pid}.jpg"
        p["images"] = [p["image"], f"{base}_product_slice_{pid}.jpg"]
    return data


if __name__ == "__main__":
    d = resolve_date()
    print(f"date={d}")
    print(f"out_dir={out_dir(d)}")
    print(f"img_base={img_base(d)}")
