# AGENTS.md — xhs-product-push

> 面向在本仓库干活的 agent（AI 或人）。先读这一页，再动手。
> 面向"每天跑一次"的详细步骤见 [`prompt.md`](prompt.md)。

## 这是什么

一个每天 07:00 由 cron 触发的**小红书商品图文带货**自动化任务：
选 5 个商品 → 生成配图 → 合成详情长图 → 上传图床 → 推飞书群 → 更新落地页。

- 落地页：`https://xhs.220616.xyz`（GitHub Pages，CNAME）
- 仓库根目录：`/Users/xiaoan/Documents/TimeTask/xhs-product-push`
- SQLite：`xhs_push.db`（runs / products / highlights / tags / competitors / sources / hot_products）
  —— **本地文件，不入库**（.gitignore）。发布真源是 `history/{date}.json` + 根目录 json。
- 图床：`https://cloudimgs.iepose.cn/api/upload-file`
- 飞书凭证：`~/.minimax/credentials/general/feishu.json`

## 最重要的架构约定：内容与代码分离

| 类型 | 位置 | 谁写 |
|------|------|------|
| **内容**（每天不同） | `output/{date}/products.json`<br>`output/{date}/vs.json`<br>`output/{date}/image_prompts.json` | agent 写 |
| **代码**（长期不变） | `scripts/` 下 13 个通用脚本 | 直接调，别改 |

**绝对不要**再生成 `build_data_YYYYMMDD.py` 这类按日期的脚本。
历史 93+ 份已归档到 `scripts/archive/`（只读，不要复活）。
`scripts/archive/` 里的文件保留着 10 月前的硬编码绝对路径，是历史快照，不是模板。

所有脚本都接受日期参数，默认今天，也支持 `XHS_DATE=2026-10-21`：

```bash
source /Users/xiaoan/Documents/TimeTask/config/xhs.env.sh
cd ${TASK_XHS_DIR}
python3 scripts/build_data.py 2026-10-22
```

## 13 个脚本各自干什么

| 脚本 | 作用 | 备注 |
|------|------|------|
| `lib_xhs.py` | 公共脚手架：日期解析 / 路径常量 / schema 断言 / 颜色引擎 / 统计 | **改逻辑优先改这里** |
| `build_data.py` | `products.json` → `data.json` | 补 image/images、派生 theme_color、写统计字段 |
| `build_vs_data.py` | `vs.json` → `vs-data.json` | |
| `gen_images.sh` | 5 张 1:1 配图（mmx） | 内部已处理代理，**外层别再加** |
| `contact_sheet.py` | 拼 5 图对照图 | **出图后必须肉眼核对** |
| `compose_cards.py` | 合成 1080×15080 长图 + 5 切片 | 用派生主题色，保证白字 ≥4.5:1 |
| `upload_cloudimgs.py` | 上传 **11 张**（1 全图 + 5 切片 + 5 纯图） | 只传切片 → 落地页图全空 |
| `feishu_push_optimized.py` | 飞书卡片推送 | 内部已处理代理 |
| `db_init.py` | 建表 + 幂等迁移 | |
| `db_save.py` | 落库（覆盖语义） | |
| `db_export.py` | 导出 **8 个** json + 重建 history 索引 | |
| `validate_schema.py` | 从 DB 校验 | 失败即 abort |
| `verify_live.py` | 线上端到端闸门（含**页面渲染断言**） | |

## 数据流

```
products.json  ┐
vs.json        ├─→ build_data/build_vs_data ─→ data.json / vs-data.json
image_prompts  ┘         │
                          ↓
                     gen_images.sh ─→ images/product_1..5.jpg
                          ↓
                     compose_cards ─→ product_card_full.jpg + product_slice_1..5.jpg
                          ↓
                     upload_cloudimgs ─→ 11 张上 CDN
                          ↓
              ┌───────────┴───────────┐
        feishu_push                 db_save → db_export(8 个 json)
                                              ↓
                                    index.html DATA_VERSION + v/{VERSION}/
                                              ↓
                                        git push → verify_live
```

**注意 `db_export` 会用 DB 的内容覆盖 `data.json`。**
所以任何要出现在落地页上的字段（`links` 等）必须**落库**，
只写在 `products.json` 里是不够的 —— 会被覆盖掉。

## 硬规则

1. **价格 / 销量 / 评论数 / 商品链接必须来自真实搜索结果，严禁编造。**
   编造的链接比没有链接更糟（假带货链路）。每个 URL 都要 curl 核验 200/202。
