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
"""
import json
import os
import sqlite3
import sys
import time

DB_PATH = "/Users/xiaoan/WorkBuddy/xhs-product-push/xhs_push.db"
TASK_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push"


def _row_to_dict(row, cursor):
    return {c[0]: row[i] for i, c in enumerate(cursor.description)}


def _load_products(conn, run_id: int) -> list:
    cur = conn.execute(
        """SELECT id, product_id, name, category, price, desc, suitable, price_note, color, image, image_slice
        FROM products WHERE run_id = ? ORDER BY product_id""",
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

        data = {
            "date": run[1],
            "totalProducts": run[3],
            "products": _load_products(conn, run_id),
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

    # 写入 5 个位置
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

    print(f"\n🎉 {date_str} → 7 个 json 已导出, version={version}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: db_export.py <date> [version]")
        sys.exit(2)
    date = sys.argv[1]
    version = int(sys.argv[2]) if len(sys.argv) > 2 else None
    sys.exit(export(date, version))
