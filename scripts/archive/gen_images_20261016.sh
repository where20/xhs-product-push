#!/bin/bash
# gen_images_20261016.sh — 2026-10-16 5 商品 1:1 配图 (mmx image generate)
# 选品: 纯色全棉四件套 / 高速负离子吹风机 / 免翻面空气炸锅 / 手提露营灯 / 热敷筋膜枪
# ⚠️ proxy 端口 7897 (10/13 踩坑: 6696 是死端口)
# ⚠️ 10/16 实测: 代理 7897 已下线, 直连 api.minimaxi.com 正常, 不要挂代理

set -u
OUT=/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-16/images
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

# 1. 纯色全棉四件套 — 雾霾蓝纯色床品, 绝不带品牌 logo / 文字
gen 1 "Product photography of a neatly folded plain solid dusty blue bedding set, a duvet cover stacked with two pillowcases and one flat sheet, all in a soft matte cotton texture with no pattern and no print, completely unbranded with a clean blank surface, arranged on a light grey studio backdrop, minimalist home textile e-commerce product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused natural daylight"

# 2. 高速负离子吹风机 — 石墨黑无刷电机吹风机
gen 2 "Product photography of a modern high-speed hair dryer in matte graphite black, sleek cylindrical body with a smooth handle, an attached concentrator nozzle, subtle metallic accent ring near the barrel, completely blank unbranded surface with no visible buttons text, standing upright on a clean light grey studio surface, minimalist beauty appliance product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting with a gentle shadow"

# 3. 免翻面空气炸锅 — 哑光米白圆角机身 + 可视窗
gen 3 "Product photography of a modern countertop air fryer in matte warm off-white with softly rounded corners, a large dark tinted viewing window on the front and a clean control dial area on top, minimalist capsule body, completely unbranded with a blank surface, standing on a light wood kitchen counter against a pale neutral wall, minimalist kitchen appliance product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft bright natural daylight"

# 4. 手提露营灯 — 橄榄绿金属质感手提灯
gen 4 "Product photography of a compact portable camping lantern in matte olive drab green metal finish, a rounded retro handle on top and a soft frosted glass light dome below, minimal cylindrical form, completely unbranded with a blank surface, sitting on a clean light grey studio surface, minimalist outdoor lighting product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused studio lighting with a warm glow"

# 5. 热敷筋膜枪 — 雾紫色枪型按摩器
gen 5 "Product photography of a modern handheld percussion massage gun in soft matte lavender purple, ergonomic rounded pistol-grip body with a smooth curved motor housing on top and a massage head attachment at the front, completely blank unbranded surface, lying on a clean light grey studio surface with a subtle soft shadow, minimalist wellness tech product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting"

echo "=== done ==="
ls -la "$OUT"
