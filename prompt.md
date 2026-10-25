# xhs-product-push 自动化任务 prompt 模板

> **2026-10-21 重写**：内容与代码分离。每天只写 3 个**纯数据文件**，不再生成 250 行的 Python 脚本。
> 详见 `scripts/archive/README.md`（历史 93 个按日期生成的脚本已归档）。

## 任务
每天 07:00 cron 触发，跑「小红书商品图文带货」全流程，产出：
- 5 个当日精选商品详情图
- 飞书群卡片推送
- landing page 数据更新

## 必读
- `/Users/xiaoan/Documents/TimeTask/config/xhs.env.sh` 加载环境变量
- 凭证：`~/.minimax/credentials/general/feishu.json`（appId/appSecret，真实）
- 图床：`cloudimgs.iepose.cn` POST /api/upload-file
- 历史参考：`memory/$(date -v-1d +%Y-%m-%d).md`（昨天的执行日志）
- 9/02 bug 修复记录：`memory/2026-09-02.md` 末尾的"## 🐛 Bug 发现与修复"

---

## 核心概念：内容 vs 代码

| 类型 | 位置 | 谁写 |
|------|------|------|
| **内容**（每天不同） | `output/{date}/products.json`<br>`output/{date}/vs.json`<br>`output/{date}/image_prompts.json` | **你（agent）写** |
| **代码**（长期不变） | `scripts/` 下 13 个通用脚本 | 不用写，直接调 |

所有脚本都接受日期参数，默认今天，也支持 `XHS_DATE=2026-10-21`。

---

## 完整流程

### 1. 加载环境
```bash
source /Users/xiaoan/Documents/TimeTask/config/xhs.env.sh
echo "TASK_XHS_DIR=$TASK_XHS_DIR IMG_HOST_PRIMARY=$IMG_HOST_PRIMARY"
```

### 2. 前置检查
```bash
# 凭证(可选,缺失会跳过飞书推送)
ls ~/.minimax/credentials/general/feishu.json
# SQLite 建表(idempotent, 不会重置数据)
python3 ${TASK_XHS_DIR}/scripts/db_init.py
```

### 3. 读昨日执行日志，避免选品重复
```bash
ls -la ${TASK_XHS_DIR}/memory/ | tail -3
cat ${TASK_XHS_DIR}/memory/$(date -v-1d +%Y-%m-%d).md 2>/dev/null | grep -A 20 "今日精选商品"
```
再扫 `history/*.json` 提取近 7 天全部 product name，选 5 个**不重复**的。

### 4. WebSearch 选品
- 秋季/初冬/双 11 前哨 主题
- 覆盖 5 大不同场景（不要全选数码/全选厨房）
- 价格 ¥10-500 区间（小红书带货主力价位）
- 价格/销量/评论数**必须来自真实搜索结果，严禁编造**
- **先按价格带筛，再看销量**（10/22 踩坑：迪奥 30ml ¥594.5 超价被排除）
- **同时抓真实商品页 URL**（`links.primary`），见 5.1

### 5. 写 3 个内容文件

#### 5.1 `output/{date}/products.json` —— 5 个商品
```json
[
  {
    "id": 1,
    "name": "完整商品名",
    "category": "品类标签",
    "price": "¥XX(规格·渠道)",
    "desc": "150-200 字真实描述(来源: web search)",
    "highlights": ["亮点1","亮点2","亮点3","亮点4","亮点5"],
    "tags": ["标签1","标签2","标签3","标签4","标签5"],
    "suitable": "适用人群",
    "price_note": "价格说明 + 渠道",
    "color": "#RRGGBB",
    "links": {
      "primary": "https://真实商品页URL",
      "source": "苏宁/唯品会/什么值得买",
      "extra": ["https://另一个真实商品页URL"]
    }
  }
]
```
> `image` / `images` **不要写**，脚本会自动按 CDN 模板补齐。

**`links` 怎么来的（2026-10-22 新增，必填）**
- 用 WebSearch 的 `search_type=shopping` 搜「商品名 + 商品详情页/购买」，
  返回结果里带 `product.suning.com` / `www.vip.com` / `wiki.smzdm.com` /
  `mitem.jd.hk` / `24h.pchome.com.tw` / `shop.theclub.com.hk` 这类**商品详情页**的即为可用。
- ⚠️ **`search.jd.com` / `item.jd.com` 直链拿不到**（京东反爬，curl 无输出），
  不要在它上面浪费时间。
- 每个 URL 都要 `curl --noproxy '*' -o /dev/null -w '%{http_code}' -L` 核验一遍，
  200/202 才写进 products.json。**严禁编造 URL**（编出来的链接 404 = 假带货链路）。