2. **选品零重复**：扫 `history/*.json` 近 7 天的 product name + 读昨日 `memory/*.md`。
3. **先按价格带筛（¥10-500），再看销量。**
4. **`color` 只能是 `#RRGGBB`**，语义是"商品主色"。
   脚本会派生 `theme_color`（同色相、压暗到对白字 ≥4.5:1），你不用自己压暗。
   写成中文描述串会被 `assert_data` 直接 raise。
5. **`image` / `images` 不要写**在内容文件里，脚本自动补 CDN URL。
6. **每个脚本都从 `lib_xhs` 取路径常量**，不要硬编码绝对路径。
7. **改完必须重跑 `verify_live.py`**，看退出码，不是看日志顺眼。

## 已知坑（都踩过，别再踩）

- **代理端口会变而且生死不定** → 只能**探测**，不能记忆，也不能一律绕过。
  git 用 `bash scripts/push_with_probe.sh origin main`。
  **不要手写 `git -c http.proxy=` 硬绕**，也不要用 `scripts/archive/push_via_api.py`（会造成 SHA 分叉）。
- **push 判据不是 exit code**，是输出里有没有 `main -> main` 或 SHA 区间行。
- **`git add` 遇到坏 pathspec 会整批中止**（已 add 的也作废），
  后面 commit 报 "no changes added"、push 报 "Everything up-to-date" —— 全链路假成功。
  仓库根目录**没有** `history.json`，它在 `history/` 目录下。
  **只写 `history/`（目录形式已包含 history.json），不要单独列 history.json。**
- **memory 日志必须在 `git add` 之前写好**，否则 pathspec 报错会整批中止。
- **CDN 有 max-age=600 缓存 bug**：必须更新 `DATA_VERSION` + 走 `v/{时间戳}/` 路径。
- **GitHub Pages 推送后约 40s 传播**：404/旧版本先轮询 2-3 分钟再下结论，别重复 push。
- **落地页取当天目录用的是本地日期**：以前写的是 UTC 日期，
  07:00 CST 属于当天但 UTC 还是前一天 → 必然 404。已修为 `localDateStr()`。
- **`history/history.json` 不要手工追加**，`db_export` 会从 `history/{date}.json` 自动重建。
- **图床对同名文件再上传会重命名成 `{name}_{ts}_{n}`**：
  确定性模板 URL（`{date}_product_3.jpg`）永远指向当天**第一次**上传的那份。
  所以 data.json 里的图片 URL 必须是 `uploaded_urls.json` 里的**真实 URL**，
  不能拼模板 —— 模板 URL 是 200 的，所有"CDN 可达性"检查都会通过，
  但内容是旧的。`db_save` 已经处理好了，别在别处再拼模板 URL。

## 加一天的标准动作

见 `prompt.md` 的 step 1-17。最小骨架：

```bash
source /Users/xiaoan/Documents/TimeTask/config/xhs.env.sh
cd ${TASK_XHS_DIR}
TODAY=$(date +%Y-%m-%d)

# 写 3 个内容文件 → build → 出图 → 肉眼核对 → 合成 → 上传 → 飞书 → 落库 → 导出
python3 scripts/build_data.py    $TODAY
python3 scripts/build_vs_data.py $TODAY
bash    scripts/gen_images.sh    $TODAY
python3 scripts/contact_sheet.py $TODAY     # ← 打开看
python3 scripts/compose_cards.py $TODAY
python3 scripts/upload_cloudimgs.py $TODAY
python3 scripts/feishu_push_optimized.py ${TASK_XHS_DIR}/output/$TODAY $TODAY
python3 scripts/db_save.py    $TODAY
VERSION=$(date +%s)
python3 scripts/db_export.py  $TODAY $VERSION
python3 scripts/validate_schema.py $TODAY

# 版本号 + push + 验证
bash scripts/push_with_probe.sh origin main
python3 scripts/verify_live.py $TODAY
```

## 改完怎么验证

```bash
python3 -m py_compile scripts/*.py          # 语法
python3 scripts/verify_live.py 2026-10-22   # 端到端 + 页面渲染断言
```

`verify_live.py` 的**页面渲染断言**用 Node + DOM stub 把线上 `index.html`
真跑一遍，断言渲染结果里真的有价格 / 详情 / 购买链接、统计栏有值、
版本徽章跟随 `DATA_VERSION`。
这一项专治"数据在但页面不显示"——2026-10-22 之前模板写 `p.priceRange` /
`p.description`，数据里却是 `p.price` / `p.desc`，字段对不上导致价格和详情
整块不渲染，而所有"检查文件存在"的脚本都发现不了。
