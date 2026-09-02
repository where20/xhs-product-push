# xhs-product-push 自动化任务 prompt 模板

## 任务
每天 07:00 cron 触发,跑「小红书商品图文带货」全流程,产出:
- 5 个当日精选商品详情图
- 飞书群卡片推送
- landing page 数据更新

## 必读
- `/Users/xiaoan/WorkBuddy/common.sh` 加载环境变量
- 凭证: `~/.minimax/credentials/general/feishu.json` (appId/appSecret, 真实)
- 图床: `cloudimgs.iepose.cn` POST /api/upload-file
- 历史参考: `memory/$(date -d yesterday +%Y-%m-%d).md` (昨天的执行日志)
- 9/02 bug 修复记录(必读!): `memory/2026-09-02.md` 末尾的"## 🐛 Bug 发现与修复"

## 14 步流程(严格按顺序)

**重要变更 (9/2 之后)**: 增加 SQLite 落库步骤。所有 cron 跑出的数据
必先写 SQLite (`xhs_push.db`),再从 db 导出 json 给 GitHub Pages。
SQLite 约束保证 `products.image` / `hotProducts.image` NOT NULL,
9/2 漏 image bug 不再发生。

### 1. 加载环境
```bash
source /Users/xiaoan/WorkBuddy/common.sh
echo "TASK_XHS_DIR=$TASK_XHS_DIR IMG_HOST_PRIMARY=$IMG_HOST_PRIMARY"
```

### 2. 读取任务 prompt 模板
```bash
cat ${TASK_XHS_DIR}/prompt.md  # 即本文件
```

### 3. 前置检查
- `${WORKBUDDY_CREDENTIALS_DIR}/${WORKBUDDY_FEISHU_CRED_FILE}` 存在(可选,缺失会跳过飞书推送)
- **`xhs_push.db` 已建表**:`python3 ${TASK_XHS_DIR}/scripts/db_init.py` (idempotent,不会重置数据)

### 4. 读昨日执行日志(避免选品重复)
```bash
ls -la ${TASK_XHS_DIR}/memory/ | tail -3
cat ${TASK_XHS_DIR}/memory/$(date -v-1d +%Y-%m-%d).md 2>/dev/null | grep -A 20 "今日精选商品"
```
提取近 5 天(在 history/ 里)所有 product name,选 5 个**不重复**的。

### 5. WebSearch 5 个今日热门商品关键词
- 秋季/开学季/9月/换季 主题
- 覆盖 5 大不同场景(不要全选数码/全选厨房)
- 价格 ¥10-500 区间(小红书带货主力价位)

### 6. **生成 data.json (schema 必填项,缺一不可!)**
```json
{
  "date": "YYYY-MM-DD",
  "totalProducts": 5,
  "products": [
    {
      "id": 1,
      "name": "完整商品名",
      "category": "品类标签",
      "price": "¥XX(规格·渠道)",
      "desc": "150-200 字真实描述(来源:web search)",
      "highlights": ["亮点1", "亮点2", "亮点3", "亮点4", "亮点5"],
      "tags": ["标签1", "标签2", "标签3", "标签4", "标签5"],
      "suitable": "适用人群",
      "price_note": "价格说明 + 渠道",
      "color": "#XXXXXX",
      "image": "https://cloudimgs.iepose.cn/api/images/YYYY-MM-DD_product_1.jpg",  ← 必填!
      "images": [                                                                 ← 必填!
        "https://cloudimgs.iepose.cn/api/images/YYYY-MM-DD_product_1.jpg",
        "https://cloudimgs.iepose.cn/api/images/YYYY-MM-DD_product_slice_1.jpg"
      ]
    }
  ]
}
```

**Schema 校验(写完后必跑,失败则 raise)**:
```python
import json
d = json.load(open(f'{OUT_DIR}/data.json'))
for p in d['products']:
    assert 'image' in p, f"❌ product {p['id']} 缺 image 字段"
    assert p['image'].startswith('https://'), f"❌ product {p['id']} image 必须 CDN URL"
    assert 'images' in p and len(p['images']) >= 1, f"❌ product {p['id']} 缺 images 数组"
print('✅ data.json schema 校验通过')
```

