# scripts/archive/ — 历史脚本归档

## 为什么在这里

2026-10-21 之前，这个仓库里 **93 个"按日期生成"的脚本** 和 7 个稳定脚本混在一起：

```
compose_cards_20260817.py ~ compose_cards_20261020.py   35 份
build_data_20260906.py   ~ build_data_20261020.py        29 份
build_vs_data_20260906.py ~ build_vs_data_20261020.py    29 份
gen_images_2026*.sh / .mjs                               23 份
attach_cdn_urls_2026*.py                                  4 份
append_history_20260919.py                                1 份
push_via_api.py                                           1 份
compose_cards_20260817b.py / compose_20260827.py          2 份
```

问题不在于"文件多"，而在于 **样板被复制了 93 份**：

- `compose_cards_YYYYMMDD.py` —— 归一化日期后，**35 份里有 20+ 份完全一致**，
  只是一行 `TODAY = "..."` 不同。改一次排版要改 35 个文件 → 迟早漏改。
- `build_data_YYYYMMDD.py` —— 每份 220 行里，只有 `products` 列表是新的，
  剩下 ~40 行样板（`TODAY` / `OUT_DIR` / `IMG_BASE` / 断言 / `main`）逐字复制。
- **这类"复制样板"正是 2026-10-20 那次静默失败事故的温床**：
  cron prompt step 13 的 `git add` pathspec 写错（`history.json` 实际在 `history/` 下），
  整批 `add` 中止 → commit 报 "no changes added" → push 报 "Everything up-to-date"，
  **全链路看起来都成功，实际一个文件都没推上去**。样板越多，抄错的地方越多。

## 现在的做法：内容与代码分离

| | 每天变 | 长期不变 |
|---|---|---|
| 放在 | `output/{date}/products.json`<br>`output/{date}/vs.json`<br>`output/{date}/image_prompts.json` | `scripts/` 下的 13 个通用脚本 |
| 例子 | 5 个商品的名字/价格/描述/亮点/标签<br>竞品与来源<br>5 条出图 prompt | `build_data.py` / `build_vs_data.py`<br>`gen_images.sh` / `compose_cards.py` |

**每天只需要写 3 个纯数据文件，不用再写 250 行的 Python。**

```bash
python3 scripts/build_data.py     2026-10-21   # products.json      → data.json
python3 scripts/build_vs_data.py  2026-10-21   # vs.json            → vs-data.json
bash   scripts/gen_images.sh      2026-10-21   # image_prompts.json → images/product_1..5.jpg
python3 scripts/contact_sheet.py  2026-10-21   # 拼图核对(出图后必做)
python3 scripts/compose_cards.py  2026-10-21   # data.json          → 长图 + 5 切片
```

所有脚本都接受日期参数，默认今天；也支持 `XHS_DATE=2026-10-21`。

## 归档内容的处置

- **历史日期脚本** —— 保留以便回溯某天的排版/内容，但不再新增。
  回溯时：`python3 scripts/archive/compose_cards_20261019.py`（注意它内部写死了 `TODAY`）。
- **`attach_cdn_urls_*.py`** —— 已被 `build_data.py` / `build_vs_data.py` 完全取代
  （CDN URL 现在由脚本按模板生成，不再从 `uploaded_urls.json` 回填）。
- **`append_history_20260919.py`** —— 已被 `db_export.py` 取代
  （导出时会一并写 `history/{date}.json`；`history.json` 的追加由 `lib_xhs` 辅助脚本完成）。
- **`push_via_api.py`** —— **不要用**。它是 2026-10-17 代理故障时的临时绕行方案，
  走 Git Data API 建 commit 会造成本地与远端 SHA 分叉（内容相同但哈希不同），
  后续每次推送都变复杂。实测 github.com 直连可用（HTTP 200），
  正常用 `git -c http.proxy= -c https.proxy= push origin main` 即可。
  归档到此处也是为了让"别用它"这条指令更难被误触。

## 迁移前后的等价性验证（2026-10-21）

新流程用 `output/2026-10-20/` 的内容文件重建了当天的 `data.json` / `vs-data.json`，
与当天**已发布版本语义完全相等**（`data.json` 7 个位置 md5 全部 `2fbcc62e0997`，
`vs-data.json` 3 个位置 md5 全部 `a1a77d4d8f3d`），
`product_slice_3.jpg` 重合成后 **byte-identical**。
