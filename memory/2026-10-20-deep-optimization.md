# 2026-10-20 深度优化 · xhs-product-push

> 22:00 自主发起 · 目标：把「每天复制粘贴样板」的管线改成「内容与代码分离」的稳定管线
> 触发：10-20 那趟执行时连续踩到 3 个由"样板复制"引发的缺陷

## 一、为什么要动

10-20 那趟 cron 执行结束时，我在日志里记了 7 条踩坑。回头看，其中 **3 条的根因是同一个**：
**同一段样板代码被复制了几十份，改一处漏一处。**

| # | 现象 | 根因 |
|---|------|------|
| 1 | cron prompt 的 `git add` 写 `history.json`（根目录根本没这文件）→ 整批 add 中止 → commit 报 "no changes added" → push 报 "Everything up-to-date"，**全链路看起来成功，实际一个文件都没推上去** | prompt.md 与 cron prompt 两处各写了一遍这段 git 命令，改的时候只改了一处 |
| 2 | `db_save.py` 打印 "(5 组 × 4 项)"，实际是 25 项(5×5) | 日志文案硬编码，跟真实数据脱钩 |
| 3 | prompt.md step 13 的内联 python 混进一行游离的 `202`，复制就 SyntaxError | 样板内联在 markdown 里，没有语法检查 |

而仓库里的结构直接放大了这个风险：

```
compose_cards_YYYYMMDD.py   35 份   ← 归一化日期后 20+ 份完全一致, 只差一行 TODAY
build_data_YYYYMMDD.py      29 份   ← 每份 220 行, 只有 products 列表是新的
build_vs_data_YYYYMMDD.py   29 份   ← 同上
gen_images_YYYYMMDD.sh/mjs  23 份
attach_cdn_urls_*.py         4 份   ← 已被取代
append_history_*.py          1 份   ← 已被取代
push_via_api.py              1 份   ← 已被取代, 且是脚雷
────────────────────────────────────
                          123 份样板副本
```

`scripts/` 一度有 130 个文件，其中 123 个是"每天重新生成一遍"的。

## 二、改了什么

### 2.1 内容与代码分离（核心）

| | 每天变 | 长期不变 |
|---|---|---|
| 位置 | `output/{date}/products.json`<br>`output/{date}/vs.json`<br>`output/{date}/image_prompts.json` | `scripts/` 下 13 个通用脚本 |
| 写入方 | **agent 写 3 个纯 JSON** | 不用写 |

```bash
python3 scripts/build_data.py     2026-10-21   # products.json      → data.json
python3 scripts/build_vs_data.py  2026-10-21   # vs.json            → vs-data.json
bash   scripts/gen_images.sh      2026-10-21   # image_prompts.json → images/product_1..5.jpg
python3 scripts/contact_sheet.py  2026-10-21   # 拼图核对(出图后必做)
python3 scripts/compose_cards.py  2026-10-21   # data.json          → 长图 + 5 切片
```

所有脚本接受日期位置参数或 `--date=` / `XHS_DATE=`，默认今天。
`lib_xhs.py` 统一了路径解析、日期校验（非法日期直接报错，不会静默写错目录）、
schema 断言（data.json / vs-data.json）。

**收益**：agent 每天少写约 700 行样板代码 → 少几百个能抄错的地方；
`scripts/` 从 130 个文件降到 13 个。

### 2.2 修掉的缺陷

| 缺陷 | 修法 |
|---|---|
| `db_save.py` 硬编码 "(5 组 × 4 项)" 假日志 | 改成从实际数据动态计算分组数与每组项数 |
| cron prompt `git add history.json` pathspec 错 → 静默失败 | prompt 改为只写 `history/`，并加"别信 exit code，看有没有 `main -> main`"的判据 |
| prompt.md step 13 内联 python 语法错（游离的 `202`） | 改为 heredoc 脚本 + 同日幂等（先 filter 掉旧 entry 再 append） |
| 死代理端口写死 7897（10-20 实际已变 6696） | 全部改成"显式 unset / --noproxy / -c http.proxy="，**做法对端口变化免疫** |
| 根目录 `compose_cards.py` 是 2026-08-05 的硬编码旧副本（跑它会产出 8/5 的染发膏卡片） | 替换为真·通用版 |
| 没有任何步骤确认"线上真的换成今天的数据了" | 新增 `verify_live.py` 端到端验证闸门 |

### 2.3 新增的能力

**`scripts/verify_live.py`** —— 之前 push 成功 ≠ 用户看到的页面是新的。现在这个判断是自动的：

```bash
python3 scripts/verify_live.py 2026-10-21
# 轮询等 GitHub Pages 传播(实测约 40s, 最多 180s)
# 校验: 线上 DATA_VERSION / v/{VERSION}/data.json 与本地一致 /
#       5 商品 image 全 CDN URL / hotProducts=5 / sources>=10 / 每组竞品>=4 /
#       11 张图床图片 HTTP 200
# 退出码 0 = 线上已完整切换
```

