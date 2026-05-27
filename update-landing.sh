#!/bin/bash
# update-landing.sh — xhs-product-push 执行后，更新落地页 data.json 并推送到 GitHub Pages
#
# 用法: ./update-landing.sh [输出目录]
# 例:   ./update-landing.sh /Users/xiaoan/WorkBuddy/output/2026-05-27
#
# 前置条件:
#   1. 已有 GitHub 仓库用于 GitHub Pages（默认 where20.github.io 下的 xhs-landing 子目录）
#   2. 已配置 git SSH key 或 token

set -e

# ===== 配置 =====
LANDING_DIR="/Users/xiaoan/WorkBuddy/2026-05-27-21-58-13/xhs-landing"
DATA_FILE="$LANDING_DIR/data.json"
OUTPUT_DIR="${1:-}"

if [ -z "$OUTPUT_DIR" ]; then
  echo "❌ 请传入输出目录参数"
  echo "用法: $0 /path/to/output/YYYY-MM-DD"
  exit 1
fi

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "❌ 输出目录不存在: $OUTPUT_DIR"
  exit 1
fi

echo "📂 输出目录: $OUTPUT_DIR"

# ===== 读取当前 data.json 中的 totalRuns =====
if [ -f "$DATA_FILE" ]; then
  TOTAL_RUNS=$(python3 -c "
import json
with open('$DATA_FILE') as f:
    d = json.load(f)
print(d.get('totalRuns', 0))
")
else
  TOTAL_RUNS=0
fi

NEW_TOTAL=$((TOTAL_RUNS + 1))

# ===== 提取日期 =====
TODAY=$(date +%Y-%m-%d)

# ===== 从 product_card.html 提取商品名称（简单解析） =====
PRODUCTS_JSON="[]"
if [ -f "$OUTPUT_DIR/product_card.html" ]; then
  PRODUCTS_JSON=$(python3 -c "
import re, json

with open('$OUTPUT_DIR/product_card.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 提取商品名称（匹配 HTML 中的商品标题）
names = re.findall(r'class=\"product-name[^>]*>([^<]+)', html)
if not names:
    names = re.findall(r'<h3[^>]*>([^<]+)', html)
if not names:
    names = ['商品1', '商品2', '商品3', '商品4', '商品5']

# 提取品类标签
tags = re.findall(r'class=\"(?:product-tag|sp-tag)[^>]*>([^<]+)', html)

products = []
for i, name in enumerate(names[:5]):
    p = {
        'name': name.strip(),
        'category': tags[i].strip() if i < len(tags) else '好物',
        'image': ''
    }
    # 查找对应图片
    img_pattern = f'product_{i+1}_001'
    products.append(p)

print(json.dumps(products, ensure_ascii=False))
")
fi

# ===== 生成新的 data.json =====
cat > "$DATA_FILE" << EOF
{
  "totalRuns": $NEW_TOTAL,
  "lastRunDate": "$TODAY",
  "status": "运行中",
  "updateTime": "$(date '+%Y-%m-%d %H:%M')",
  "products": $PRODUCTS_JSON
}
EOF

echo "✅ data.json 已更新 (totalRuns=$NEW_TOTAL)"

# ===== 推送到 GitHub Pages =====
cd "$LANDING_DIR"

if [ -d ".git" ]; then
  echo "🔄 推送到 GitHub Pages..."
  git add data.json
  git commit -m "更新运行数据 $TODAY" || echo "⚠️ 无变更，跳过提交"
  git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "⚠️ 推送失败，请手动推送"
  echo "✅ 推送完成"
else
  echo "⚠️ 未初始化 git，请先执行:"
  echo "   cd $LANDING_DIR"
  echo "   git init && git remote add origin https://github.com/where20/xhs-product-push.git"
  echo "   然后将落地页文件推送到 xhs-landing 子目录"
fi

echo "🎉 落地页数据更新完成！"