### 7. **生成 vs-data.json (schema 必填项)**
```json
{
  "date": "YYYY-MM-DD",
  "sources": ["来源1", "来源2", ...],   ← 真实搜索 URL/网站名,严禁编造
  "competitors": [
    {
      "product": "品类 价位段区间",
      "items": [
        {
          "name": "商品名",       ← 第 1 个是今日主推
          "price": "¥XX",
          "advantage": "核心优势",
          "jd_sales": "销量/排行",
          "color": "#XXXXXX",
          "image": "https://cloudimgs.iepose.cn/api/images/YYYY-MM-DD_product_1.jpg"  ← 主推商品必填!
        }
      ]
    }
  ],
  "hotProducts": [    ← 必填! 5 项,从 5 个主推商品衍生
    {
      "name": "商品名",
      "category": "品类",
      "price": "¥XX",
      "image": "https://...",          ← 必填!
      "sales": "销量/排行摘要",
      "platform": "京东自营/天猫旗舰"
    }
  ],
  "dataSource": "WebSearch 真实数据 · YYYY-MM-DD cron 自动化抓取",  ← 必填!
  "updateTime": "YYYY-MM-DD 07:30"  ← 必填!
}
```

### 8. mmx image generate 生成 5 张 1:1 纯商品图
- aspect-ratio 1:1
- prompt 风格: "Product photography of ..., minimalist e-commerce style, no text, no watermark"
- 输出到 `${TASK_XHS_DIR}/output/$(date +%Y-%m-%d)/images/product_{1-5}.jpg`

### 9. PIL 合成 5 卡片长图(基于 compose_cards_2026MMDD.py)
- 1080x3000 每卡 + 5 卡片 5 等份裁剪

### 10. **上传 6 张图到 cloudimgs**(关键:5 张纯图 + 5 张切片)
⚠️ **必须上传 5 张 product_{1-5}.jpg**(不只是 slice) — landing page 要用
```bash
python3 ${TASK_XHS_DIR}/scripts/upload_cloudimgs.py $(date +%Y-%m-%d)
# 上传: 1 full + 5 slice
# 追加: 5 product_{1-5}.jpg  → 1:1 纯图,landing page 渲染用
```

或扩展 upload_cloudimgs.py 让它也传 5 张 product_{1-5}.jpg。

### 11. **必跑:data.json + vs-data.json 加 image 字段**(脚本化)
如果第 8 步跑完后,data.json product 还没 image 字段,跑这个 Python 脚本补:
```python
import json
TODAY = "$(date +%Y-%m-%d)"
IMG_BASE = f"https://cloudimgs.iepose.cn/api/images/{TODAY}"
with open(f"output/{TODAY}/data.json", encoding="utf-8") as f:
    d = json.load(f)
for p in d["products"]:
    pid = p["id"]
    p["image"] = f"{IMG_BASE}_product_{pid}.jpg"
    p["images"] = [p["image"], f"{IMG_BASE}_product_slice_{pid}.jpg"]
with open(f"output/{TODAY}/data.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
# 同样补 vs-data.json
```

### 12. 飞书推送(可选,凭证缺失跳过)
```bash
python3 ${TASK_XHS_DIR}/scripts/feishu_push_optimized.py ${TASK_XHS_DIR}/output/$(date +%Y-%m-%d) $(date +%Y-%m-%d)
```
⚠️ 9/2 bug 修复后,build_card 不再硬编码 orig_product,会按 image_keys 实际 keys 排序。**build_card 后断言 img 元素数 == 上传成功数,空卡片会 raise**。

### 12.5 **落库 SQLite (新增,关键!)**
```bash
# 1. 写 db
python3 ${TASK_XHS_DIR}/scripts/db_save.py $(date +%Y-%m-%d)
# - 自动补全 LLM 漏的 image 字段(从 cloudimgs URL 模板)
# - 缺 hotProducts.image / sources 等字段会 raise
# - 幂等:同日重复跑会覆盖 (DELETE + INSERT)

# 2. 从 db 导出 json (兼容 GitHub Pages 静态 fetch)
python3 ${TASK_XHS_DIR}/scripts/db_export.py $(date +%Y-%m-%d)
# - 导出到 7 个位置:output/{date}/ + v/{VERSION}/ + 根目录 + history/{date}.json
# - 验证导出的 json 和原 json byte-identical (landing page 渲染不变)
```