**`scripts/contact_sheet.py`** —— 把 10-19/10-20 两次"手写拼图核对"固化成脚本，
让"出图后肉眼核对"从"想起来才做"变成固定动作（10/18 图文不符事故的防线）。

### 2.4 仓库治理

| 项 | 前 | 后 |
|---|---|---|
| `scripts/` 文件数 | 130 | **13**（+ `archive/` 123 份历史脚本） |
| 根目录散落文件 | 20 个 2026-08 遗留 + 17 个根级 compose_cards + `2026-07-31/` | **0** |
| git 跟踪的 output 图片 | 472 张 / **214.3 MB** | **0**（`.gitignore` + `git rm --cached`，磁盘文件保留） |
| output 下仍跟踪的 json | 123 | **123**（一个没少 —— 落地页兜底数据源） |
| 死代理脚本 | `push_via_api.py` 在活跃目录 | 归档（走 API 建 commit 会造成 SHA 分叉） |

> ⚠️ 只排图片不排 json：`index.html` 的 fetch 链里有 `./output/${today}/data.json`
> 作为 fallback 数据源，那些 json 必须继续入库。

### 2.5 prompt 同步

- `prompt.md` 重写为新流程（内容文件驱动），并修掉上述 3 个缺陷
- **线上 cron prompt 同步更新**（`cron_update`，cron_id `60fb5156-...`），
  下次触发 2026-10-21 07:00

## 三、等价性验证（最关键的一步）

重构不能"看起来能跑"。做法：拿**今天已经发布**的产物当基准，
用新流程从内容文件重建，再逐字节/逐字段对比。

```
新流程: products.json → build_data.py → db_save → db_export
        vs.json       → build_vs_data.py → db_save → db_export

对比基准: 10-20 当天已发布并已上线的版本

  data.json     语义完全相等 ✅   7 个位置 md5 全部 2fbcc62e0997
  vs-data.json  语义完全相等 ✅   3 个位置 md5 全部 a1a77d4d8f3d
  product_slice_3.jpg 重合成后 byte-identical ✅
  validate_schema.py 通过, 0 错误
```

**结论：新管线与旧管线产出等价，可以安全切换。**

### 3.1 验证中发现并修掉的 2 个设计问题

1. **竞品 `color` 语义** —— 我最初让 `build_vs_data.py` 把每组竞品的颜色统一继承主推商品色。
   但竞品配色是落地页 chip 的**视觉区分手段**（10-20 手工写的 25 个色值是刻意区分的）。
   折中：内容文件里写了 `color` 就用它，没写才继承主推色。
2. **派生基准被污染** —— 第一次对比时，我从 `output/2026-10-20/vs-data.json` 反推 `vs.json`，
   而那个文件**已经被上一轮错误的 build 覆盖过**（颜色全被重置成默认值），
   于是把错误值当基准又验证了一遍。改为从 `/tmp/ref_vs.json`（未被污染的已发布版）派生。

> 教训：**做等价性验证时，基准必须是独立保存的副本**，不能从"当前工作目录"反推 ——
> 否则验证的是"脚本和它自己一致"。

## 四、遗留与建议

| 项 | 状态 | 说明 |
|---|---|---|
| `.git` 目录 579M | **未处理** | 本次只是"止血"（不再增长），历史提交里的 214MB 图片还在历史中。
彻底瘦身需 `git filter-repo` 重写历史 + **force push**。
⚠️ 强制推送会造成本地与远端 SHA 分叉 —— tasks.json 记录过 10-17 走 API 建 commit
导致的同类事故。**这个操作需要单独评估，本次没做。** |
| `v/` 52 个版本目录 | 未处理 | 1.4MB, 体积可忽略, 保留（它是 CDN cache-bust 机制） |
| `output/` 磁盘 217MB | 未处理 | 磁盘不是瓶颈, 且本地重传图床需要留底 |
| `xhs-ai-pack/` | 保留 | 文档包, 与管线无关 |

## 五、改动清单

```
新增  10 个: scripts/{lib_xhs,build_data,build_vs_data,contact_sheet,verify_live}.py
               scripts/gen_images.sh
               scripts/archive/README.md
               output/2026-10-20/{products,vs,image_prompts}.json
               memory/2026-10-20-deep-optimization.md
修改   6 个: scripts/{db_save,compose_cards}.py  prompt.md  .gitignore
               output/2026-10-20/{data,vs-data}.json (重生成, 内容等价)
归档 143 个 → scripts/archive/
删除 502 个 (472 张 output jpg 移出索引 + 20 个 2026-08 根目录遗留 + 10 个其他)
```

## 六、下次触发注意

- 2026-10-21 07:00 cron 会走**新流程**。第一件事是写 3 个内容文件；
  如果 agent 还在生成 `build_data_YYYYMMDD.py`，说明 prompt 没生效，要检查 cron prompt。
- 新流程的产物布局多了一层 `output/{date}/products.json` 等内容文件，
  它们应该进 git（是当天的"源"）。
- `verify_live.py` 建议在 push 后必跑，它是唯一能确认"用户看到的是今天数据"的检查。
