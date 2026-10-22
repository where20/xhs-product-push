#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 SQLite 导出 data.json + vs-data.json (兼容 GitHub Pages 静态 fetch)

用法: python3 scripts/db_export.py <date>
      python3 scripts/db_export.py 2026-09-02

导出位置:
  - output/{date}/data.json       (主输出)
  - output/{date}/vs-data.json    (主输出)
  - v/{VERSION}/data.json         (版本化路径,bust CDN 缓存)
  - v/{VERSION}/vs-data.json
  - data.json (根目录 fallback)
  - vs-data.json
  - history/{date}.json           (history 同步)
  - history/history.json          (落地页时间线索引, 由上面这些文件自动重建)
"""
import json
import os
import sqlite3
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import (  # noqa: E402
    DB_PATH,
    TASK_DIR,
    build_history_index,
    derive_theme_color,
    published_stats,
)


def _row_to_dict(row, cursor):
    return {c[0]: row[i] for i, c in enumerate(cursor.description)}


def _has_column(conn, table, col):
    return col in {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def _load_products(conn, run_id: int) -> list:
    has_links = _has_column(conn, "products", "links")
    cols = "id, product_id, name, category, price, desc, suitable, price_note, color, image, image_slice"
    if has_links:
        cols += ", links"
    cur = conn.execute(
        f"SELECT {cols} FROM products WHERE run_id = ? ORDER BY product_id",
        (run_id,),
    )
    products = []
    for r in cur.fetchall():
        p = _row_to_dict(r, cur)
        pk = p.pop("id")
        p["id"] = p.pop("product_id")
        # highlights
        cur2 = conn.execute(
            "SELECT idx, text FROM product_highlights WHERE product_pk = ? ORDER BY idx",
            (pk,),
        )
        p["highlights"] = [row[1] for row in cur2.fetchall()]
        # tags
        cur2 = conn.execute(
            "SELECT tag FROM product_tags WHERE product_pk = ? ORDER BY id",
            (pk,),
        )
        p["tags"] = [row[0] for row in cur2.fetchall()]
        # images
        p["images"] = [p["image"]]
        if p.get("image_slice"):
            p["images"].append(p["image_slice"])
        p.pop("image_slice", None)
        # 真实商品页链接(db 里存的是 JSON 字符串)
        links = p.pop("links", None)
        if links:
            try:
                p["links"] = json.loads(links)
            except (TypeError, ValueError):
                p["links"] = None
        # 主题色: 由 color 现算, 不入库 —— 单一事实来源是 color
        p["theme_color"] = derive_theme_color(p.get("color", "#1C3A5F"))
        products.append(p)
    return products


def _load_competitors(conn, run_id: int) -> list:
    cur = conn.execute(
        """SELECT p.product_id, pc.group_name, pc.idx, pc.name, pc.price, pc.advantage, pc.jd_sales, pc.color, pc.image
        FROM product_competitors pc
        JOIN products p ON p.id = pc.product_pk
        WHERE p.run_id = ?
        ORDER BY p.product_id, pc.idx""",
        (run_id,),
    )
    groups = {}
    for r in cur.fetchall():
        product_id, group_name, idx, name, price, advantage, jd_sales, color, image = r
        if group_name not in groups:
            groups[group_name] = []
        item = {
            "name": name,
            "price": price,
            "advantage": advantage,
            "jd_sales": jd_sales,
            "color": color,
        }
        if image:
            item["image"] = image
        groups[group_name].append(item)
    return [{"product": k, "items": v} for k, v in groups.items()]


def _load_hot_products(conn, run_id: int) -> list:
    cur = conn.execute(
        "SELECT idx, name, category, price, image, sales, platform FROM hot_products WHERE run_id = ? ORDER BY idx",
        (run_id,),
    )
    return [
        {"name": n, "category": cat, "price": p, "image": img, "sales": s, "platform": plat}
        for idx, n, cat, p, img, s, plat in cur.fetchall()
    ]


def _load_sources(conn, run_id: int) -> list:
    cur = conn.execute(
        "SELECT source FROM competitor_sources WHERE run_id = ? ORDER BY id",
        (run_id,),
    )
    return [r[0] for r in cur.fetchall()]


def export(date_str: str, version: int = None) -> int:
    if version is None:
        version = int(time.time())

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "SELECT id, date, total_runs, product_count, update_time, status FROM runs WHERE date = ?",
            (date_str,),
        )
        run = cur.fetchone()
        if not run:
            print(f"❌ runs 表里没 {date_str} 数据,先跑 db_save.py")
            return 1
        run_id = run[0]
        products = _load_products(conn, run_id)

        # 发布即成功: db_export 是落库后的最后一步, 能走到这里说明本次 run 已完成。
        # (历史遗留的 37 条 "运行中" 也在这里被归正 —— 配合 db_save 的同义更新。)
        conn.execute("UPDATE runs SET status = '已完成' WHERE id = ?", (run_id,))
        conn.commit()

        # 统计口径与 build_data.py 完全一致:
        #   history/ 已发布天数(不含当天) + 当天
        # 两处用同一个 published_stats(), 避免"脚本算一套、页面显示另一套"。
        stats = published_stats(exclude_dates=(date_str,))

        data = {
            "date": run[1],
            "totalProducts": run[3],
            "totalRuns": stats["totalRuns"] + 1,
            "totalProductImages": stats["totalProductImages"] + len(products),
            "lastRunDate": date_str,
            "status": "已完成",
            "updateTime": run[4],
            "products": products,
        }
        vs = {
            "date": run[1],
            "sources": _load_sources(conn, run_id),
            "competitors": _load_competitors(conn, run_id),
            "hotProducts": _load_hot_products(conn, run_id),
            "dataSource": "WebSearch 真实数据 · SQLite db 导出",
            "updateTime": run[4],
        }
    finally:
        conn.close()

    # 写入 7 个位置
    out_dir = os.path.join(TASK_DIR, "output", date_str)
    v_dir = os.path.join(TASK_DIR, "v", str(version))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(v_dir, exist_ok=True)

    targets = [
        (os.path.join(out_dir, "data.json"), data),
        (os.path.join(out_dir, "vs-data.json"), vs),
        (os.path.join(v_dir, "data.json"), data),
        (os.path.join(v_dir, "vs-data.json"), vs),
        (os.path.join(TASK_DIR, "data.json"), data),
        (os.path.join(TASK_DIR, "vs-data.json"), vs),
        (os.path.join(TASK_DIR, "history", f"{date_str}.json"), data),
    ]
    for path, payload in targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        size = os.path.getsize(path)
        rel = path.replace(TASK_DIR + "/", "")
        print(f"  📄 {rel} ({size}B)")

    # 第 8 个产物: history/history.json —— 落地页"历史记录"时间线索引。
    # 以前靠 prompt.md 的内联脚本手工追加, 38 条 status 全停在"运行中"。
    # 现在由 history/{date}.json 自动重建, 不再需要手工维护。
    hpath, hentries = build_history_index()
    print(f"  📄 history/history.json ({os.path.getsize(hpath)}B, {len(hentries)} 条)")

    print(f"\n🎉 {date_str} → 8 个 json 已导出, version={version}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: db_export.py <date> [version]")
        sys.exit(2)
    date = sys.argv[1]
    version = int(sys.argv[2]) if len(sys.argv) > 2 else None
    sys.exit(export(date, version))