- `links` 会落库（`products.links`）→ 落地页「购买」按钮直接指向该商品页。
  历史 190 个商品没有 links，落地页会自动回退到京东搜索链接。

**`color` 只能是 `#RRGGBB`**
- 语义 = **商品主色**（浅灰垫 / 奶白机 / 金键盘…），不是主题色。
- 脚本会把它派生成 `theme_color`（同色相、压暗到对白字 ≥4.5:1），
  卡片和落地页共用这个派生色。**你只写商品主色，不要自己压暗**。
- 必须是合法十六进制。写成 `"中国红礼盒 / 烫金书法字"` 这类描述串会被
  `assert_data` 直接 raise（历史上 35 处坏数据就是这么来的）。

#### 5.2 `output/{date}/vs.json` —— 竞品数据
```json
{
  "sources": ["真实来源 URL 或站点名", "..."],
  "competitors": [
    {
      "product": "品类 价位段区间",
      "items": [
        {
          "name": "商品名",
          "price": "¥XX",
          "advantage": "核心优势",
          "jd_sales": "销量/排行 + 来源出处",
          "color": "#RRGGBB"
        }
      ]
    }
  ],
  "hotProducts": [
    {"name":"商品名","category":"品类","price":"¥XX","sales":"销量/排行摘要","platform":"京东自营/天猫旗舰"}
  ]
}
```
- `competitors` **每组至少 4 项**（`validate_schema.py` 硬约束），建议写 5 项
- 每组第 1 项 = 当日主推商品
- `hotProducts` 固定 **5 项**，与 5 个主推商品一一对应
- `image` **不要写**，脚本自动补；`color` 可省，省略时继承所属组主推商品的配色
- `sources` 至少 10 条真实 URL

#### 5.3 `output/{date}/image_prompts.json` —— 5 条出图 prompt
```json
{
  "1": "Product photography of ..., minimalist e-commerce style, no text, no watermark",
  "2": "...",
  "3": "...",
  "4": "...",
  "5": "..."
}
```
每个 prompt 必须与 `products.json` 里**同序号的商品**严格对应。

### 6. 生成 data.json / vs-data.json
```bash
TODAY=$(date +%Y-%m-%d)
python3 ${TASK_XHS_DIR}/scripts/build_data.py     $TODAY
python3 ${TASK_XHS_DIR}/scripts/build_vs_data.py  $TODAY
```
脚本自带 schema 断言，失败直接 raise，不会流到落库和发布。

### 7. 生成 5 张 1:1 配图
```bash
bash ${TASK_XHS_DIR}/scripts/gen_images.sh $TODAY
```
- `gen_images.sh` 内部已 `unset` 代理变量 + `NO_PROXY="*"`，**不要在外层重复加代理**
- 失败会 exit 1，必须重试到 5 张全出

### 8. ⚠️ 出图后必须肉眼核对（10/18 踩坑 #2）
```bash
python3 ${TASK_XHS_DIR}/scripts/contact_sheet.py $TODAY
```
生成 `_contact_sheet.jpg`，**打开看**，确认 5 张图与 5 个商品名一一对应。
选品中途换过 SKU 的话，prompt 必须同步改，否则会出现"卡片写梨、配图是山药"。

### 9. PIL 合成 5 卡片长图
```bash
python3 ${TASK_XHS_DIR}/scripts/compose_cards.py $TODAY
```
输出 `product_card_full.jpg`（1080×15080）+ `product_slice_1..5.jpg`（各 1080×3000）。

### 10. 上传 11 张图到 cloudimgs
```bash
python3 ${TASK_XHS_DIR}/scripts/upload_cloudimgs.py $TODAY
```
上传内容：1 全图 + 5 切片 + **5 张 product_1..5.jpg（1:1 纯图，landing page 要用）**。
⚠️ 只传切片不传纯图 → landing page 图片全空。

### 11. 飞书推送（可选，凭证缺失跳过）
```bash
python3 ${TASK_XHS_DIR}/scripts/feishu_push_optimized.py \
  ${TASK_XHS_DIR}/output/$TODAY $TODAY
```
build_card 会断言 img 元素数 == 上传成功数，空卡片会 raise。

### 12. SQLite 落库 + 导出
```bash
python3 ${TASK_XHS_DIR}/scripts/db_save.py   $TODAY
python3 ${TASK_XHS_DIR}/scripts/db_export.py $TODAY $VERSION
python3 ${TASK_XHS_DIR}/scripts/validate_schema.py $TODAY
```
- `db_save` 幂等：同日重复跑会覆盖（DELETE + INSERT）；写完把 `runs.status` 置为「已完成」
- `db_export` 导出到 **8 个位置**：`output/{date}/` + `v/{VERSION}/` + 根目录 +
  `history/{date}.json` + `history/history.json`
