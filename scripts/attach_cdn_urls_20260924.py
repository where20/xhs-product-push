#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attach_cdn_urls_20260924.py
读取 uploaded_urls.json 把 CDN URL 回填 data.json / vs-data.json (db 兼容格式)
"""
import json
from pathlib import Path

OUT_DIR = Path('/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-24')

with open(OUT_DIR / 'uploaded_urls.json', 'r', encoding='utf-8') as f:
    log = json.load(f)

url_map = {r['filename']: r['url'] for r in log['uploaded']}

# --- data.json: products[].image
with open(OUT_DIR / 'data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, p in enumerate(data['products']):
    fname = f"2026-09-24_product_{i+1}.jpg"
    if fname in url_map:
        p['image'] = url_map[fname]
        p['images'] = [url_map[fname]]

with open(OUT_DIR / 'data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"✅ data.json: 5 个商品 image URL 已回填")

# --- vs-data.json: hotProducts[].image + competitors[*].items[0].image
with open(OUT_DIR / 'vs-data.json', 'r', encoding='utf-8') as f:
    vs = json.load(f)

for i, hp in enumerate(vs['hotProducts']):
    fname = f"2026-09-24_product_{i+1}.jpg"
    if fname in url_map:
        hp['image'] = url_map[fname]

for grp_idx, grp in enumerate(vs['competitors']):
    pid = grp_idx + 1
    fname = f"2026-09-24_product_{pid}.jpg"
    if grp['items'] and fname in url_map:
        grp['items'][0]['image'] = url_map[fname]

with open(OUT_DIR / 'vs-data.json', 'w', encoding='utf-8') as f:
    json.dump(vs, f, ensure_ascii=False, indent=2)
print(f"✅ vs-data.json: hotProducts + competitors[*].items[0] image URL 已回填")