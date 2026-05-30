#!/bin/bash
# update-landing.sh — 从最新 xhs-product-push 输出更新落地页并推送 GitHub Pages
#
# 功能:
#   1. 解析商品信息（从 product_card.html 或已有的 product_N.jpg）
#   2. 裁剪全图为5张独立商品图（如尚未裁剪）
#   3. 逐张上传图床
#   4. 写入 data.json（每张商品独立 image URL）
#   5. 保存历史快照到 history/YYYY-MM-DD.json
#   6. 更新 history/history.json
#   7. 推送到 GitHub Pages
#
# 用法:
#   ./update-landing.sh                        # 自动找最新输出目录
#   ./update-landing.sh /path/to/output/日期   # 指定输出目录

set -e

# PIL 需要系统 Python（沙箱签名限制），JSON 处理用 managed Python
PYTHON_SYS=/usr/bin/python3
PYTHON=/Users/xiaoan/.workbuddy/binaries/python/envs/default/bin/python3
LANDING_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_FILE="$LANDING_DIR/data.json"
HISTORY_DIR="$LANDING_DIR/history"
HISTORY_INDEX="$HISTORY_DIR/history.json"
CDN_BASE="https://cloudimgs.231203.xyz"

# ===== 自动搜索最新 output 目录 =====
find_latest_output() {
  local latest=""
  local latest_date=""
  for dir in /Users/xiaoan/WorkBuddy/*/output/*/; do
    [ -d "$dir" ] || continue
    basename_dir=$(basename "$dir")
    if [[ "$basename_dir" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      if [[ "$basename_dir" > "$latest_date" ]]; then
        latest_date="$basename_dir"
        latest="$dir"
      fi
    fi
  done
  echo "$latest"
}

if [ -n "$1" ]; then
  OUTPUT_DIR="$1"
else
  OUTPUT_DIR=$(find_latest_output)
fi

if [ -z "$OUTPUT_DIR" ] || [ ! -d "$OUTPUT_DIR" ]; then
  echo "❌ 找不到输出目录，请确认 xhs-product-push 已执行过"
  echo "   或手动指定: $0 /path/to/output/YYYY-MM-DD"
  exit 1
fi

TODAY=$(basename "$OUTPUT_DIR")
echo "📂 输出目录: $OUTPUT_DIR (${TODAY})"

# ===== 步骤1: 解析商品信息 =====
PRODUCTS_JSON="[]"

# 方式A: 从 product_card.html 解析
if [ -f "$OUTPUT_DIR/product_card.html" ]; then
  echo "🔍 从 product_card.html 解析商品数据..."
  PRODUCTS_JSON=$($PYTHON -c "
import re, json

with open('$OUTPUT_DIR/product_card.html', 'r', encoding='utf-8') as f:
    html = f.read()

names = re.findall(r'class=\"product-name[^>]*>\s*([^<]+)', html)
cats = re.findall(r'class=\"product-category[^>]*>\s*([^<]+)', html)

# 提取标签：按 tags-wrap 分组，每组对应一个商品
all_tags_html = re.findall(r'class=\"tags-wrap[^>]*>(.*?)</div>', html, re.DOTALL)
product_tags = []
for sec in all_tags_html:
    tag_items = re.findall(r'class=\"(?:tag|tag-item|tag-pill|sp-tag)[^>]*>\s*([^<]+)', sec)
    if not tag_items:
        tag_items = re.findall(r'>([^<]+)</span>', sec)
    product_tags.append([t.strip() for t in tag_items])

products = []
for i, name in enumerate(names[:5]):
    p = {
        'name': name.strip(),
        'category': cats[i].strip() if i < len(cats) else '好物推荐',
        'tags': product_tags[i] if i < len(product_tags) else [],
        'image': ''
    }
    products.append(p)

print(json.dumps(products, ensure_ascii=False))
")
  PCOUNT=$(echo "$PRODUCTS_JSON" | $PYTHON -c "import sys,json; print(len(json.load(sys.stdin)))")
  echo "✅ 提取到 ${PCOUNT} 个商品"
fi

# 方式B: 如果没有 HTML，但已有裁剪图 product_1.jpg ~ product_5.jpg 或 product_card_1.jpg ~ product_card_5.jpg
if [ "$PRODUCTS_JSON" = "[]" ]; then
  HAS_CROPS=true
  for i in 1 2 3 4 5; do
    if [ ! -f "$OUTPUT_DIR/product_${i}.jpg" ] && [ ! -f "$OUTPUT_DIR/product_card_${i}.jpg" ]; then
      HAS_CROPS=false
      break
    fi
  done

  if [ "$HAS_CROPS" = true ]; then
    echo "📋 未找到 HTML，使用已有裁剪图 + 默认商品名"
    PRODUCTS_JSON='[{"name":"精选好物1","category":"好物推荐","tags":[],"image":""},{"name":"精选好物2","category":"好物推荐","tags":[],"image":""},{"name":"精选好物3","category":"好物推荐","tags":[],"image":""},{"name":"精选好物4","category":"好物推荐","tags":[],"image":""},{"name":"精选好物5","category":"好物推荐","tags":[],"image":""}]'
  fi
fi

# ===== 步骤2: 裁剪全图（如需） =====
CROP_DIR="$LANDING_DIR/.crop_tmp"

# 检查是否已有裁剪图（两种命名：product_N.jpg 或 product_card_N.jpg）
ALREADY_CROPPED=true
CROP_NAMES=""
for i in 1 2 3 4 5; do
  if [ -f "$OUTPUT_DIR/product_${i}.jpg" ]; then
    CROP_NAMES="product_${i}.jpg"
  elif [ -f "$OUTPUT_DIR/product_card_${i}.jpg" ]; then
    CROP_NAMES="product_card_${i}.jpg"
  else
    ALREADY_CROPPED=false
    break
  fi
done

# 找全图
FULL_IMAGE_PATH=""
for ext in jpg jpeg png; do
  if [ -f "$OUTPUT_DIR/product_card_full.$ext" ]; then
    FULL_IMAGE_PATH="$OUTPUT_DIR/product_card_full.$ext"
    break
  fi
done
if [ -z "$FULL_IMAGE_PATH" ]; then
  FULL_IMAGE_PATH=$(ls "$OUTPUT_DIR"/product_card_full* 2>/dev/null | head -1 || echo "")
fi

if [ "$ALREADY_CROPPED" = false ] && [ -n "$FULL_IMAGE_PATH" ] && [ -f "$FULL_IMAGE_PATH" ]; then
  echo "✂️  裁剪全图为 5 张独立商品图..."
  rm -rf "$CROP_DIR"
  mkdir -p "$CROP_DIR"

  $PYTHON_SYS -c "
from PIL import Image
import os

img = Image.open('$FULL_IMAGE_PATH')
w, h = img.size
chunk_h = h // 5
print(f'原图: {w}x{h}, 每张: {chunk_h}px')

for i in range(5):
    y1 = i * chunk_h
    y2 = (i + 1) * chunk_h if i < 4 else h
    crop = img.crop((0, y1, w, y2))
    out_path = f'$CROP_DIR/product_{i+1}.jpg'
    crop.save(out_path, 'JPEG', quality=95, optimize=True)
    print(f'  ✅ product_{i+1}.jpg ({crop.size[0]}x{crop.size[1]})')
"

  CROP_SOURCE="$CROP_DIR"
elif [ "$ALREADY_CROPPED" = true ]; then
  echo "✅ 已有裁剪图，跳过裁剪"
  CROP_SOURCE="$OUTPUT_DIR"
  # 确定裁剪图的实际命名模式
  if [ -f "$OUTPUT_DIR/product_1.jpg" ]; then
    CROP_PATTERN="product_%d.jpg"
  elif [ -f "$OUTPUT_DIR/product_card_1.jpg" ]; then
    CROP_PATTERN="product_card_%d.jpg"
  else
    CROP_PATTERN="product_%d.jpg"
  fi
elif [ -z "$FULL_IMAGE_PATH" ] || [ ! -f "$FULL_IMAGE_PATH" ]; then
  echo "⚠️  未找到全图文件，也没有已有裁剪图"
  CROP_SOURCE=""
fi

# ===== 步骤3: 逐张上传图床 =====
echo "☁️  逐张上传图床..."
URL_ARRAY="[]"

if [ -n "$CROP_SOURCE" ]; then
  IMAGE_URLS=""
  # 确定文件名模式
  if [ -z "$CROP_PATTERN" ]; then
    if [ -f "$CROP_SOURCE/product_1.jpg" ]; then
      CROP_PATTERN="product_%d.jpg"
    elif [ -f "$CROP_SOURCE/product_card_1.jpg" ]; then
      CROP_PATTERN="product_card_%d.jpg"
    else
      CROP_PATTERN="product_%d.jpg"
    fi
  fi
  for i in 1 2 3 4 5; do
    CROP_FILE=$(printf "$CROP_SOURCE/$CROP_PATTERN" $i)
    if [ -f "$CROP_FILE" ]; then
      UPLOAD=$(curl -s -m 60 -F "image=@$CROP_FILE" "$CDN_BASE/api/upload" 2>/dev/null || echo "")
      URL=$(echo "$UPLOAD" | $PYTHON -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('success') and d.get('data',{}).get('url'):
        url = d['data']['url']
        if url.startswith('/'):
            url = '$CDN_BASE' + url
        print(url)
    else:
        print('')
except:
    print('')
" 2>/dev/null || echo "")
      if [ -n "$URL" ]; then
        IMAGE_URLS="${IMAGE_URLS}${URL}\n"
        echo "  ✅ product_${i}.jpg → ${URL:0:70}..."
      else
        IMAGE_URLS="${IMAGE_URLS}\n"
        echo "  ❌ product_${i}.jpg 上传失败"
      fi
      sleep 0.5
    fi
  done

  URL_ARRAY=$(echo -e "$IMAGE_URLS" | grep -v '^$' | $PYTHON -c "
import sys, json
urls = [line.strip() for line in sys.stdin if line.strip()]
print(json.dumps(urls))
" 2>/dev/null || echo "[]")
  URL_COUNT=$(echo "$URL_ARRAY" | $PYTHON -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
  echo "✅ 上传完成: ${URL_COUNT}/5 张"
fi

# 清理临时裁剪目录
rm -rf "$CROP_DIR" 2>/dev/null || true

# ===== 步骤4: 计算累计数据 =====
if [ -f "$DATA_FILE" ]; then
  TOTAL_RUNS=$($PYTHON -c "
import json
with open('$DATA_FILE') as f:
    d = json.load(f)
print(d.get('totalRuns', 0))
")
else
  TOTAL_RUNS=0
fi
NEW_TOTAL=$((TOTAL_RUNS + 1))

# ===== 步骤5: 写入 data.json =====
# 用 Python 脚本写临时文件避免 shell 转义问题
$PYTHON -c "
import json, datetime, sys

products = json.loads('''$PRODUCTS_JSON''')
urls = json.loads('''${URL_ARRAY:-[]}''')

# 注入独立图片URL
for i, p in enumerate(products):
    if i < len(urls) and urls[i]:
        p['image'] = urls[i]

# 第一张URL作为全图兜底
first_url = urls[0] if urls else ''

data = {
    'totalRuns': $NEW_TOTAL,
    'totalProducts': $NEW_TOTAL * len(products),
    'lastRunDate': '$TODAY',
    'status': '运行中',
    'updateTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'products': products,
    'imageUrl': first_url
}

with open('$DATA_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'✅ data.json 已更新 (totalRuns={data[\"totalRuns\"]}, products={len(products)})')
"

# ===== 步骤6: 保存历史快照 =====
mkdir -p "$HISTORY_DIR"
cp "$DATA_FILE" "$HISTORY_DIR/${TODAY}.json"
echo "📸 历史快照已保存: history/${TODAY}.json"

# 更新历史索引
$PYTHON -c "
import json, os, glob

index = []
for f in sorted(glob.glob('$HISTORY_DIR/????-??-??.json')):
    try:
        with open(f) as fh:
            d = json.load(fh)
        date = os.path.basename(f).replace('.json', '')
        index.append({
            'date': date,
            'totalRuns': d.get('totalRuns', 0),
            'productCount': len(d.get('products', [])),
            'updateTime': d.get('updateTime', ''),
            'status': d.get('status', '')
        })
    except:
        pass

with open('$HISTORY_INDEX', 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f'✅ 历史索引已更新 ({len(index)} 条记录)')
"

# ===== 步骤7: 推送到 GitHub Pages =====
cd "$LANDING_DIR"
if [ -d ".git" ]; then
  echo "🔄 推送到 GitHub Pages..."
  git add data.json history/
  git commit -m "数据更新 $TODAY (第${NEW_TOTAL}次)" 2>/dev/null || echo "⚠️ 无变更，跳过提交"

  # 用 gh auth token 做 push（避免 502）
  TOKEN=$(gh auth token 2>/dev/null || echo "")
  if [ -n "$TOKEN" ]; then
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if echo "$REMOTE_URL" | grep -q "https://"; then
      PUSH_URL=$(echo "$REMOTE_URL" | sed "s|https://|https://${TOKEN}@|")
      git push "$PUSH_URL" main 2>&1 || echo "⚠️ 推送失败"
    else
      git push origin main 2>&1 || echo "⚠️ 推送失败"
    fi
  else
    git push origin main 2>&1 || echo "⚠️ 推送失败，请手动: cd $LANDING_DIR && git push origin main"
  fi
  echo "✅ 已推送，落地页约1分钟后更新"
  echo "🌐 https://where20.github.io/xhs-product-push/"
else
  echo "⚠️ 未找到 git 仓库，请手动推送"
fi

echo ""
echo "🎉 完成！"
