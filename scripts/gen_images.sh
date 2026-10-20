#!/bin/bash
# gen_images.sh — 通用版 (2026-10-21 起替代 gen_images_YYYYMMDD.sh 共 9 份)
#
# 用法:
#   bash scripts/gen_images.sh [YYYY-MM-DD]
#   # 默认今天; 也可用 XHS_DATE=2026-10-21
#
# 输入: output/{date}/image_prompts.json
#   {
#     "1": "Product photography of a ..., no text, no watermark",
#     "2": "...",
#     "3": "...",
#     "4": "...",
#     "5": "..."
#   }
#
# 输出: output/{date}/images/product_{1..5}.jpg  (1:1)
#
# ⚠️ 死代理: 父 shell 会 export HTTP_PROXY/HTTPS_PROXY (本机端口无监听),
#    mmx 继承后全部 code:6 Network request failed。
#    这里显式 unset + NO_PROXY 直连 —— 不要依赖"记住端口号",端口会变(7897→6696),
#    做法要对端口变化免疫。
unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy
export NO_PROXY="*"
export no_proxy="*"

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TODAY="${1:-${XHS_DATE:-$(date +%Y-%m-%d)}}"
OUT="${TASK_DIR}/output/${TODAY}/images"
PROMPTS="${TASK_DIR}/output/${TODAY}/image_prompts.json"

if [[ ! -f "${PROMPTS}" ]]; then
  echo "❌ 找不到 ${PROMPTS}" >&2
  echo "   需要先写当日出图提示词文件, 格式:" >&2
  echo '   {"1":"Product photography of ...","2":"...","3":"...","4":"...","5":"..."}' >&2
  exit 2
fi

mkdir -p "${OUT}"

# 用 python3 读 JSON, 避免 bash 解析 JSON 的引号/换行地狱
prompts="$(python3 -c '
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8"))
if isinstance(d,list):
    d={str(i+1):p for i,p in enumerate(d)}
for k in sorted(d, key=lambda x:int(x)):
    print(f"{k}\t{d[k]}")
' "${PROMPTS}")"

if [[ -z "${prompts}" ]]; then
  echo "❌ ${PROMPTS} 解析后为空" >&2
  exit 2
fi

ok=0; fail=0
while IFS=$'\t' read -r id prompt; do
  [[ -z "${id}" ]] && continue
  echo "🎨 generating product_${id} ..."
  if mmx image generate --prompt "${prompt}" --aspect-ratio 1:1 \
        --out "${OUT}/product_${id}.jpg" --quiet 2>&1; then
    if [[ -f "${OUT}/product_${id}.jpg" ]]; then
      echo "✅ product_${id}.jpg ($(du -k "${OUT}/product_${id}.jpg" | cut -f1)KB)"
      ok=$((ok+1))
    else
      echo "❌ product_${id}.jpg missing after generate"
      fail=$((fail+1))
    fi
  else
    echo "❌ product_${id} generate FAILED"
    fail=$((fail+1))
  fi
done <<< "${prompts}"

echo ""
echo "=== 出图结果: ${ok} 成功 / ${fail} 失败 ==="
ls -la "${OUT}"

# ⚠️ 10/18 踩坑 #2: 选品中途换 SKU 但 prompt 没同步 → 卡片写梨、配图是山药。
#    出图后必须肉眼核对(见 scripts/contact_sheet.py), 确认与 data.json 一一对应。
[[ ${fail} -gt 0 ]] && exit 1
exit 0
