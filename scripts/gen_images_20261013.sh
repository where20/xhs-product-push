#!/bin/bash
# gen_images_20261013.sh — 2026-10-13 5 商品 1:1 配图 (mmx image generate)
# 选品: 迪卡侬冲锋衣 / Amazfit 智能手表 / 九阳破壁机 / 格力除湿机 / 欧莱雅面霜
set -u
OUT=/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-13/images
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

gen 1 "Product photography of a dark forest green waterproof hardshell hiking jacket with a matte finish, fully zipped, laid flat on a clean light grey stone surface with the hood down, subtle water droplets beading on the shoulder panel, minimalist outdoor technical apparel e-commerce product shot, no text, no logo, no watermark, no lettering, soft diffused studio lighting, neutral clean background"
gen 2 "Product photography of a round black smartwatch with a dark metal case, black silicone sport band, and a clean blank AMOLED display face with no numbers, placed at a slight angle on a smooth dark grey surface, minimalist wearable technology product photography, no text, no logo, no watermark, no lettering, soft studio lighting with subtle rim light"
gen 3 "Product photography of a modern white and light purple countertop blender with a transparent glass pitcher filled with smooth fresh soybean milk, standing on a clean white kitchen counter with soft morning light, minimalist kitchen appliance product photography, no text, no logo, no watermark, no lettering, clean bright background"
gen 4 "Product photography of a tall white portable dehumidifier unit with a digital display panel and air outlet grille, standing on a clean light grey floor in a bright minimal room, minimalist home appliance product photography, no text, no logo, no watermark, no lettering, soft even studio lighting"
gen 5 "Product photography of a round frosted glass cosmetic cream jar in warm golden amber tone with a cream-colored lid, closed and centered on a clean beige marble surface with a soft folded silk cloth beside it, luxurious skincare product photography, no text, no logo, no watermark, no lettering, soft warm natural daylight"