- `history/history.json`（落地页时间线索引）**由 db_export 自动重建**，
  事实来源 = `history/{date}.json`，不要再手工追加（见 step 14）
- `validate_schema` 失败即 abort，不会发布坏数据

### 13. 版本号更新 + 版本化路径（关键！防 CDN 和浏览器缓存旧数据）
```bash
TODAY=$(date +%Y-%m-%d)
VERSION=$(date +%s)   # Unix 时间戳，每个 push 唯一
# 更新 index.html 里的 DATA_VERSION 常量和 meta 标签
sed -i '' "s/const DATA_VERSION = '[^']*'/const DATA_VERSION = '${VERSION}'/" "${TASK_XHS_DIR}/index.html"
sed -i '' "s/content=\"[^\"]*\" \/>/content=\"${VERSION}\" \/>/" "${TASK_XHS_DIR}/index.html" 2>/dev/null || true
# 同步根目录 fallback
cp "${TASK_XHS_DIR}/output/${TODAY}/data.json"    "${TASK_XHS_DIR}/data.json"
cp "${TASK_XHS_DIR}/output/${TODAY}/vs-data.json" "${TASK_XHS_DIR}/vs-data.json"
```
> `v/{VERSION}/` 目录由 step 12 的 `db_export.py` 创建，不用手动 mkdir。

### 14. history.json（**已自动化，不用手工做**）
`history/history.json` 由 step 12 的 `db_export.py` 自动重建：
它扫 `history/{date}.json` 逐日生成时间线条目（date / totalRuns / productCount /
updateTime / status），`status` 固定「已完成」。

> ⚠️ 以前这一步靠 prompt 里的一段内联 python 手工追加，那段脚本出过 bug，
> 结果 38 条记录的 status 全停在「运行中」，落地页"运行状态"永远显示进行中。
> **现在不需要也不应该再手工追加** —— 手工改会被下一次 db_export 覆盖。

### 15. git add + commit + push
```bash
cd ${TASK_XHS_DIR}
git add output/${TODAY}/ history/ data.json vs-data.json v/ index.html memory/${TODAY}.md
git commit -m "xhs-push: ${TODAY} 商品图文 (5个精选商品)"
bash ${TASK_XHS_DIR}/scripts/push_with_probe.sh origin main
```

> `push_with_probe.sh` 会**动态探测**可用代理(端口有监听 + 经它访问 github.com 返回 200),
> 探不到才直连。**不要手写 `git -c http.proxy=` 硬绕**——10/21 实测代理活着时绕过反而推不上去。
⚠️ **pathspec 注意**：仓库根目录**没有** `history.json` 这个文件，它在 `history/` 目录下。
写 `git add history.json` 会让 git 报 `pathspec did not match any files`，
而 `git add` 遇到坏 pathspec 会**整批中止**（已 add 的也作废），
后续 commit 报 "no changes added to commit"、push 报 "Everything up-to-date"——
**全链路看起来都成功，实际一个文件都没推上去**。
所以只写 `history/`（目录形式已包含 history.json），**不要单独列 history.json**。
判据：**别信 push 的 exit code，要看输出里有没有 `main -> main` 或 SHA 区间的行**。

### 16. 线上验证（2026-10-21 新增，建议必做）
```bash
python3 ${TASK_XHS_DIR}/scripts/verify_live.py $TODAY
```
- 轮询等待 GitHub Pages 构建传播（实测约 40s，最多等 180s）
- 校验：线上 DATA_VERSION、v/{VERSION}/data.json 内容与本地一致、
  5 商品 image 全为 CDN URL、11 张图在图床 HTTP 200
- **页面渲染断言**（2026-10-22 新增）：用 Node + DOM stub 把**线上** index.html
  的脚本真跑一遍，断言渲染结果里真的有价格、详情、购买链接，统计栏有值，
  版本徽章跟随 DATA_VERSION。这一项专门抓"数据在但页面不显示"——
  2026-10-22 之前模板写 `p.priceRange` / `p.description`，数据里却是
  `p.price` / `p.desc`，字段对不上导致价格和详情整块不渲染，
  而所有"检查文件存在"的脚本都发现不了。
- 退出码 0 = 线上已完整切换到今天的数据

### 17. 写执行日志
`${TASK_XHS_DIR}/memory/$(date +%Y-%m-%d).md`
记录：执行时间 / 5 商品 / 选品来源 / 数据生成 / 工程产物 / Git 状态 / 踩坑 / 下次触发

---

## 已知风险与约定

