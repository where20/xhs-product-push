#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_links.py — 核验内容文件里所有链接真的可达(2026-10-29 新增)

用法:
    python3 scripts/verify_links.py <date>
    python3 scripts/verify_links.py 2026-10-29

检查范围(当天内容文件):
    output/{date}/products.json  → 每个 product 的 links.primary + links.extra[]
    output/{date}/vs.json        → sources[]

为什么需要这个脚本
------------------
硬规则 #1: "价格 / 销量 / 评论数 / 商品链接必须来自真实搜索结果, 严禁编造。
**编造的链接比没有链接更糟**(假带货链路)。每个 URL 都要 curl 核验 200/202。"

但"每个都要核验"这句话靠人肉执行必然漏 —— 2026-10-29 是靠一段临时 bash 循环做的,
下一次就可能忘记。本脚本把它变成**固定闸门**: 链接不可达 = 非零退出码 = 流程停下。

已知不可用(不要写进 links):
    ⚠️ www.sohu.com/a/...      文章页 curl 恒 403(直连/代理/UA 全试过)
       → 改用可 200 的镜像域: db.m.auto.sohu.com/model_.../a/...、gov.sohu.com/a/...
    ⚠️ search.jd.com / item.jd.com  京东反爬, 直链拿不到
       → 用 www.jd.com/phb/*.html 排行榜页兜底(200 且含商品名+真实评论数)
    ⚠️ mitem.jd.hk / 24h.pchome.com.tw  实测 404 / 连接失败
    💡 smzdm 商品页(m.smzdm.com/p/...、www.smzdm.com/p/...、smzdm.com/sou/...)
       价格明文在 HTML 里, 可 200, 是价格来源的首选外链。
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_xhs import out_dir  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 已知恒不可达的域名 → 提前拦下, 不浪费 15s 超时
KNOWN_BAD_HOSTS = {
    "www.sohu.com": "文章页恒 403, 改用 db.m.auto.sohu.com 或 gov.sohu.com 镜像域",
    "search.jd.com": "京东反爬, 直链拿不到",
    "item.jd.com": "京东反爬, 直链拿不到, 用 www.jd.com/phb/*.html 榜单页兜底",
    "mitem.jd.hk": "实测 404",
    "24h.pchome.com.tw": "实测连接失败",
}


def check(url, timeout=15):
    """返回 (ok, code, note)。⚠️ --noproxy '*': 本机代理端口时活时死, 且
    p.3.cn 等域名被 DNS 劫持到内网假 IP, 走代理反而拿不到。"""
    for host, note in KNOWN_BAD_HOSTS.items():
        if url.startswith(f"https://{host}") or url.startswith(f"http://{host}"):
            return False, "known-bad", note
    if not url.startswith(("http://", "https://")):
        return False, "bad-scheme", "必须是 http(s) 绝对地址"
    try:
        r = subprocess.run(
            ["curl", "--noproxy", "*", "-m", str(timeout), "-s", "-o", "/dev/null",
             "-w", "%{http_code}", "-L", "-A", UA, url],
            capture_output=True, text=True, timeout=timeout + 5)
        code = (r.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return False, "timeout", f"超过 {timeout}s 未响应"
    except Exception as e:
        return False, "error", str(e)
    if code in ("200", "202"):
        return True, code, ""
    return False, code or "000", "非 200/202"


def collect(date):
    """收集当天所有待核验 URL → [(来源描述, url)]"""
    od = out_dir(date)
    items = []

    ppath = os.path.join(od, "products.json")
    if os.path.exists(ppath):
        products = json.load(open(ppath, encoding="utf-8"))
        if isinstance(products, dict):
            products = products.get("products") or []
        for p in products:
            pid = p.get("id", "?")
            links = p.get("links") or {}
            primary = links.get("primary")
            if primary:
                items.append((f"product[{pid}].links.primary", primary))
            for i, u in enumerate(links.get("extra") or [], 1):
                items.append((f"product[{pid}].links.extra[{i}]", u))
            if not links:
                items.append((f"product[{pid}].links", "⚠️ 无 links —— 落地页会回退到京东搜索链接"))
    else:
        print(f"⚠️  找不到 {ppath}", file=sys.stderr)

    vpath = os.path.join(od, "vs.json")
    if os.path.exists(vpath):
        vs = json.load(open(vpath, encoding="utf-8"))
        for i, u in enumerate(vs.get("sources") or [], 1):
            items.append((f"vs.sources[{i}]", u))
    else:
        print(f"⚠️  找不到 {vpath}", file=sys.stderr)

    return items


def main():
    if len(sys.argv) < 2:
        print("用法: verify_links.py <date>")
        return 2
    date = sys.argv[1]
    items = collect(date)

    if not items:
        print(f"❌ {date} 没有可核验的链接(products.json / vs.json 缺失或为空)")
        return 1

    print(f"🔗 {date} 链接核验 (共 {len(items)} 条)\n")
    bad = []
    for label, url in items:
        if not url.startswith("http"):
            print(f"  ❌ {label}: {url}")
            bad.append((label, url, "bad-scheme"))
            continue
        ok, code, note = check(url)
        mark = "✅" if ok else "❌"
        extra = f"  ← {note}" if note else ""
        print(f"  {mark} {label}: {code}  {url[:78]}{extra}")
        if not ok:
            bad.append((label, url, note))

    print()
    if bad:
        print(f"❌ {len(bad)}/{len(items)} 条链接不可达:")
        for label, url, note in bad:
            print(f"   - {label}: {url}  ({note})")
        print("\n修复: 换成可 200/202 的真实商品页(京东榜单页 / smzdm 商品页),")
        print("     **严禁编造 URL** —— 编造的链接 = 假带货链路, 比没有链接更糟。")
        return 1
    print(f"✅ 全部 {len(items)} 条链接可达 (200/202)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