### 12.6 **Schema 校验 (从 db 读)**
```bash
python3 ${TASK_XHS_DIR}/scripts/validate_schema.py $(date +%Y-%m-%d)
# - 必含:products.image, hotProducts.image, dataSource, updateTime
# - 失败 abort,不会发布坏数据
```

### 13. history 同步
```bash
TODAY=$(date +%Y-%m-%d)
cp ${TASK_XHS_DIR}/output/${TODAY}/data.json ${TASK_XHS_DIR}/history/${TODAY}.json
# 追加 history.json(读旧,加新条,totalRuns = 旧长度 + 1)
python3 -c "
import json
p = '${TASK_XHS_DIR}/history/history.json'
with open(p) as f:
    h = json.load(f)
h.append({
    'date': '${TODAY}',
    'totalRuns': len(h) + 1,
    'productCount': 5,
    'updateTime': '${TODAY} 07:30',
    'status': '运行中'
})
with open(p, 'w') as f:
    json.dump(h, f, ensure_ascii=False, indent=2)
"
```

### 14. 版本化路径 + bust 缓存
```bash
TODAY=$(date +%Y-%m-%d)
VERSION=$(date +%s)
# 1. 更新 index.html DATA_VERSION
sed -i '' "s/const DATA_VERSION = '[^']*'/const DATA_VERSION = '${VERSION}'/" "${TASK_XHS_DIR}/index.html"
sed -i '' "s/content=\"[^\"]*\" \/>/content=\"${VERSION}\" \/>/" "${TASK_XHS_DIR}/index.html" 2>/dev/null || true
# 2. 创建版本化路径(bust CDN 缓存)
mkdir -p "${TASK_XHS_DIR}/v/${VERSION}"
cp "${TASK_XHS_DIR}/output/${TODAY}/data.json" "${TASK_XHS_DIR}/v/${VERSION}/data.json"
cp "${TASK_XHS_DIR}/output/${TODAY}/vs-data.json" "${TASK_XHS_DIR}/v/${VERSION}/vs-data.json"
# 3. 根目录 fallback
cp "${TASK_XHS_DIR}/output/${TODAY}/data.json" "${TASK_XHS_DIR}/data.json"
cp "${TASK_XHS_DIR}/output/${TODAY}/vs-data.json" "${TASK_XHS_DIR}/vs-data.json"
```

### 15. git push
```bash
cd ${TASK_XHS_DIR}
git add output/$(date +%Y-%m-%d)/ history/$(date +%Y-%m-%d).json history/history.json data.json vs-data.json v/$(date +%s)/ index.html memory/$(date +%Y-%m-%d).md
git commit -m "xhs-push: $(date +%Y-%m-%d) 商品图文 (5个精选商品)"
git -c http.proxy= -c https.proxy= push origin main
```

### 16. 写 memory/$(date +%Y-%m-%d).md
记录: 执行时间 / 5 商品 / 选品来源 / 数据生成 / 工程产物 / Git 状态 / 下次触发

## 已知风险
- vs-data.json 价格/销量必须来自 web search,严禁编造
- history/{date}.json 必须每执行一次同步一份
- history.json 必须追加一条不覆盖
- git_proxy_push 可能因 GH_REPO_XHS_PUSH=null 失败,直接 `git -c http.proxy= -c https.proxy= push origin main` 绕过
- **必须上传 5 张 product_{1-5}.jpg(不只是 slice),否则 landing page 图全空**
- **data.json product 必含 image + images[] 字段,缺则 landing page "暂无图片"**
- **vs-data.json 必含 hotProducts + dataSource + updateTime 字段**

## Schema 校验(必跑,失败则 abort)
```python
import json
d = json.load(open(f"output/{TODAY}/data.json"))
for p in d["products"]:
    assert "image" in p, f"❌ product {p['id']} 缺 image"
    assert p["image"].startswith("https://"), f"❌ product {p['id']} image 必须 CDN URL"
vs = json.load(open(f"output/{TODAY}/vs-data.json"))
assert "hotProducts" in vs, "❌ vs-data.json 缺 hotProducts"
assert len(vs["hotProducts"]) == 5, "❌ hotProducts 必须 5 项"
assert "dataSource" in vs, "❌ vs-data.json 缺 dataSource"
assert "updateTime" in vs, "❌ vs-data.json 缺 updateTime"
for hp in vs["hotProducts"]:
    assert "image" in hp, f"❌ hotProducts 缺 image 字段"
print("✅ schema 校验通过")
```