- **本机代理端口会变，而且"活着/死掉"不固定**：`HTTP_PROXY`/`HTTPS_PROXY` 指向本地端口，
  **有时有监听（clash-verge 在跑），有时没有**：
  - 10-17 端口 7897 **无监听** → 必须绕过
  - 10-20 端口 6696 **无监听** → 必须绕过
  - 10-21 端口 6696 **有监听** → **绕过反而连不上**：`github.com` 直连 TCP 443 直接超时，
    经代理 0.75s 返回 200；而 `api.github.com` / `codeload.github.com` 直连都正常
  → **正确做法是"探测"，不是"记住端口号"，也不是"一律绕过"**：
  - git → `bash scripts/push_with_probe.sh origin main`（自动探测，探不到才直连）
  - curl → 同样先探活；**确认某端口没监听后**才用 `--noproxy "*"`
  - mmx → `gen_images.sh` 内部已处理，调用前别加代理
  - 飞书 → `feishu_push_optimized.py` 内部已处理
  - 诊断口诀：`nc -z -G 2 127.0.0.1 <port>` 看有没有监听，
    再 `curl -x http://127.0.0.1:<port> -m 20 -w '%{http_code}' https://github.com/` 看能不能真通
- **不要用 `scripts/archive/push_via_api.py`**：10-17 代理故障时的临时绕行方案，
  会造成本地与远端 SHA 分叉（内容相同但哈希不同），后续推送全部变复杂。
  现在用 step 15 的 `push_with_probe.sh` 即可（自动选代理或直连）。
- vs-data.json 的价格/销量数据必须来自真实搜索结果，**严禁编造**。
- `history/{date}.json` 必须每执行一次同步一份（`db_export` 自动做）；
  `history/history.json` 由 `db_export` **自动重建**，不要手工追加。
- **links 里的 URL 严禁编造**：每个都要 curl 核验 200/202。
  编造的链接 = 假带货链路，比没有链接更糟。
  ⚠️ **`www.sohu.com/a/...` 文章页 curl 恒 403**（直连 / 代理 / 浏览器 UA 全试过）。
  要引用搜狐内容时改用可 200 的镜像域：`db.m.auto.sohu.com/model_.../a/...`、
  `gov.sohu.com/a/...`。**别把 www.sohu.com 写进 links.primary**，否则落地页「购买」按钮点开就是 403。
  💡 京东商品直链（`item.jd.com` / `search.jd.com`）依然拿不到，但 **`www.jd.com/phb/*.html`
  排行榜页可以 curl 200**，且页内含商品名 + 真实评论数 + 榜单名次 —— 是 links.primary 的优质兜底。
- **出图 prompt 里的颜色词必须跟 `products.json` 的 `color` 字段对齐**（2026-10-26 新增）：
  `color` 不只决定卡片配色，**出图 prompt 写错颜色 = 配图与实物不符 = 假带货**。
  10/26 实测：prompt 写 "white WiFi router"，但真实中兴巡天 BE5100 是黑色、color 写的是 `#2B2B2E`，
  结果卡片深黑主题配一张白路由器，图文割裂。→ 写 prompt 前先看 `color` 字段，
  把商品主色翻译进 prompt（如 `#2B2B2E` → "matte black"），出图后用 contact_sheet 二次核对颜色。
- **WebSearch(search_type=shopping) 结果体积会爆**：单次输出常被外部化成 78KB+ 的 artifact。
  → 用 `grep` 定向捞 `"link":` / 价格 / 评论数，**不要通读整个 artifact**；
  一次搜不全就补搜，别在单次查询里堆太多关键词。
- 补全缺失日期时用 `output/{date}/data.json` 扫描补全。
- **GitHub Pages CDN 有 max-age=600 缓存 bug + 浏览器本地缓存**，
  必须在 step 13 更新 DATA_VERSION + 走 `v/{时间戳}/` 路径，landing page 才会拿到最新数据。
- 推送后 GitHub Pages 有约 40s 构建传播延迟，遇到 404/旧版本号**先轮询 2-3 分钟再下结论**，
  不要立刻重复 push（会多造空版本目录）。
- `output/**/*.jpg` 已在 .gitignore 中（**215MB** 的重复图片，落地页只读图床 CDN 的 URL），
  `git add output/${TODAY}/` 时会自动跳过；`output/${TODAY}/*.json` 仍会入库（landing page 的兜底数据源）。

## Schema 校验（脚本内已内置，失败即 abort）
- `data.json`：`products[].image` 必须是 https CDN URL、`images[]` ≥1 项、
  `highlights` 恰好 5 条、`tags` 恰好 5 个、`desc` ≥150 字、`price` 非空、
  **`color` 必须是合法 `#RRGGBB`**（非法即 raise）、
  **`links` 里的每个 URL 必须是 http(s) 绝对地址**
- `vs-data.json`：`hotProducts` 恰好 5 项且每项含 CDN image、
  每组竞品 ≥4 项、`sources` ≥10 条、`dataSource` / `updateTime` 必填
