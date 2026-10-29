#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jd_fetch.py — 京东榜单页解析器(2026-10-29 新增, 固化当天的数据源探测结论)

用法:
    python3 scripts/jd_fetch.py <榜单页URL> [<榜单页URL> ...]
    python3 scripts/jd_fetch.py --imgs <榜单页URL> [...]   # 顺便下载主图到临时目录

背景(为什么需要这个脚本)
----------------------
2026-10-29 实测: JD 的**搜索/详情/价格接口全部被反爬或 DNS 劫持**, 但
**榜单页 (www.jd.com/phb/*.html) 服务端直出** 商品名 / SKU / 评论数 / 商品主图。
这是当天唯一稳定能拿到"真实商品名 + 真实评论数 + 真实主图"的路径。

各端点实测结论(别再重复踩):

| 端点                              | 结果 | 说明 |
|-----------------------------------|------|------|
| www.jd.com/phb/*.html 榜单页      | ✅   | 服务端直出 name/sku/评论数/主图, **本脚本的目标** |
| p.3.cn/prices/mgets (价格 API)    | ❌   | DNS 被劫持到 10.x/172.x 内网假 IP(DoH 查 google/cloudflare/alidns 全是假 IP) |
| search.jd.com / so.m.jd.com      | ❌   | 302 → 「京东验证」页 |
| item.jd.com/{sku}.html            | ❌   | 200 但返回通用首页, 无商品数据 |
| api.m.jd.com client.action        | ❌   | {"code":"1","echo":"no access"} |
| list.jd.com/list.html?cat=        | ❌   | Vite SPA, 数据全在 JS 里 |
| search.suning.com / www.vip.com   | ⚠️   | 200 但价格同样 JS 渲染 |

⚠️ **榜单页的坑(10-29 踩到)**: 同一 URL 的内容会**按关键词轮换**。
   例如 `木积盒子排行榜` 可能返回的是收纳盒而非积木, `水笔竹子排行榜` 返回的是
   水彩笔而非中性笔 —— **标题和实际内容对不上**。
   → 所以本脚本**逐条打印真实商品名**, 不要凭 URL 或网页标题想当然, 写内容文件前
     必须逐条 read 实际商品名。

⚠️ **榜单页没有价格**: `<span class="price-rmb" data-skuId="...">` 值恒为空(JS 渲染)。
   → 价格必须走 smzdm 商品页(价格明文在 HTML 里, 见 verify_links.py 的说明)。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# 榜单页每个商品的 HTML 块以 <div class="product-img"> 开头
BLOCK_SPLIT = '<div class="product-img">'


def curl(url, timeout=25):
    """抓取 URL。⚠️ 强制 --noproxy '*': 本机 HTTP_PROXY 指向的端口时活时死,
    且 p.3.cn 等域名被 DNS 劫持到内网假 IP —— 走代理反而更糟。"""
    r = subprocess.run(
        ["curl", "--noproxy", "*", "-m", str(timeout), "-s", "-L", "-A", UA,
         "-H", "Referer: https://www.jd.com/", url],
        capture_output=True)
    return r.stdout.decode("utf-8", "ignore")


def parse_phb(url):
    """解析榜单页 → [{name, sku, comments, image, url}]"""
    html = curl(url)
    if not html:
        return [], ""
    out = []
    for block in html.split(BLOCK_SPLIT)[1:]:
        m = re.search(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"', block)
        if not m:
            m = re.search(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', block)
        if not m:
            continue
        image, name = m.group(1), m.group(2).strip()
        if image.startswith("//"):
            image = "https:" + image
        sku_m = re.search(r'item\.jd\.com/(\d+)\.html', block)
        if not sku_m:
            continue
        sku = sku_m.group(1)
        # ⚠️ 榜单页原文是 `<span class="evaluate-num">已有5000000人评论</span>`,
        #   数字是**原始条数**(不是"5万"), 别自作聪明加单位。
        cm = re.search(r'已有\s*([\d.]+)\s*(万)?人评论', block)
        if cm:
            comments = f"{cm.group(1)}{cm.group(2) or ''}人评论"
        else:
            cm2 = re.search(r'([\d.]+万?)\s*条评价', block)
            comments = f"{cm2.group(1)}条评价" if cm2 else ""
        out.append({
            "name": name,
            "sku": sku,
            "comments": comments,
            "image": image,
            "url": f"https://item.jd.com/{sku}.html",
        })
    return out, html


def page_title(html):
    m = re.search(r'<title>([^<]*)</title>', html)
    return m.group(1) if m else "?"


def download_images(products, outdir):
    """下载商品主图(s450x450 版本)用于**肉眼验色**。
    2026-10-26 踩坑: 卡片写黑、图是白 = 图文不符 = 假带货。颜色零猜测。"""
    os.makedirs(outdir, exist_ok=True)
    saved = []
    for p in products:
        if not p["image"]:
            continue
        big = re.sub(r'/n7/s80x80_jfs/', '/n1/s450x450_jfs/', p["image"])
        path = os.path.join(outdir, f"{p['sku']}.jpg")
        subprocess.run(["curl", "--noproxy", "*", "-m", "20", "-s", "-o", path, big],
                       capture_output=True)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        if size < 3000:
            if os.path.exists(path):
                os.remove(path)
            continue
        p["image_local"] = path
        saved.append(path)
    return saved


def main():
    ap = argparse.ArgumentParser(
        description="京东榜单页解析器(拿真实商品名/SKU/评论数/主图)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    ap.add_argument("urls", nargs="+", help="京东榜单页 URL (www.jd.com/phb/*.html)")
    ap.add_argument("--imgs", action="store_true",
                    help="同时下载商品主图(用于肉眼验色)")
    ap.add_argument("--outdir", default=None,
                    help="主图下载目录(默认系统临时目录)")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非文本")
    args = ap.parse_args()

    outdir = args.outdir or os.path.join(tempfile.gettempdir(), "xhs_jd_imgs")
    all_data = {}

    for url in args.urls:
        products, html = parse_phb(url)
        title = page_title(html)
        print(f"\n{'=' * 72}")
        print(f"榜单页: {url}")
        print(f"页面标题: {title}")
        if not products:
            print("  ⚠️ 解析到 0 个商品 —— 可能是反爬页 / URL 错 / 页面结构变了")
            print(f"     页面片段: {html[:200]!r}")
            all_data[url] = {"title": title, "products": []}
            continue
        print(f"解析到 {len(products)} 个商品:")
        for i, p in enumerate(products, 1):
            print(f"  {i}. {p['name'][:74]}")
            print(f"     sku={p['sku']}  评论数={p['comments']}")
            print(f"     主图={p['image'][:96]}")
        if args.imgs:
            saved = download_images(products, outdir)
            print(f"  📥 主图已下载 {len(saved)} 张 → {outdir}")
            print(f"     ⚠️ 请逐张打开确认颜色与实物一致(10-26 踩坑: 卡片写黑、图是白)")
        all_data[url] = {"title": title, "products": products}

    if args.json:
        print(json.dumps(all_data, ensure_ascii=False, indent=1))
    else:
        print(f"\n{'=' * 72}")
        print("💡 下一步:")
        print("   1. 逐条 read 真实商品名(榜单页内容会按关键词轮换, 别信标题)")
        print("   2. 主图肉眼验色 → 决定 products.json 的 color 字段")
        print("   3. 价格走 smzdm 商品页(榜单页价格是 JS 渲染的, 抓不到)")
        print("   4. links URL 用 scripts/verify_links.py 核验 200/202")
    return 0


if __name__ == "__main__":
    sys.exit(main())
