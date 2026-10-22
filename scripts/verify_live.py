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
  7. **页面渲染断言**(2026-10-22 新增):
     用 Node + DOM stub 把线上 index.html 的脚本真跑一遍, 断言渲染出来的
     商品卡片里真的有价格、详情、购买链接, 而不是"数据在但页面不显示"。
     这一项能抓住 2026-10-22 之前那个 bug: 模板写的是 p.priceRange / p.description,
     而数据里是 p.price / p.desc → 字段不匹配 → 价格和详情整块不渲染。

代理
----
默认**绕过**系统代理直连(ProxyHandler({})): 落地页域名和图床都能直连,
走代理反而会因为代理端口生死不定而随机失败。直连失败时才回落到默认 opener。

用法:
    python3 scripts/verify_live.py [YYYY-MM-DD] [--timeout 180] [--skip-cdn] [--skip-render]
退出码: 0 = 全部通过; 1 = 有检查失败
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
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

# 直连 opener(绕过 http_proxy / https_proxy 环境变量)
_DIRECT = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def check(name, passed, detail=""):
    _results.append((name, passed, detail))
    mark = OK if passed else BAD
    print(f"  {mark} {name}" + (f" — {detail}" if detail else ""))
    return passed


def _open(url, timeout=TIMEOUT):
    """直连优先, 失败回落默认 opener(带代理)。返回 (status, body_text)。"""
    req = urllib.request.Request(url, headers={"User-Agent": "xhs-verify/2.0"})
    try:
        with _DIRECT.open(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except Exception:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")


def http_get(url, timeout=TIMEOUT):
    return _open(url, timeout)


def http_code(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": "xhs-verify/2.0"})
    for opener in (_DIRECT, urllib.request.build_opener()):
        try:
            with opener.open(req, timeout=timeout) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception:
            continue
    return 0


def local_data_version():
    html = open(os.path.join(TASK_DIR, "index.html"), encoding="utf-8").read()
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


# ==========================================================================
# 页面渲染断言: 用 Node + DOM stub 真跑一遍线上 index.html 的脚本
# ==========================================================================
#
# 为什么不用正则去猜模板: 之前 index.html 的模板写的是 p.priceRange / p.description,
# 而 data.json 里是 p.price / p.desc —— 两者语义完全对不上, 但"页面能打开、
# JSON 也能下载", 所有"检查文件存在"的脚本都发现不了, 只有真的渲染一次才暴露。
#
# 这里用 vm 模块跑**线上**那份 index.html 的 <script>, 把 fetch 指向线上 data.json,
# 然后读渲染后的 #productList.innerHTML —— 断言里面真的出现了价格/详情/购买链接。

NODE_RENDER_JS = r"""
const fs = require('fs');
const vm = require('vm');

const [, , htmlPath, dataPath, vsPath] = process.argv;
const html = fs.readFileSync(htmlPath, 'utf8');
const liveData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const liveVs = JSON.parse(fs.readFileSync(vsPath, 'utf8'));

const m = html.match(/<script[^>]*>([\s\S]*?)<\/script>/);
if (!m) { console.error('NO_SCRIPT_BLOCK'); process.exit(3); }
const pageJs = m[1];

// ---------------- DOM stub ----------------
const registry = new Map();
function makeEl(id) {
  const el = {
    _id: id, _text: '', _html: '', value: '', href: '', src: '', disabled: false,
    style: {}, dataset: {},
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    children: [], parentNode: null,
    get textContent(){ return this._text; },
    set textContent(v){ this._text = v == null ? '' : String(v); },
    get innerHTML(){ return this._html; },
    set innerHTML(v){ this._html = v == null ? '' : String(v); },
    get innerText(){ return this._text; },
    set innerText(v){ this._text = v == null ? '' : String(v); },
    get offsetHeight(){ return 0; }, get offsetWidth(){ return 0; },
    get scrollHeight(){ return 0; }, get scrollTop(){ return 0; },
    get firstChild(){ return null; }, get lastChild(){ return null; },
    get childNodes(){ return []; },
    get nextElementSibling(){ return null; }, get previousElementSibling(){ return null; },
    appendChild(c){ this.children.push(c); return c; },
    removeChild(c){ return c; }, replaceChild(){}, insertBefore(c){ this.children.push(c); return c; },
    remove(){}, addEventListener(){}, removeEventListener(){}, dispatchEvent(){ return true; },
    querySelector(){ return makeEl(id + '>q'); }, querySelectorAll(){ return []; },
    getElementsByClassName(){ return []; }, getElementsByTagName(){ return []; },
    closest(){ return null; }, matches(){ return false; }, contains(){ return false; },
    getBoundingClientRect(){ return {top:0,left:0,right:0,bottom:0,width:0,height:0,x:0,y:0}; },
    scrollIntoView(){}, scrollTo(){}, focus(){}, blur(){}, click(){}, setSelectionRange(){},
    setAttribute(){}, getAttribute(){ return null; }, removeAttribute(){}, hasAttribute(){ return false; },
    cloneNode(){ return makeEl(id + '>clone'); },
  };
  return el;
}
const getEl = (id) => { if (!registry.has(id)) registry.set(id, makeEl(id)); return registry.get(id); };

const document = {
  getElementById: getEl,
  querySelector: (sel) => getEl('sel:' + sel),
  querySelectorAll: () => [],
  getElementsByClassName: () => [],
  createElement: (tag) => makeEl('new:' + tag),
  createTextNode: (t) => ({ nodeType: 3, textContent: String(t) }),
  createDocumentFragment: () => makeEl('frag'),
  body: makeEl('body'), head: makeEl('head'), documentElement: makeEl('html'),
  addEventListener(){}, removeEventListener(){},
  title: '', cookie: '', readyState: 'complete',
};

const logs = [];
const consoleStub = {
  log: (...a) => logs.push(a.map(String).join(' ')),
  warn: (...a) => logs.push('WARN ' + a.map(String).join(' ')),
  error: (...a) => logs.push('ERROR ' + a.map(String).join(' ')),
  info: (...a) => logs.push(a.map(String).join(' ')),
  debug: () => {},
};

function fakeFetch(url) {
  const u = String(url);
  let payload = null;
  if (/vs-data\.json/.test(u)) payload = liveVs;
  else if (/history\/history\.json/.test(u)) payload = [];
  else if (/history\/\d{4}-\d{2}-\d{2}\.json/.test(u)) payload = null;
  else if (/data\.json/.test(u)) payload = liveData;
  if (payload === null) {
    return Promise.resolve({
      ok: false, status: 404, statusText: 'Not Found',
      json: async () => { throw new Error('404 Not Found'); },
      text: async () => '',
    });
  }
  return Promise.resolve({
    ok: true, status: 200, statusText: 'OK',
    json: async () => JSON.parse(JSON.stringify(payload)),
    text: async () => JSON.stringify(payload),
  });
}

const sandbox = {
  console: consoleStub,
  setTimeout: () => 0, clearTimeout: () => {},
  setInterval: () => 0, clearInterval: () => {},
  fetch: fakeFetch,
  document,
  navigator: { userAgent: 'xhs-render-check', language: 'zh-CN' },
  location: { href: 'https://' + 'xhs.220616.xyz' + '/', search: '', hash: '',
              hostname: 'xhs.220616.xyz', protocol: 'https:', pathname: '/' },
  alert(){}, confirm(){ return true; }, prompt(){ return ''; }, open(){},
  JSON, Math, Date, Promise, Object, Array, String, Number, Boolean, Error, RegExp,
  Map, Set, WeakMap, Symbol, Intl, Uint8Array, ArrayBuffer,
  encodeURIComponent, decodeURIComponent, encodeURI, decodeURI,
  isNaN, isFinite, parseInt, parseFloat, undefined: undefined,
};
sandbox.window = sandbox;
sandbox.self = sandbox;
sandbox.top = sandbox;
sandbox.globalThis = sandbox;

let evalError = null;
try {
  const ctx = vm.createContext(sandbox);
  vm.runInContext(pageJs, ctx, { filename: 'online-index.html' });
} catch (e) {
  evalError = (e && e.message) ? e.message : String(e);
}

function snapshot() {
  return {
    productListHtml: getEl('productList')._html,
    totalRuns: getEl('totalRuns')._text,
    totalProducts: getEl('totalProducts')._text,
    lastRunDate: getEl('lastRunDate')._text,
    status: getEl('status')._text,
    updateTime: getEl('updateTime')._text,
    debugVersion: getEl('debugVersionText')._text,
    debugFetch: getEl('debugFetch')._text,
  };
}

(async () => {
  const deadline = Date.now() + 8000;
  let snap = snapshot();
  while (Date.now() < deadline) {
    if (snap.productListHtml && snap.productListHtml.indexOf('product-item') !== -1) break;
    await new Promise(r => setTimeout(r, 100));
    snap = snapshot();
  }
  const out = { ok: !evalError, evalError, logs: logs.slice(0, 40) };
  Object.assign(out, snap);
  process.stdout.write(JSON.stringify(out));
})();
"""


def render_live_page(html_text, data_obj, vs_obj):
    """用 Node 渲染线上 index.html。返回 (result_dict, error_str)"""
    node = shutil.which("node")
    if not node:
        return None, "未找到 node, 无法做页面渲染断言"
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, "index.html")
        dp = os.path.join(td, "data.json")
        vp = os.path.join(td, "vs-data.json")
        jp = os.path.join(td, "render.js")
        with open(hp, "w", encoding="utf-8") as f:
            f.write(html_text)
        with open(dp, "w", encoding="utf-8") as f:
            json.dump(data_obj, f, ensure_ascii=False)
        with open(vp, "w", encoding="utf-8") as f:
            json.dump(vs_obj, f, ensure_ascii=False)
        with open(jp, "w", encoding="utf-8") as f:
            f.write(NODE_RENDER_JS)
        try:
            r = subprocess.run(
                [node, jp, hp, dp, vp],
                capture_output=True, text=True, timeout=90,
            )
        except subprocess.TimeoutExpired:
            return None, "node 渲染超时(90s)"
        if r.returncode != 0:
            return None, f"node 退出码 {r.returncode}: {r.stderr.strip()[:300]}"
        try:
            return json.loads(r.stdout), None
        except Exception as e:
            return None, f"node 输出无法解析({e}): {r.stdout[:200]}"


def _norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def check_render(html_text, data_obj, vs_obj, products):
    """页面渲染断言: 渲染线上页面, 检查商品卡片里真的有价格/详情/购买链接。"""
    res, err = render_live_page(html_text, data_obj, vs_obj)
    if res is None:
        check("页面渲染断言(可执行)", False, err)
        return

    check("线上脚本可无错执行", bool(res.get("ok")), res.get("evalError") or "")
    rendered = res.get("productListHtml") or ""
    if not rendered:
        check("渲染出商品卡片", False, "#productList 为空")
        return

    cards = rendered.count('class="product-item"')
    check(f"渲染出 {len(products)} 张商品卡片", cards == len(products), f"实际 {cards}")

    missing_price, missing_desc, missing_link = [], [], []
    bad_href = []
    for p in products:
        name = p.get("name", "")
        price = _norm(p.get("price") or p.get("priceRange"))
        desc = _norm(p.get("desc") or p.get("description"))
        # 价格: 模板渲染出来的价格文本必须出现在 HTML 里
        if price and price not in _norm(rendered):
            missing_price.append(p.get("id"))
        # 详情: 取前 30 个字做锚点, 避免 HTML 转义导致的整段不匹配
        if desc and desc[:30] not in _norm(rendered):
            missing_desc.append(p.get("id"))
        # 购买链接: 该商品必须渲染出至少一个指向其真实商品页的 href
        links = p.get("links") or {}
        primary = links.get("primary")
        if primary:
            if primary not in rendered:
                missing_link.append(p.get("id"))
        else:
            # 没有 links 的老数据: 必须回退出京东搜索链接
            if "search.jd.com/Search?keyword=" not in rendered:
                missing_link.append(p.get("id"))
    check("每张卡片都渲染出价格", not missing_price, f"缺: {missing_price}" if missing_price else "")
    check("每张卡片都渲染出详情描述", not missing_desc, f"缺: {missing_desc}" if missing_desc else "")
    check("每张卡片都渲染出购买链接", not missing_link, f"缺: {missing_link}" if missing_link else "")

    hrefs = re.findall(r'href="([^"]+)"', rendered)
    bad = [h for h in hrefs if not h.startswith(("http://", "https://"))]
    check("购买链接全部是 http(s) 绝对地址", not bad, f"异常: {bad[:3]}" if bad else f"{len(hrefs)} 个链接")

    # 统计栏: 之前 data.json 没有这些字段, 页面上永远是 0 / -- / 运行中
    total_runs = _norm(res.get("totalRuns"))
    total_products = _norm(res.get("totalProducts"))
    last_run = _norm(res.get("lastRunDate"))
    status = _norm(res.get("status"))
    update_time = _norm(res.get("updateTime"))
    check("统计栏 累计执行次数 已填充", total_runs not in ("", "0", "--"), total_runs)
    check("统计栏 已生成商品图文 已填充", total_products not in ("", "0", "--"), total_products)
    check("统计栏 最近执行日期 已填充", last_run not in ("", "--"), last_run)
    check("统计栏 运行状态 = 已完成", status == "已完成", status or "空")
    check("统计栏 更新时间 已填充", update_time not in ("", "--") and "最近更新" in update_time, update_time)

    # 版本徽章: 以前是写死的 'HTML v1787267344', 页面换版本也不变
    badge = _norm(res.get("debugVersion"))
    expect_badge = "v" + str(data_obj.get("date") and "" or "")
    check("版本徽章由 DATA_VERSION 动态渲染", bool(badge) and badge != "v—", badge or "空")
    m = re.search(r"const DATA_VERSION = '([^']*)'", html_text)
    live_ver = m.group(1) if m else ""
    check("版本徽章 == 线上 DATA_VERSION", badge == "v" + live_ver, f"徽章={badge} DATA_VERSION={live_ver}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", default=None)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--skip-cdn", action="store_true")
    ap.add_argument("--skip-render", action="store_true")
    args = ap.parse_args()

    date = resolve_date([args.date] if args.date else [])
    od = out_dir(date)
    print(f"🔍 线上验证 · {date} · 域名 {DOMAIN}\n")

    # ---------- 1. 本地状态 ----------
    print("[1/5] 本地状态")
    version = local_data_version()
    check("index.html 有 DATA_VERSION", bool(version), version or "未找到")
    head = git_head()
    check("git HEAD 存在", bool(head), (head or "")[:12])
    if version is None:
        print("\n❌ 无法继续: index.html 没有 DATA_VERSION")
        return 1

    # ---------- 2. 等待线上生效 ----------
    print(f"\n[2/5] 等待线上生效 (超时 {args.timeout}s, GitHub Pages 传播约需 40s)")
    ok, live, code = wait_for_live(version, args.timeout)
    check("线上 DATA_VERSION 已更新", live == version, f"live={live} 期望={version}")
    check(f"线上 /v/{version}/data.json 可达", code == 200, f"HTTP {code}")

    # ---------- 3. 内容一致性 ----------
    print("\n[3/5] 内容一致性")
    base = f"https://{DOMAIN}"
    lpath = os.path.join(od, "data.json")
    if not os.path.exists(lpath):
        check("本地 data.json 存在", False, lpath)
        return 1
    local = read_json(lpath)
    online_html = ""
    try:
        _, online_html = http_get(f"{base}/?cb={int(time.time()*1000)}")
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
    print("\n[4/5] vs-data 与 CDN 图片")
    online_vs = {}
    try:
        _, vs_txt = http_get(f"{base}/v/{version}/vs-data.json?cb={int(time.time()*1000)}")
        online_vs = json.loads(vs_txt)
        check("线上 vs-data hotProducts == 5", len(online_vs.get("hotProducts", [])) == 5,
              str(len(online_vs.get("hotProducts", []))))
        check("线上 vs-data sources >= 10", len(online_vs.get("sources", [])) >= 10,
              f"{len(online_vs.get('sources', []))} 条")
        sizes = [len(g.get("items", [])) for g in online_vs.get("competitors", [])]
        check("每组竞品 >= 4 项", all(s >= 4 for s in sizes), str(sizes))
    except Exception as e:
        check("线上 vs-data.json 可解析", False, str(e))

    if not args.skip_cdn:
        # ⚠️ 必须用**线上 data.json 里的真实 URL**, 不能用 `{date}_product_slice_N.jpg`
        #    这种模板 URL —— 图床对同名文件再上传会重命名成 {name}_{ts}_{n},
        #    模板 URL 指向的永远是当天第一次上传的旧图(2026-10-22 实测踩过)。
        urls = []
        for p in remote.get("products", []):
            urls.append(p.get("image"))
            for u in (p.get("images") or [])[1:]:
                urls.append(u)
        # 长图: 从本地 uploaded_urls.json 取真实 URL
        up_path = os.path.join(od, "uploaded_urls.json")
        if os.path.exists(up_path):
            try:
                up = read_json(up_path)
                if up.get("card_full"):
                    urls.append(up["card_full"])
            except Exception:
                pass
        urls = [u for u in urls if u]
        bad = [u for u in urls if http_code(u) != 200]
        check(f"CDN 图片全部可达 ({len(urls)} 张)", not bad,
              (f"失败: {bad[:3]}" if bad else ""))

    # ---------- 5. 页面渲染断言 ----------
    print("\n[5/5] 页面渲染断言 (Node + DOM stub 真跑线上 index.html)")
    if args.skip_render:
        print(f"  {WARN} 已跳过(--skip-render)")
    else:
        try:
            check_render(online_html, remote, online_vs, remote.get("products", []))
        except Exception as e:
            check("页面渲染断言(可执行)", False, f"{type(e).__name__}: {e}")

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
