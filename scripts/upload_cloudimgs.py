#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上传今日长图 + 5 张裁剪图到 cloudimgs.iepose.cn (/api/upload-file 协议)

用法: python3 scripts/upload_cloudimgs.py <date>
      python3 scripts/upload_cloudimgs.py 2026-09-29

实现: 用 curl 命令调用 (替代 Python urllib, 解决 cloudimgs Cloudflare connection refused 问题)
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import out_dir as xhs_out_dir  # noqa: E402

HOST = "https://cloudimgs.iepose.cn"
UPLOAD_PATH = "/api/upload-file"


def upload_one(local_path: str, custom_name: str = None) -> dict:
    """通过 curl 上传文件，返回 {success, filename, url, size, error}"""
    filename = custom_name or os.path.basename(local_path)
    # 用 curl 调用，绕过 Python urllib Cloudflare connection refused 问题
    cmd = [
        "curl", "--noproxy", "*", "-sS", "-m", "60",
        "-F", f"file=@{local_path};filename={filename}",
        HOST + UPLOAD_PATH
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=65)
        if result.returncode != 0:
            return {"success": False, "error": f"curl exit {result.returncode}: {result.stderr.strip()}"}
        data = json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "curl timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}

    if not data.get("success"):
        return {"success": False, "error": data.get("message", "unknown")}

    d = data["data"]
    rel = d["url"]  # 形如 /api/files/xxx.jpg
    return {
        "success": True,
        "filename": d["filename"],
        "relPath": d.get("relPath", d["filename"]),
        "size": d["size"],
        "url": HOST + rel.replace("/api/files/", "/api/images/"),
    }


def main():
    if len(sys.argv) < 2:
        print("usage: upload_cloudimgs.py <date>")
        sys.exit(1)
    date = sys.argv[1]
    out_dir = Path(xhs_out_dir(date))
    if not out_dir.is_dir():
        print(f"❌ output dir not found: {out_dir}")
        sys.exit(2)

    files_to_upload = [
        # 1 全图 + 5 切片(给飞书卡片用)
        ("product_card_full.jpg", f"{date}_product_card_full.jpg"),
        ("product_slice_1.jpg",   f"{date}_product_slice_1.jpg"),
        ("product_slice_2.jpg",   f"{date}_product_slice_2.jpg"),
        ("product_slice_3.jpg",   f"{date}_product_slice_3.jpg"),
        ("product_slice_4.jpg",   f"{date}_product_slice_4.jpg"),
        ("product_slice_5.jpg",   f"{date}_product_slice_5.jpg"),
        # 5 张 1:1 纯商品图(landing page 渲染用,9/2 bug 修复必须上传)
        ("images/product_1.jpg",  f"{date}_product_1.jpg"),
        ("images/product_2.jpg",  f"{date}_product_2.jpg"),
        ("images/product_3.jpg",  f"{date}_product_3.jpg"),
        ("images/product_4.jpg",  f"{date}_product_4.jpg"),
        ("images/product_5.jpg",  f"{date}_product_5.jpg"),
    ]

    results = []
    for local_name, custom_name in files_to_upload:
        path = out_dir / local_name
        if not path.exists():
            print(f"⚠️  missing: {path}")
            results.append({"name": local_name, "success": False, "error": "local file missing"})
            continue
        print(f"⬆️  uploading {local_name} ({path.stat().st_size//1024}KB) ...")
        r = upload_one(str(path), custom_name=custom_name)
        r["name"] = local_name
        results.append(r)
        if r["success"]:
            print(f"   ✅ {r['url']}")
        else:
            print(f"   ❌ {r['error']}")

    # 写入 uploaded_urls.json
    # ⚠️ images / slices 这两个映射是 db_save.py 的**唯一**图片来源。
    #    图床对同名文件再上传会重命名成 {name}_{ts}_{n}, 确定性模板 URL 拿不到新图,
    #    所以必须把上传接口返回的**真实 URL** 落到这里(pid → url)。
    #    (2026-10-22 实测: 只写 uploaded 列表时 db_save 读不到 images,
    #     落地页一直显示当天第一次上传的旧卡片。)
    images_map, slices_map = {}, {}
    card_full = None
    for r in results:
        if not r.get("success"):
            continue
        name = r.get("name", "")
        if name.startswith("images/product_"):
            try:
                pid = int(name.split("product_")[1].split(".")[0])
                images_map[str(pid)] = r["url"]
            except ValueError:
                pass
        elif name.startswith("product_slice_"):
            try:
                pid = int(name.replace("product_slice_", "").split(".")[0])
                slices_map[str(pid)] = r["url"]
            except ValueError:
                pass
        elif name == "product_card_full.jpg":
            card_full = r["url"]

    upload_log = {
        "date": date,
        "host": HOST,
        "endpoint": UPLOAD_PATH,
        "images": images_map,      # {product_id: 1:1 纯图真实 URL}
        "slices": slices_map,      # {product_id: 切片真实 URL}
        "card_full": card_full,    # 长图真实 URL
        "uploaded": [r for r in results if r.get("success")],
    }
    log_path = out_dir / "uploaded_urls.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(upload_log, f, ensure_ascii=False, indent=2)
    print(f"\n📝 写入 {log_path}")

    n_ok = sum(1 for r in results if r.get("success"))
    print(f"✅ {n_ok}/{len(results)} 上传成功")
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())