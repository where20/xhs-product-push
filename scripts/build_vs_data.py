#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_vs_data.py — 通用版(替代 29 个 build_vs_data_YYYYMMDD.py)

用法:
    python3 scripts/build_vs_data.py [YYYY-MM-DD]

输入: output/{date}/vs.json
      {
        "sources": ["真实来源 URL 或 站点名", ...],
        "competitors": [
          {"product": "品类 价位段",
           "items": [
             {"name":"...", "price":"¥xx", "advantage":"...",
              "jd_sales":"来源出处 + 销量/评论数", "color":"#RRGGBB"},
             ...          ← 每组至少 4 项(validate_schema 硬约束), 第 1 项为当日主推
           ]},
          ...
        ],
        "hotProducts": [
          {"name":"...", "category":"...", "price":"¥xx",
           "sales":"销量/排行摘要", "platform":"京东自营/天猫旗舰"},
          ...              ← 固定 5 项, 与 5 个主推商品一一对应
        ]
      }

输出: output/{date}/vs-data.json —— 结构与历史一致

脚本自动补的字段(内容文件不必写):
  - competitors[i].items[j].image  → 第 j 组主推用第 j 个商品的图, 其余沿用同组主推
  - hotProducts[i].image            → 第 i 个主推商品的图
  - date / dataSource / updateTime
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import (  # noqa: E402
    assert_vs_data,
    img_base,
    out_dir,
    read_json,
    resolve_date,
    write_json,
)


def main():
    date = resolve_date()
    od = out_dir(date)
    src = os.path.join(od, "vs.json")
    if not os.path.exists(src):
        print(
            f"❌ 找不到 {src}\n"
            f"   需要先写当日竞品内容文件: {src}\n"
            f"   格式见本文件头部说明(sources / competitors / hotProducts)",
            file=sys.stderr,
        )
        sys.exit(2)

    with open(src, "r", encoding="utf-8") as f:
        vs = json.load(f)

    base = img_base(date)
    # 配色来自当日主推商品(data.json), 竞品/爆款沿用所属组的商品色。
    # 这样内容文件不必写 color —— 少写 25 个色值 = 少 25 个出错机会。
    palette = {}
    dpath = os.path.join(od, "data.json")
    if os.path.exists(dpath):
        try:
            for p in read_json(dpath)["products"]:
                palette[p["id"]] = p.get("color", "#1C3A5F")
        except Exception:
            palette = {}

    competitors = vs.get("competitors") or []
    if not competitors:
        raise AssertionError("❌ vs.json 缺 competitors")
    for gi, grp in enumerate(competitors):
        items = grp.get("items") or []
        if not items:
            raise AssertionError(f"❌ 竞品组 {gi+1} 没有 items")
        main_img = f"{base}_product_{gi+1}.jpg"
        main_color = palette.get(gi + 1, "#1C3A5F")
        for it in items:
            it.setdefault("image", main_img)
            it.setdefault("color", main_color)

    hot = vs.get("hotProducts") or []
    for i, hp in enumerate(hot, 1):
        hp.setdefault("image", f"{base}_product_{i}.jpg")
        hp.setdefault("color", palette.get(i, "#1C3A5F"))

    data = {
        "date": date,
        "sources": vs.get("sources") or [],
        "competitors": competitors,
        "hotProducts": hot,
        "dataSource": vs.get(
            "dataSource", f"WebSearch 真实数据 · {date} cron 自动化抓取"
        ),
        "updateTime": vs.get("updateTime", f"{date} 07:30"),
    }
    assert_vs_data(data)

    out = write_json(os.path.join(od, "vs-data.json"), data)
    print(f"✅ vs-data.json 生成并通过 schema 校验 → {out}")
    print(f"   sources: {len(data['sources'])} 条")
    for i, g in enumerate(data["competitors"], 1):
        print(f"   组{i} {g['product']}: {len(g['items'])} 项")
    print(f"   hotProducts: {len(data['hotProducts'])} 项")


if __name__ == "__main__":
    main()
