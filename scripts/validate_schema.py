#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Schema 校验 (从 SQLite 读,9/2 bug 预防)

用法: python3 scripts/validate_schema.py <date>
      python3 scripts/validate_schema.py 2026-09-02

校验内容(全部 NOT NULL 是 db 约束,这里只是报告):
- runs.date 唯一
- products 5 个, image NOT NULL
- hotProducts 5 个, image NOT NULL
- product_competitors 每组 4 项, 主推 is_main=1 且 image NOT NULL
- dataSource + updateTime 字段
"""
import json
import os
import sqlite3
import sys

DB_PATH = "/Users/xiaoan/WorkBuddy/xhs-product-push/xhs_push.db"
TASK_DIR = "/Users/xiaoan/WorkBuddy/xhs-product-push"


def validate_db(date_str: str) -> list:
    """从 db 校验,返回 error list"""
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"❌ db 不存在: {DB_PATH},先跑 db_init.py")
        return errors

    conn = sqlite3.connect(DB_PATH)
    try:
        # 1. runs
        cur = conn.execute(
            "SELECT id, total_runs, product_count, update_time, status FROM runs WHERE date = ?",
            (date_str,),
        )
        run = cur.fetchone()
        if not run:
            errors.append(f"❌ db.runs 缺 {date_str},先跑 db_save.py")
            return errors
        run_id, total_runs, product_count, update_time, status = run
        if product_count != 5:
            errors.append(f"❌ runs.product_count = {product_count}, 应为 5")

        # 2. products (image NOT NULL 是 db 约束,缺则前面就 raise 了)
        cur = conn.execute(
            "SELECT product_id, name, image FROM products WHERE run_id = ? ORDER BY product_id",
            (run_id,),
        )
        products = cur.fetchall()
        if len(products) != 5:
            errors.append(f"❌ products 应 5 个, db 里 {len(products)}")

        # 3. product_competitors
        cur = conn.execute(
            "SELECT COUNT(*) FROM product_competitors pc JOIN products p ON p.id = pc.product_pk WHERE p.run_id = ?",
            (run_id,),
        )
        n_comp = cur.fetchone()[0]
        if n_comp != 20:  # 5 组 × 4 项
            errors.append(f"❌ product_competitors 应 20, db 里 {n_comp}")

        # 4. 主推商品 (is_main=1) 必须有 image
        cur = conn.execute(
            """SELECT p.product_id, pc.name, pc.image
            FROM product_competitors pc
            JOIN products p ON p.id = pc.product_pk
            WHERE p.run_id = ? AND pc.is_main = 1
            ORDER BY p.product_id""",
            (run_id,),
        )
        for pid, name, image in cur.fetchall():
            if not image:
                errors.append(f"❌ 主推竞品[product {pid}] '{name[:30]}' 缺 image")

        # 5. hot_products (image NOT NULL)
        cur = conn.execute(
            "SELECT idx, name, image FROM hot_products WHERE run_id = ? ORDER BY idx",
            (run_id,),
        )
        hot = cur.fetchall()
        if len(hot) != 5:
            errors.append(f"❌ hot_products 应 5, db 里 {len(hot)}")

        # 6. sources
        cur = conn.execute(
            "SELECT COUNT(*) FROM competitor_sources WHERE run_id = ?",
            (run_id,),
        )
        n_src = cur.fetchone()[0]
        if n_src < 5:
            errors.append(f"❌ competitor_sources 应 ≥5, db 里 {n_src}")

        # 7. updateTime 不空
        if not update_time:
            errors.append("❌ runs.update_time 空")
    finally:
        conn.close()

    return errors


def validate_json(date_str: str) -> list:
    """从 output/{date}/json 校验 (向后兼容)"""
    errors = []
    out_dir = os.path.join(TASK_DIR, "output", date_str)
    data_path = os.path.join(out_dir, "data.json")
    vs_path = os.path.join(out_dir, "vs-data.json")

    if not os.path.exists(data_path):
        errors.append(f"❌ {data_path} 不存在")
    else:
        with open(data_path, encoding="utf-8") as f:
            d = json.load(f)
        for p in d.get("products", []):
            if "image" not in p:
                errors.append(f"❌ product {p.get('id')} 缺 image 字段")
            elif not p["image"].startswith("https://"):
                errors.append(
                    f"❌ product {p.get('id')} image 必须 CDN URL, 实际: {p['image'][:60]}"
                )

    if not os.path.exists(vs_path):
        errors.append(f"❌ {vs_path} 不存在")
    else:
        with open(vs_path, encoding="utf-8") as f:
            vs = json.load(f)
        if "hotProducts" not in vs:
            errors.append("❌ vs-data.json 缺 hotProducts 字段")
        for i, hp in enumerate(vs.get("hotProducts", [])):
            if "image" not in hp:
                errors.append(f"❌ hotProducts[{i}] 缺 image 字段")
        if "dataSource" not in vs:
            errors.append("❌ vs-data.json 缺 dataSource")
        if "updateTime" not in vs:
            errors.append("❌ vs-data.json 缺 updateTime")
    return errors


def main():
    if len(sys.argv) < 2:
        print("用法: validate_schema.py <date>")
        sys.exit(2)
    date_str = sys.argv[1]

    print(f"🔍 {date_str} schema 校验 (db + json 双轨)\n")

    db_errors = validate_db(date_str)
    json_errors = validate_json(date_str)
    all_errors = db_errors + json_errors

    if all_errors:
        print(f"❌ 共 {len(all_errors)} 个错误:")
        for e in all_errors:
            print(f"  {e}")
        print("\n修复: 参考 prompt.md step 6/7/12.5,补全字段后重跑")
        return 1
    else:
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.execute(
                "SELECT total_runs, product_count FROM runs WHERE date = ?", (date_str,)
            )
            run = cur.fetchone()
            cur = conn.execute(
                "SELECT COUNT(*) FROM products pr JOIN runs r ON pr.run_id = r.id WHERE r.date = ?",
                (date_str,),
            )
            n_products = cur.fetchone()[0]
            cur = conn.execute(
                """SELECT COUNT(*) FROM product_competitors pc
                JOIN products p ON p.id = pc.product_pk
                JOIN runs r ON r.id = p.run_id WHERE r.date = ?""",
                (date_str,),
            )
            n_comp = cur.fetchone()[0]
            cur = conn.execute(
                "SELECT COUNT(*) FROM hot_products hp JOIN runs r ON hp.run_id = r.id WHERE r.date = ?",
                (date_str,),
            )
            n_hot = cur.fetchone()[0]
            cur = conn.execute(
                "SELECT COUNT(*) FROM competitor_sources cs JOIN runs r ON cs.run_id = r.id WHERE r.date = ?",
                (date_str,),
            )
            n_src = cur.fetchone()[0]
        finally:
            conn.close()
        print(f"✅ {date_str} schema 校验通过")
        print(f"  - runs: total_runs={run[0]} product_count={run[1]}")
        print(f"  - products: {n_products} (均含 image NOT NULL)")
        print(f"  - product_competitors: {n_comp}")
        print(f"  - hot_products: {n_hot} (均含 image NOT NULL)")
        print(f"  - competitor_sources: {n_src}")
        print(f"  - data.json + vs-data.json + history/{date_str}.json + 根目录 + v/{{VERSION}}/ 全部就绪")
        return 0


if __name__ == "__main__":
    sys.exit(main())
