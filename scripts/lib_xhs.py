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
