# 2026-10-22 深度优化 · xhs-product-push

> 14:00 自主发起 · 目标：把「能跑通」升级成「跑得对、且能被自动证明是对的」
> 触发：10-22 常规执行时发现落地页的带货链路**整条不显示**（价格/详情/购买按钮/统计栏全是空的），
> 而所有"检查文件是否存在"的脚本全部绿灯 —— 说明闸门是假的。

## 一、为什么要动

10-22 早上那趟 cron 执行结束时，12/12 项验证全过，落地页却**什么都没渲染出来**。
回头查，暴露的不是单点 bug，而是**一整类问题**：校验只证明"文件在、内容对"，
不证明"页面把内容渲染对了"。

体检出的 6 个真实缺陷（全部有量化证据）：

| # | 缺陷 | 量化证据 | 后果 |
|---|------|---------|------|
| 1 | 落地页模板字段与数据字段**对不上** | 模板写 `p.priceRange` / `p.description`，数据里是 `p.price` / `p.desc`；190 个历史商品里 `priceRange` 出现 **0** 次 | 价格、详情整块不渲染 |
| 2 | 购买链接**从来没有数据** | 190 个历史商品 `links` 写入 **0** 次 | 带货按钮全空，落地页不是带货页 |
| 3 | 卡片白字**大面积不可读** | 155 张历史卡片里 **85 张(54.8%)** 对比度 < 4.5:1，**40 张(25.8%)** < 2.5:1；今天 5 张全部不达标(1.17~2.50:1) | 每天推进飞书群的图都看不清 |
| 4 | `color` 字段**35 处是描述串** | 如 `'中国红礼盒 / 烫金书法字'` —— 旧 schema 遗留，被当成色值直接刷到卡片上 | 随时炸合成脚本 |
| 5 | 状态/版本**全是假的** | `history.json` 38 条 status 全是「运行中」；`.last_version` 停在 1792451064（实际已到 1792624129）；徽章写死 `HTML v1787267344` | 排查缓存时看到假版本号 |
| 6 | **8 处硬编码绝对路径** | db_init 1 / db_save 2 / db_export 2 / validate_schema 2 / upload 1 | 换机器/换路径即挂 |

另外两个隐蔽的：

- **落地页用 UTC 日期取当天目录**：`new Date().toISOString().slice(0,10)`。
  定时任务 07:00 CST 跑，那一刻 UTC 还是前一天 23:00 → 必然去请求昨天的目录 → 404。
- **统计栏读的是 data.json 里根本不存在的字段**：`totalRuns` / `lastRunDate` / `status` / `updateTime`，
  而 data.json 顶层只有 `date` / `totalProducts` / `products` → 永远显示 0 / -- / 运行中。

## 二、改了什么

### 1. 配色：保留"商品主色"语义，派生可读主题色

没有粗暴换成固定品牌色（那会丢掉商品识别度），而是**在 HSL 空间只压暗 lightness**，
取第一个对白字 ≥4.5:1 的颜色 —— 色相不变，视觉上仍是"这个商品的颜色"。

```
#9AA5B1 → #697888 (4.52:1)     #C9A227 → #8F731C (4.53:1)
#E8DCC8 → #8F703C (4.61:1)     #EDEDE8 → #76765D (4.65:1)
#E8B4B8 → #C84C55 (4.54:1)
```

- `lib_xhs.derive_theme_color()` —— 派生算法（WCAG 2.1 相对亮度）
- `lib_xhs.assert_data()` —— **color 早失败**：非 `#RRGGBB` 直接 raise，并说清该写什么
- `compose_cards.py` —— 顶栏/编号/标签/价格条用派生色；原色只留顶部 8px 品牌点缀条
- 落地页标题/分隔线用同一个派生色（对白底同样 ≥4.5:1）

### 2. 购买链接：真实商品页

用 WebSearch 的 shopping 模式抓真实商品详情页，**逐条 curl 核验**：

| 商品 | primary | 平台 | 核验 |
|------|---------|------|------|
| 匹克瑜伽垫 | product.suning.com/1000015651/12434518841.html | 苏宁 | 200 |
| 迈从 K99 V3 | shop.theclub.com.hk/...mcho-k99v3-mo | The Club | 200 |
| 小熊 HMJ-A50N1 | product.suning.com/12451430946.html | 苏宁 | 200 |
| 霍曼 PF20 | wiki.smzdm.com/p/70o393y | 什么值得买 | 200 |
| COACH 纽约淡香水 | vip.com/detail-0000000000-6920040719284303944.html | 唯品会 | 200 |

13 个 URL 里 12 个 200、1 个 202(什么值得买反爬，浏览器可过)。
`links` **必须落库**（`products.links`），因为 `db_export` 会用 DB 内容覆盖 data.json ——
只写在 products.json 里会被覆盖掉。
落地页优先级：`links.primary` > `links.jd/taobao/pdd` > 京东搜索兜底（保证 190 条历史数据也有入口）。
购买按钮加了 `event.stopPropagation()`，点它不再误触发大图 lightbox。

### 3. 落地页字段兼容

```
p.priceRange              →  p.priceRange || p.price
p.description             →  p.description || p.desc
links.{jd,taobao,pdd}     →  renderLinkButtons(): primary 优先 + 京东搜索兜底
new Date().toISOString()  →  localDateStr()        (UTC → 本地日期)
debugVersion 徽章         →  由 DATA_VERSION 实时渲染 (原来是写死的 v1787267344)
```

