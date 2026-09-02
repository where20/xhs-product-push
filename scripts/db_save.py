#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 data.json + vs-data.json 写 SQLite (9/2 bug 预防)

用法: python3 scripts/db_save.py <date>
      python3 scripts/db_save.py 2026-09-02

如果 LLM 漏 image 字段,自动从 cloudimgs URL 补全(前提是 product_slice_*.jpg
已上传)。schema 缺失则 raise(防 9/2 bug)。
"""
import json
import os
import sqlite3
import sys

DB_PATH = "/Users/xiaoan/WorkBuddy/xhs-product-push/xhs_push.db"
TASK_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push"


def _img_base(date_str: str) -> str:
    return f"https://cloudimgs.iepose.cn/api/images/{date_str}"


def save(date_str: str) -> int:
    out_dir = os.path.join(TASK_DIR, "output", date_str)
    data_path = os.path.join(out_dir, "data.json")
    vs_path = os.path.join(out_dir, "vs-data.json")
    img_urls_path = os.path.join(out_dir, "image_urls.json")

    if not os.path.exists(data_path):
        print(f"❌ {data_path} 不存在")
        return 1
    if not os.path.exists(vs_path):
        print(f"❌ {vs_path} 不存在")
        return 1

    # 读 data
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("products", [])
    if len(products) != 5:
        print(f"❌ products 必须 5 项, 实际 {len(products)}")
        return 1

    # 读 vs-data
    with open(vs_path, encoding="utf-8") as f:
        vs = json.load(f)
    competitors = vs.get("competitors", [])
    hot_products = vs.get("hotProducts", [])
    sources = vs.get("sources", [])

    if len(competitors) != 5:
        print(f"❌ competitors 必须 5 组, 实际 {len(competitors)}")
        return 1
    if len(hot_products) != 5:
        print(f"❌ hotProducts 必须 5 项, 实际 {len(hot_products)}")
        return 1

    # 读 uploaded image_urls(优先用)
    img_urls = {}
    if os.path.exists(img_urls_path):
        with open(img_urls_path, encoding="utf-8") as f:
            u = json.load(f)
        img_urls = {int(k): v for k, v in u.get("images", {}).items()}

    # === 自动补全 image 字段(LLM 漏的) ===
    img_base = _img_base(date_str)
    for p in products:
        if not p.get("image"):
            pid = p["id"]
            # 优先用 uploaded_urls,否则用 cloudimgs URL 模板
            p["image"] = img_urls.get(pid) or f"{img_base}_product_{pid}.jpg"
            print(f"  🔧 product {pid} 补 image: {p['image']}")
        if not p.get("images") or not isinstance(p.get("images"), list):
            pid = p["id"]
            p["images"] = [p["image"], f"{img_base}_product_slice_{pid}.jpg"]
    for hp in hot_products:
        if not hp.get("image"):
            print(f"  ❌ hotProducts 缺 image 字段(必须 LLM 显式提供)")
            return 1
    for grp_idx, grp in enumerate(competitors):
        if not grp["items"][0].get("image"):
            pid = grp_idx + 1
            grp["items"][0]["image"] = img_urls.get(pid) or f"{img_base}_product_{pid}.jpg"
            print(f"  🔧 competitor[{grp_idx}].items[0] 补 image: {grp['items'][0]['image']}")

    # 写 db
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        # 如果同日已存在 run,先删除(覆盖语义)
        cur = conn.execute("SELECT id FROM runs WHERE date = ?", (date_str,))
        existing = cur.fetchone()
        if existing:
            run_id = existing[0]
            print(f"  ⚠️ run {date_str} 已存在 (id={run_id}),覆盖")
            conn.execute("DELETE FROM runs WHERE id = ?", (run_id,))

        # 1. runs
        # 算 total_runs = max(id)+1
        cur = conn.execute("SELECT MAX(id) FROM runs")
        max_id = cur.fetchone()[0] or 0
        total_runs = max_id + 1
        cur = conn.execute(
            "INSERT INTO runs (date, total_runs, product_count, update_time, status) VALUES (?,?,?,?,?)",
            (date_str, total_runs, 5, f"{date_str} 07:30", "运行中"),
        )
        run_id = cur.lastrowid
        print(f"  ✅ runs.id={run_id} (date={date_str}, total_runs={total_runs})")

        # 2. products + highlights + tags
        for p in products:
            cur = conn.execute(
                """INSERT INTO products
                (run_id, product_id, name, category, price, desc, suitable, price_note, color, image, image_slice)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    run_id,
                    p["id"],
                    p["name"],
                    p["category"],
                    p["price"],
                    p["desc"],
                    p.get("suitable", ""),
                    p.get("price_note", ""),
                    p.get("color", "#000000"),
                    p["image"],
                    p.get("images", [None])[1] if len(p.get("images", [])) > 1 else None,
                ),
            )
            product_pk = cur.lastrowid
            for i, hl in enumerate(p.get("highlights", []), 1):
                conn.execute(
                    "INSERT INTO product_highlights (product_pk, idx, text) VALUES (?,?,?)",
                    (product_pk, i, hl),
                )
            for tag in p.get("tags", []):
                conn.execute(
                    "INSERT INTO product_tags (product_pk, tag) VALUES (?,?)",
                    (product_pk, tag),
                )
        print(f"  ✅ products: 5 个, highlights + tags 已写入")

        # 3. competitors (5 组, 每组 4 项, 第 1 项是主推)
        n_competitors = 0
        for grp_idx, grp in enumerate(competitors):
            for idx, it in enumerate(grp.get("items", [])):
                # product_pk 关联到当日第 grp_idx+1 个 product
                cur = conn.execute(
                    "SELECT id FROM products WHERE run_id = ? AND product_id = ?",
                    (run_id, grp_idx + 1),
                )
                product_pk = cur.fetchone()[0]
                conn.execute(
                    """INSERT INTO product_competitors
                    (product_pk, group_name, name, price, advantage, jd_sales, color, image, is_main, idx)
                    VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (
                        product_pk,
                        grp.get("product", ""),
                        it["name"],
                        it["price"],
                        it.get("advantage", ""),
                        it.get("jd_sales", ""),
                        it.get("color", "#000000"),
                        it.get("image", ""),
                        1 if idx == 0 else 0,
                        idx,
                    ),
                )
                n_competitors += 1
        print(f"  ✅ product_competitors: {n_competitors} 项 (5 组 × 4 项)")

        # 4. sources
        for src in sources:
            conn.execute(
                "INSERT INTO competitor_sources (run_id, source) VALUES (?,?)",
                (run_id, src),
            )
        print(f"  ✅ competitor_sources: {len(sources)} 项")

        # 5. hot_products
        for i, hp in enumerate(hot_products, 1):
            conn.execute(
                """INSERT INTO hot_products
                (run_id, idx, name, category, price, image, sales, platform)
                VALUES (?,?,?,?,?,?,?,?)""",
                (
                    run_id,
                    i,
                    hp["name"],
                    hp.get("category", ""),
                    hp["price"],
                    hp["image"],
                    hp.get("sales", ""),
                    hp.get("platform", ""),
                ),
            )
        print(f"  ✅ hot_products: 5 项")

        conn.commit()
        print(f"\n🎉 {date_str} 全部数据已落 SQLite")
        return 0
    except sqlite3.IntegrityError as e:
        print(f"❌ SQLite 约束失败: {e}")
        print(f"   (通常是 NOT NULL 字段缺失,如 image / hotProducts)")
        conn.rollback()
        return 1
    except Exception as e:
        print(f"❌ 写入失败: {e}")
        conn.rollback()
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: db_save.py <date>")
        sys.exit(2)
    sys.exit(save(sys.argv[1]))
