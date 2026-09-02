#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data.json + vs-data.json schema 校验 (9/2 bug 预防)

用法: python3 scripts/validate_schema.py <date>
      python3 scripts/validate_schema.py 2026-09-03
"""
import json
import os
import sys


def validate(date_str: str) -> int:
    task_dir = "/Users/xiaoan/WorkBuddy/xhs-product-push"
    out_dir = os.path.join(task_dir, "output", date_str)
    if not os.path.isdir(out_dir):
        print(f"❌ output 目录不存在: {out_dir}")
        return 1

    errors = []

    # === 1. data.json product 必含 image + images[] 字段 ===
    data_path = os.path.join(out_dir, "data.json")
    if not os.path.exists(data_path):
        errors.append(f"❌ {data_path} 不存在")
    else:
        try:
            with open(data_path, encoding="utf-8") as f:
                d = json.load(f)
            if "products" not in d:
                errors.append("❌ data.json 缺 products 字段")
            else:
                for p in d["products"]:
                    pid = p.get("id", "?")
                    if "image" not in p:
                        errors.append(f"❌ product {pid} 缺 image 字段")
                    elif not p["image"].startswith("https://"):
                        errors.append(
                            f"❌ product {pid} image 必须 CDN URL (https://), 实际: {p['image'][:60]}"
                        )
                    if "images" not in p or not isinstance(p.get("images"), list) or len(p["images"]) < 1:
                        errors.append(f"❌ product {pid} 缺 images[] 数组(landing page 渲染用)")
        except Exception as e:
            errors.append(f"❌ data.json 解析失败: {e}")

    # === 2. vs-data.json 必含 hotProducts + dataSource + updateTime ===
    vs_path = os.path.join(out_dir, "vs-data.json")
    if not os.path.exists(vs_path):
        errors.append(f"❌ {vs_path} 不存在")
    else:
        try:
            with open(vs_path, encoding="utf-8") as f:
                vs = json.load(f)
            if "hotProducts" not in vs:
                errors.append("❌ vs-data.json 缺 hotProducts 字段(热门商品区域渲染用)")
            elif len(vs["hotProducts"]) != 5:
                errors.append(f"❌ hotProducts 必须 5 项, 实际 {len(vs['hotProducts'])}")
            else:
                for i, hp in enumerate(vs["hotProducts"]):
                    if "image" not in hp:
                        errors.append(f"❌ hotProducts[{i}] 缺 image 字段")
                    elif not hp["image"].startswith("https://"):
                        errors.append(
                            f"❌ hotProducts[{i}] image 必须 CDN URL, 实际: {hp['image'][:60]}"
                        )
            if "dataSource" not in vs:
                errors.append("❌ vs-data.json 缺 dataSource 字段")
            if "updateTime" not in vs:
                errors.append("❌ vs-data.json 缺 updateTime 字段")
        except Exception as e:
            errors.append(f"❌ vs-data.json 解析失败: {e}")

    # === 报告 ===
    if errors:
        print(f"❌ {date_str} schema 校验失败,共 {len(errors)} 个错误:")
        for e in errors:
            print(f"  {e}")
        print("\n修复: 参考 prompt.md 第 6/7 步,补全缺失字段后重跑")
        return 1
    else:
        print(f"✅ {date_str} schema 校验通过")
        print(f"  - data.json: {len(d['products'])} 个 product,均含 image + images[]")
        print(f"  - vs-data.json: hotProducts {len(vs['hotProducts'])} 项,均含 image")
        print(f"  - vs-data.json: dataSource + updateTime 已就位")
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: validate_schema.py <date>")
        sys.exit(2)
    sys.exit(validate(sys.argv[1]))