一次修好 190 个历史商品的价格显示，不改数据 schema。

### 4. 数据层：统计字段 + 状态归真 + history 索引自动化

- `build_data.py` / `db_export.py` 补 `totalRuns` / `totalProductImages` / `lastRunDate` / `status` / `updateTime`
  （口径统一走 `lib_xhs.published_stats()`，两个脚本算的是同一套）
- `db_save` 写完数据把 `runs.status` 置「已完成」；`db_export` 发布时再兜一次
- **38 条历史 status 全部从「运行中」回填为「已完成」**
- `history/history.json` **不再手工维护**：以前靠 prompt.md 里一段内联 python（那段脚本还出过错），
  现在由 `db_export` 从 `history/{date}.json` 自动重建。事实来源单一，不再漂移

### 5. verify_live：从"文件检查"升级成"渲染断言"

新增第 5 组检查：**用 Node + DOM stub 把线上 index.html 的脚本真跑一遍**，
断言渲染结果里真的有价格、详情、购买链接、统计栏有值、徽章跟随 DATA_VERSION。

这是唯一能抓住 10-22 那个 bug 的手段 —— 模板字段对不上时，
"页面能打开"和"JSON 能下载"全都成立，只有真的渲染一次才暴露。

### 6. 硬编码路径 8 → 0

`db_init` / `db_save` / `db_export` / `validate_schema` / `upload_cloudimgs` 全部改走
`lib_xhs` 的 `DB_PATH` / `TASK_DIR` / `out_dir()`。

### 7. 新增文档

- **`AGENTS.md`**（新建）—— 仓库级 agent 手册：架构约定、13 个脚本分工、硬规则、已知坑
- `prompt.md` 更新 —— links 字段怎么抓、color 只能是 hex、history.json 已自动化、渲染断言说明

## 三、执行中撞到的两个新 bug（比计划外的更值钱）

重跑后半段时发现**落地页拿到的还是改色前的旧卡片**。查下去是两个叠加的 bug：

### Bug A：图床对同名文件会重命名

```
2026-10-22_product_slice_3.jpg                  ← 模板 URL → 旧图(浅米色 232,219,200)
2026-10-22_product_slice_3_1792651209178_1.jpg  ← 真实 URL → 新图(深棕 143,111,60)
```

图床**第一次**上传保留原名，之后同名再传会变成 `{name}_{时间戳}_{n}.jpg`。
所以确定性模板 URL `{date}_product_3.jpg` **永远指向当天第一次上传的那份**。
今天重传了改色后的卡片，落地页却还在显示旧的浅色卡片。

### Bug B：`uploaded_urls.json` 结构和文件名**两处都对不上**

| | 写入方 | 读取方 | 结果 |
|---|--------|--------|------|
| 结构 | `{"uploaded": [列表]}` | 读 `u["images"]` | 拿到空 dict |
| 文件名 | 写 `uploaded_urls.json` | 读 `image_urls.json` | 文件不存在 |

两个都对不上 → `img_urls` 恒为空 → **永远退回模板 URL** → 落地页永远显示当天第一版图。
这解释了为什么这个 bug 能潜伏这么久：模板 URL **是能访问的**（200），
所有"CDN 图片可达性"检查都通过，只有肉眼看图才发现内容是旧的。

修复：
- `upload_cloudimgs.py` 额外写 `images` / `slices` / `card_full` 三个映射（pid → 真实 URL）
- `db_save.py` 读 `uploaded_urls.json`（兼容旧名），并用真实 URL **覆盖**模板 URL
- `verify_live.py` 的 CDN 检查改成用**线上 data.json 里的真实 URL**，不再拼模板 URL

## 四、验证结果

- 卡片对比度：5/5 全部 ≥4.5:1（4.52 ~ 4.65）
- 商品链接：13 个 URL 全部核验（12×200 + 1×202）
- `db_export` 输出 **8 个** json（原 7 个 + 自动重建的 history 索引）
- `history/history.json` 38 条，status 全部「已完成」
- `validate_schema.py` 通过
- `verify_live.py` **页面渲染断言**：5 张卡片全部渲染出价格/详情/购买链接，
  统计栏 38 / 190 / 2026-10-22 / 已完成，徽章 = 当前 DATA_VERSION
- 硬编码绝对路径：8 → **0**

## 五、教训

1. **闸门必须验证"结果"而不是"中间产物"**。
   12/12 全绿但页面全空 —— 文件存在 ≠ 页面正确。
   现在的做法是：把线上 HTML 真跑一遍渲染，断言输出里**有内容**。
2. **"URL 能访问"不等于"URL 指向最新内容"**。
   模板 URL 返回 200，但指向的是旧文件。校验要看**内容**（像素/文本），不看状态码。
3. **两个地方写同一个文件名/结构时，接口要对齐**。
   Bug B 是典型的"写的人叫 A、读的人叫 B"，两边都没报错，只是不生效。
   这种 bug 最贵 —— 因为所有存在性检查都通过。

## 🎯 下次触发

- 2026-10-23 07:00 cron 自动执行
- 选品避让：瑜伽垫 / 机械键盘 / 和面机 / 喂食器 / 香水
- 建议方向：母婴出行 · 清洁电器 · 珠宝饰品 · 文具书写 · 户外登山 · 家居香薰 · 智能穿戴 · 厨房小工具
- ⚠️ 明天开始 products.json **必须**写 `links`（真实商品页 URL，逐条 curl 核验）
