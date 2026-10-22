#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_data.py — 通用版(替代 29 个 build_data_YYYYMMDD.py)

用法:
    python3 scripts/build_data.py [YYYY-MM-DD]
    # 默认今天; 也可用 XHS_DATE=2026-10-21

输入: output/{date}/products.json
      纯内容文件, 形如:
      [
        {"id":1, "name":"...", "category":"...", "price":"¥xx",
         "desc":"150-200字...", "highlights":["x5"], "tags":["x5"],
         "suitable":"...", "price_note":"...", "color":"#RRGGBB",
         "links":{"primary":"https://真实商品页", "source":"苏宁"}},
        ...
      ]
      (也接受 {"products":[...]} 包装形式)

输出: output/{date}/data.json  —— 结构与历史一致, landing page / db / 飞书全都兼容

设计要点:
  - image / images 字段由脚本按 CDN 模板自动补齐, 内容文件不写死 URL
  - theme_color 由 color 派生(对白字 ≥4.5:1), 卡片与落地页共用
  - links 直接透传, 落地页优先用真实商品页, 缺失时前端回退京东搜索
  - 顶层补 totalRuns / lastRunDate / status / updateTime 供落地页统计栏
  - schema 断言不通过直接 raise, 坏数据不会流到落库和发布
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import (  # noqa: E402
    attach_images,
    assert_data,
    derive_theme_color,
    out_dir,
    published_stats,
    resolve_date,
    write_json,
)


def load_products(path):
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    if isinstance(obj, dict):
        for key in ("products", "items", "data"):
            if key in obj:
                obj = obj[key]
                break
        else:
            raise AssertionError(
                "❌ products.json 是对象, 但没有 products/items/data 键"
            )
    if not isinstance(obj, list) or not obj:
        raise AssertionError("❌ products.json 必须是非空数组")
    return obj


def main():
    date = resolve_date()
    od = out_dir(date)
    src = os.path.join(od, "products.json")
    if not os.path.exists(src):
        print(
            f"❌ 找不到 {src}\n"
            f"   需要先写当日内容文件: {src}\n"
            f"   格式见本文件头部说明(5 个商品的数组, 每项含 name/category/price/"
            f"desc/highlights/tags/suitable/price_note/color)",
            file=sys.stderr,
        )
        sys.exit(2)

    products = load_products(src)
    no_links = []
    for i, p in enumerate(products, 1):
        p.setdefault("id", i)
        for key in ("name", "category", "price", "desc", "highlights", "tags"):
            if key not in p:
                raise AssertionError(f"❌ product {p.get('id')} 缺字段: {key}")
        p.setdefault("suitable", "")
        p.setdefault("price_note", p["price"])
        p.setdefault("color", "#1C3A5F")
        # 主题色: 把"商品主色"派生成对白字 ≥4.5:1 的可读色。
        # 写进 data.json, 供 compose_cards 与落地页共用同一套配色。
        p["theme_color"] = derive_theme_color(p["color"])
        if not p.get("links"):
            no_links.append(p["id"])

    # ---- 落地页"运行实况"卡片的数据 ----
    # 口径 = history/ 下已发布的每日数据文件(不含当天), 当天由本文件补上。
    # 这样 build_data 与 db_export(写完 history/{date}.json 后再算) 结果一致。
    stats = published_stats(exclude_dates=(date,))

    data = {
        "date": date,
        "totalProducts": len(products),
        "totalRuns": stats["totalRuns"] + 1,
        "totalProductImages": stats["totalProductImages"] + len(products),
        "lastRunDate": date,
        "status": "已完成",
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "products": attach_images({"products": products}, date)["products"],
    }
    assert_data(data)

    out = write_json(os.path.join(od, "data.json"), data)
    print(f"✅ data.json 生成并通过 schema 校验 → {out}")
    for p in data["products"]:
        link = (p.get("links") or {}).get("primary", "")
        print(
            f"   [{p['id']}] {p['name'][:34]} | {p['category']} | {p['price']} "
            f"| desc {len(p['desc'])}字 | 亮点{len(p['highlights'])} | 标签{len(p['tags'])} "
            f"| 色 {p['color']}→{p['theme_color']} | 链接 {link or '⚠️无'}"
        )
    if no_links:
        print(
            f"⚠️  product {no_links} 没有 links —— 落地页会回退到京东搜索链接。"
            f" 建议当天用 WebSearch 抓真实商品页写进 products.json 的 links.primary"
        )


if __name__ == "__main__":
    main()
