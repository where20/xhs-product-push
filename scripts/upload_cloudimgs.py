#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""上传今日长图 + 5 张裁剪图到 cloudimgs.iepose.cn (/api/upload-file 协议)

用法: python3 scripts/upload_cloudimgs.py <date>
      python3 scripts/upload_cloudimgs.py 2026-09-01
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

HOST = "https://cloudimgs.iepose.cn"
UPLOAD_PATH = "/api/upload-file"


def upload_one(local_path: str, custom_name: str = None) -> dict:
    """POST multipart 上传，返回 {success, filename, url, size, error}"""
    boundary = "----xhs" + datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = custom_name or os.path.basename(local_path)
    with open(local_path, "rb") as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_bytes + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        HOST + UPLOAD_PATH,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
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
    out_dir = Path(f"/Users/xiaoan/WorkBuddy/xhs-product-push/output/{date}")
    if not out_dir.is_dir():
        print(f"❌ output dir not found: {out_dir}")
        sys.exit(2)

    files_to_upload = [
        ("product_card_full.jpg", f"{date}_product_card_full.jpg"),
        ("product_slice_1.jpg",   f"{date}_product_slice_1.jpg"),
        ("product_slice_2.jpg",   f"{date}_product_slice_2.jpg"),
        ("product_slice_3.jpg",   f"{date}_product_slice_3.jpg"),
        ("product_slice_4.jpg",   f"{date}_product_slice_4.jpg"),
        ("product_slice_5.jpg",   f"{date}_product_slice_5.jpg"),
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
    upload_log = {
        "date": date,
        "host": HOST,
        "endpoint": UPLOAD_PATH,
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
