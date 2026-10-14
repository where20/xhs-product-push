#!/bin/bash
# gen_images_20261015.sh — 2026-10-15 5 商品 1:1 配图 (mmx image generate)
# 选品: 电动车挡风被 / SKG颈椎按摩仪 / CATLINK猫砂盆 / 唯尊天际登机箱 / 乐歌电动升降桌
# ⚠️ proxy 端口 7897 (10/13 踩坑: 6696 是死端口)
export HTTPS_PROXY=http://127.0.0.1:7897
export HTTP_PROXY=http://127.0.0.1:7897
set -u
OUT=/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-15/images
mkdir -p "$OUT"

gen() {
  local id="$1"; shift
  local prompt="$1"
  echo "🎨 generating product_${id} ..."
  if mmx image generate --prompt "$prompt" --aspect-ratio 1:1 --out "${OUT}/product_${id}.jpg" --quiet 2>&1; then
    if [ -f "${OUT}/product_${id}.jpg" ]; then
      echo "✅ product_${id}.jpg ($(du -k "${OUT}/product_${id}.jpg" | cut -f1)KB)"
    else
      echo "❌ product_${id}.jpg missing after generate"
    fi
  else
    echo "❌ product_${id} generate FAILED"
  fi
}

# 1. 电动车挡风被 — 深蓝灰加绒防水, 绝不带品牌 logo
gen 1 "Product photography of a folded winter handlebar windproof cover quilt for electric scooter, thick plush fleece-lined dark slate blue grey fabric with a water-repellent outer shell, a wide collar opening and a rounded side wing visible, completely unbranded, neatly folded on a clean light grey studio surface, minimalist commuter gear product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused studio lighting"

# 2. 颈椎按摩仪 — 深灰蓝 U 型环颈脉冲按摩器
gen 2 "Product photography of a modern U-shaped wearable neck massager device in matte deep slate grey blue with smooth rounded ergonomic curves, a slim control button panel visible on one side, completely blank unbranded surface, floating on a clean light grey studio background, minimalist wellness tech product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting with gentle shadow"

# 3. 自动猫砂盆 — 全封闭式白色圆角智能猫砂盆
gen 3 "Product photography of a large fully enclosed automatic self-cleaning cat litter box in matte warm white with soft rounded corners and a subtle translucent oval door on the front, minimalist cylindrical capsule form, completely unbranded, standing on a clean light wood floor against a pale neutral wall, minimalist smart pet appliance product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft bright natural daylight"

# 4. 20寸登机箱 — 奶茶色磨砂 PC 硬壳箱
gen 4 "Product photography of a single hardshell carry-on suitcase in soft matte milky tea beige with a subtle brushed texture, four quiet spinner wheels at the base, a clean telescopic handle housing on top and a smooth front shell with no visible seams, completely unbranded, standing upright three-quarter view on a clean light grey studio surface, minimalist travel luggage product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused studio lighting"

# 5. 电动升降桌 — 灰胡桃木纹桌面 + 白腿
gen 5 "Product photography of a modern height adjustable standing desk with a grey walnut wood grain rectangular desktop and slim white steel legs, clean minimal lines, completely unbranded surface, photographed in a bright minimal home office corner with soft window light, minimalist ergonomic furniture product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft natural daylight"

echo "=== done ==="
ls -la "$OUT"
