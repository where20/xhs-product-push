#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_live.py — 端到端线上验证闸门

为什么需要它
------------
2026-10-20 那趟, push 之后我手工 curl 线上, 拿到的是**旧 DATA_VERSION + 新 v/ 路径 404**,
看起来像"版本化路径没生效"。实测 GitHub Pages 推送后有约 40s 构建传播延迟,
20s 时仍旧、40s 后同时正确。把这段轮询逻辑固化, 就不用每次人肉盯。

而且更重要的是: 之前**没有任何一步**会确认"线上真的换成今天的数据了"。
push 成功 ≠ 用户看到的页面是新的。本脚本把这件事变成一个可自动断言的闸门。

检查项
------
  1. 本地 index.html 的 DATA_VERSION 与 git HEAD 是否一致
  2. 线上 index.html 的 DATA_VERSION 是否已更新(轮询等待 Pages 传播)
  3. 线上 /v/{VERSION}/data.json 与本地 output/{date}/data.json 内容一致
  4. 线上 /v/{VERSION}/vs-data.json 的 hotProducts 数量、sources 数量
  5. 5 个商品图与 5 张切片在图床 CDN 上是否全部 HTTP 200
  6. 线上 data.json 每个 product 的 image/images 都是 https CDN URL

用法:
    python3 scripts/verify_live.py [YYYY-MM-DD] [--timeout 180] [--skip-cdn]
退出码: 0 = 全部通过; 1 = 有检查失败
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import TASK_DIR, out_dir, read_json, resolve_date  # noqa: E402

DOMAIN = "xhs.220616.xyz"   # CNAME
TIMEOUT = 25

OK = "\033[32m✅\033[0m"
BAD = "\033[31m❌\033[0m"
WARN = "\033[33m⚠️\033[0m"

_results = []


def check(name, passed, detail=""):
    _results.append((name, passed, detail))
    mark = OK if passed else BAD
    print(f"  {mark} {name}" + (f" — {detail}" if detail else ""))
    return passed


def http_get(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "xhs-verify/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def http_code(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "xhs-verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def local_data_version():
    html = open(os.path.join(TASK_DIR, "index.html"), encoding="utf-8").read()
    import re
    m = re.search(r"const DATA_VERSION = '([^']*)'", html)
    return m.group(1) if m else None


def git_head():
    try:
        return subprocess.check_output(
            ["git", "-C", TASK_DIR, "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return None


def wait_for_live(version, timeout):
    """轮询等待 GitHub Pages 把新版本推上线。"""
    base = f"https://{DOMAIN}"
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        try:
            _, html = http_get(f"{base}/?cb={int(time.time()*1000)}")
            import re
            m = re.search(r"const DATA_VERSION = '([^']*)'", html)
            live = m.group(1) if m else None
            code = http_code(f"{base}/v/{version}/data.json")
            last = f"live={live} v/{version}={code}"
            if live == version and code == 200:
                return True, live, code
        except Exception as e:
            last = f"err={e}"
        time.sleep(10)
    return False, last, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", default=None)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--skip-cdn", action="store_true")
    args = ap.parse_args()

    date = resolve_date([args.date] if args.date else [])
    od = out_dir(date)
    print(f"🔍 线上验证 · {date} · 域名 {DOMAIN}\n")

    # ---------- 1. 本地状态 ----------
    print("[1/4] 本地状态")
    version = local_data_version()
    check("index.html 有 DATA_VERSION", bool(version), version or "未找到")
    head = git_head()
    check("git HEAD 存在", bool(head), (head or "")[:12])
    if version is None:
        print("\n❌ 无法继续: index.html 没有 DATA_VERSION")
        return 1

    # ---------- 2. 等待线上生效 ----------
    print(f"\n[2/4] 等待线上生效 (超时 {args.timeout}s, GitHub Pages 传播约需 40s)")
    ok, live, code = wait_for_live(version, args.timeout)
    check("线上 DATA_VERSION 已更新", live == version, f"live={live} 期望={version}")
    check(f"线上 /v/{version}/data.json 可达", code == 200, f"HTTP {code}")

    # ---------- 3. 内容一致性 ----------
    print("\n[3/4] 内容一致性")
    base = f"https://{DOMAIN}"
    lpath = os.path.join(od, "data.json")
    if not os.path.exists(lpath):
        check("本地 data.json 存在", False, lpath)
        return 1
    local = read_json(lpath)
    try:
        _, remote_txt = http_get(f"{base}/v/{version}/data.json?cb={int(time.time()*1000)}")
        remote = json.loads(remote_txt)
    except Exception as e:
        check("线上 data.json 可解析", False, str(e))
        return 1

    check(
        "线上 date 正确",
        remote.get("date") == date,
        f"线上={remote.get('date')} 本地={date}",
    )
    check(
        "线上商品数 == 本地商品数",
        len(remote.get("products", [])) == len(local.get("products", [])),
        f"{len(remote.get('products', []))} vs {len(local.get('products', []))}",
    )
    lp = {p["id"]: p for p in local.get("products", [])}
    same = True
    for rp in remote.get("products", []):
        cur = lp.get(rp["id"])
        if not cur:
            same = False
            break
        if rp.get("name") != cur.get("name") or rp.get("price") != cur.get("price"):
            same = False
            break
    check("线上 5 商品 name/price 与本地完全一致", same)

    all_cdn = all(
        p.get("image", "").startswith("https://")
        and len(p.get("images", [])) >= 1
        for p in remote.get("products", [])
    )
    check("线上每个 product 的 image/images 均为 CDN URL", all_cdn)

    # ---------- 4. vs-data + CDN ----------
    print("\n[4/4] vs-data 与 CDN 图片")
    try:
        _, vs_txt = http_get(f"{base}/v/{version}/vs-data.json?cb={int(time.time()*1000)}")
        vs = json.loads(vs_txt)
        check("线上 vs-data hotProducts == 5", len(vs.get("hotProducts", [])) == 5,
              str(len(vs.get("hotProducts", []))))
        check("线上 vs-data sources >= 10", len(vs.get("sources", [])) >= 10,
              f"{len(vs.get('sources', []))} 条")
        sizes = [len(g.get("items", [])) for g in vs.get("competitors", [])]
        check("每组竞品 >= 4 项", all(s >= 4 for s in sizes), str(sizes))
    except Exception as e:
        check("线上 vs-data.json 可解析", False, str(e))

    if not args.skip_cdn:
        urls = []
        for p in remote.get("products", []):
            urls.append(p.get("image"))
        for i in range(1, 6):
            urls.append(f"https://cloudimgs.iepose.cn/api/images/{date}_product_slice_{i}.jpg")
        urls.append(f"https://cloudimgs.iepose.cn/api/images/{date}_product_card_full.jpg")
        bad = [u for u in urls if u and http_code(u) != 200]
        check(f"CDN 图片全部可达 ({len(urls)} 张)", not bad,
              (f"失败: {bad[:3]}" if bad else ""))

    # ---------- 汇总 ----------
    passed = sum(1 for _, p, _ in _results if p)
    total = len(_results)
    print(f"\n{'='*60}")
    print(f"验证结果: {passed}/{total} 项通过")
    if passed == total:
        print(f"{OK} 线上已完整切换到 {date} 的数据")
        return 0
    print(f"{BAD} 有 {total - passed} 项未通过")
    return 1


if __name__ == "__main__":
    sys.exit(main())
