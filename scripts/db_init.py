#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""xhs-product-push SQLite 数据库初始化 (9/2 bug 预防)

建表 + NOT NULL 约束 + UNIQUE 约束,任何字段缺失都会写失败。
重复运行是 idempotent (CREATE TABLE IF NOT EXISTS)。
"""
import os
import sqlite3
import sys

DB_PATH = "/Users/xiaoan/WorkBuddy/xhs-product-push/xhs_push.db"


SCHEMA = """
-- 主表: 每次 cron 跑出一条 run
CREATE TABLE IF NOT EXISTS runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT    NOT NULL UNIQUE,         -- YYYY-MM-DD
    total_runs      INTEGER NOT NULL,
    product_count   INTEGER NOT NULL,
    update_time     TEXT    NOT NULL,
    status          TEXT    NOT NULL DEFAULT '运行中',
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- 主表: 每个 product (1 run 5 个)
CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL,
    product_id      INTEGER NOT NULL,                 -- 1-5 (run 内的编号)
    name            TEXT    NOT NULL,
    category        TEXT    NOT NULL,
    price           TEXT    NOT NULL,
    desc            TEXT    NOT NULL,
    suitable        TEXT    NOT NULL,
    price_note      TEXT    NOT NULL,
    color           TEXT    NOT NULL,
    image           TEXT    NOT NULL,                 -- ← 9/2 bug 预防: NOT NULL
    image_slice     TEXT,                             -- product_slice_*.jpg URL
    UNIQUE(run_id, product_id),
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);

-- 副表: 5 个亮点(一对多)
CREATE TABLE IF NOT EXISTS product_highlights (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_pk      INTEGER NOT NULL,
    idx             INTEGER NOT NULL,                 -- 1-5
    text            TEXT    NOT NULL,
    UNIQUE(product_pk, idx),
    FOREIGN KEY(product_pk) REFERENCES products(id) ON DELETE CASCADE
);

-- 副表: 卖点标签(一对多)
CREATE TABLE IF NOT EXISTS product_tags (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_pk      INTEGER NOT NULL,
    tag             TEXT    NOT NULL,
    UNIQUE(product_pk, tag),
    FOREIGN KEY(product_pk) REFERENCES products(id) ON DELETE CASCADE
);

-- 副表: 每个 product 的竞品 (5 个主推商品的对比)
CREATE TABLE IF NOT EXISTS product_competitors (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_pk      INTEGER NOT NULL,                 -- 关联到主推商品
    group_name      TEXT    NOT NULL,                 -- "宽肩加厚塑料衣架 7.9-60元区间"
    name            TEXT    NOT NULL,
    price           TEXT    NOT NULL,
    advantage       TEXT    NOT NULL,
    jd_sales        TEXT    NOT NULL,
    color           TEXT    NOT NULL,
    image           TEXT,                             -- 主推商品才填,其他竞品可空
    is_main         INTEGER NOT NULL DEFAULT 0,       -- 1 = 今日主推
    idx             INTEGER NOT NULL,                 -- 排序
    FOREIGN KEY(product_pk) REFERENCES products(id) ON DELETE CASCADE
);

-- 副表: 真实数据来源 (vs-data.json sources[])
CREATE TABLE IF NOT EXISTS competitor_sources (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL,
    source          TEXT    NOT NULL,
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);

-- 副表: hotProducts (5 项,landing page 热门商品区渲染用)
CREATE TABLE IF NOT EXISTS hot_products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL,
    idx             INTEGER NOT NULL,                 -- 1-5
    name            TEXT    NOT NULL,
    category        TEXT    NOT NULL,
    price           TEXT    NOT NULL,
    image           TEXT    NOT NULL,                 -- ← 9/2 bug 预防: NOT NULL
    sales           TEXT    NOT NULL,
    platform        TEXT    NOT NULL,
    UNIQUE(run_id, idx),
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);

-- 索引: 按日期快速查
CREATE INDEX IF NOT EXISTS idx_runs_date ON runs(date);
CREATE INDEX IF NOT EXISTS idx_products_run_id ON products(run_id);
CREATE INDEX IF NOT EXISTS idx_hot_products_run_id ON hot_products(run_id);
CREATE INDEX IF NOT EXISTS idx_competitors_product_pk ON product_competitors(product_pk);
"""


def init(db_path: str = DB_PATH) -> int:
    """建表。已存在则幂等。返回 row count (runs 表)"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
        # 统计
        cur = conn.execute("SELECT COUNT(*) FROM runs")
        n_runs = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM products")
        n_products = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM product_competitors")
        n_competitors = cur.fetchone()[0]
        print(f"✅ {db_path} 建表完成 (idempotent)")
        print(f"   runs: {n_runs} | products: {n_products} | competitors: {n_competitors}")
        print(f"   schema 约束:")
        print(f"   - products.image NOT NULL (防 9/2 漏图 bug)")
        print(f"   - hot_products.image NOT NULL (防 hotProducts 漏图)")
        print(f"   - product_competitors.image nullable (竞品可空,主推必填)")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    init()
