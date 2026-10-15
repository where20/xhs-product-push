#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attach_cdn_urls_20261016.py — 用 uploaded_urls.json 里的真实 CDN URL 覆盖 data.json / vs-data.json

⚠️ cloudimgs 上传后会追加时间戳后缀(如 2026-10-16_product_1_1792105526896_1.jpg),
   build 脚本里写的稳定名 URL 会被打脸, 必须用实际返回的 URL 回填。

映射规则(与 build_vs_data_20261016.py 的顺序一致):
  - data.json    products[i]        -> product_{i+1}.jpg + product_slice_{i+1}.jpg
  - vs-data.json competitors[c] 第1项 -> product_{c+1}.jpg   (今日主推)
  - vs-data.json hotProducts[i]     -> product_{i+1}.jpg
"""
import json
from pathlib import Path

TODAY = "2026-10-16"
BASE = Path(f"/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/{TODAY}")

log = json.load(open(BASE / "uploaded_urls.json", encoding="utf-8"))
# uploaded_urls.json 的 name 是本地相对路径(如 images/product_1.jpg), 这里归一化掉前缀
url_map = {u["name"].split("/")[-1]: u["url"] for u in log["uploaded"]}

need = [f"product_{i}.jpg" for i in range(1, 6)] + [f"product_slice_{i}.jpg" for i in range(1, 6)]
missing = [n for n in need if n not in url_map]
assert not missing, f"❌ uploaded_urls.json 缺少: {missing}"
assert all(url_map[n].startswith("https://") for n in need), "❌ 存在非 https URL"

# --- data.json ---
dp = BASE / "data.json"
d = json.load(open(dp, encoding="utf-8"))
for p in d["products"]:
    pid = p["id"]
    main_url = url_map[f"product_{pid}.jpg"]
    slice_url = url_map[f"product_slice_{pid}.jpg"]
    p["image"] = main_url
    p["images"] = [main_url, slice_url]
json.dump(d, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"✅ data.json: {len(d['products'])} 商品 image/images 已回填真实 CDN URL")

# --- vs-data.json ---
vp = BASE / "vs-data.json"
vs = json.load(open(vp, encoding="utf-8"))

for ci, cat in enumerate(vs["competitors"]):
    main_url = url_map[f"product_{ci + 1}.jpg"]
    cat["items"][0]["image"] = main_url

for hi, hp in enumerate(vs["hotProducts"]):
    hp["image"] = url_map[f"product_{hi + 1}.jpg"]

json.dump(vs, open(vp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"✅ vs-data.json: {len(vs['competitors'])} 品类主推 + {len(vs['hotProducts'])} 热销 image 已回填")

# --- 复核 ---
for p in d["products"]:
    assert p["image"].startswith("https://"), f"❌ p{p['id']} image"
    assert len(p["images"]) == 2
for hp in vs["hotProducts"]:
    assert hp["image"].startswith("https://"), f"❌ hotProduct {hp['name']} image"
for c in vs["competitors"]:
    assert c["items"][0]["image"].startswith("https://"), f"❌ {c['product']} 主推 image"
print("✅ CDN URL 回填复核通过")
