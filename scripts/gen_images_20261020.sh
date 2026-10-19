#!/bin/bash
# gen_images_20261020.sh — 2026-10-20 5 商品 1:1 配图 (mmx image generate)
# 选品: 网易严选95白鹅绒羽绒被 / 沃隆每日坚果礼盒750g / 酷态科65W氮化镓充电器 /
#       蕉内小热皮302++儿童保暖内衣 / 洁碧WP-660台式冲牙器
# ⚠️ 沿用 10/17~10/19 踩坑修复: 父 shell export HTTPS_PROXY/HTTP_PROXY (6696/7897 均无监听),
#    mmx 继承后全部 code:6 → 显式 unset + NO_PROXY 直连
# ⚠️ 10/18 踩坑 #2: 出图后必须肉眼核对 contact sheet, 确认 5 图与 5 商品一一对应

unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy
export NO_PROXY="*"
export no_proxy="*"

set -u
OUT=/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-20/images
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

# 1. 网易严选 A类100支控温95%白鹅绒羽绒被 200×230 — 蓬松厚实 冬被
gen 1 "Product photography of a thick fluffy white goose down duvet comforter, pure bright white quilted cotton shell with soft horizontal stitching channels, generously lofted fluffy filling spilling softly from a slightly opened fold edge, folded into a neat tall stack on a clean light grey studio surface, completely blank unbranded bedding with no visible logos tags or labels, minimalist premium bedding product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

# 2. 沃隆 每日坚果礼盒 750g 混合口味 — 黄色硬盒 独立小袋
gen 2 "Product photography of a premium rectangular gift box of mixed daily nuts, warm golden yellow matte cardboard box shown closed and standing upright with a few small transparent individual snack sachets of nuts arranged neatly in front of it showing almonds cashews and walnut pieces, on a clean light beige studio surface, completely blank unbranded packaging with no visible logos text or labels, minimalist snack gift box product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

# 3. 酷态科 65W 氮化镓充电器 Type-C多口 — 白色小方块 三口 折叠插脚
gen 3 "Product photography of a tiny compact white gallium nitride fast charging adapter block with rounded corners and three visible ports on its face, two small oval Type-C ports and one rectangular USB-A port, plus a separate short white braided charging cable coiled neatly beside it, standing on a clean light grey studio surface at a three-quarter angle, completely blank unbranded plastic with no visible logos or text, minimalist consumer electronics accessory product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

# 4. 蕉内 小热皮302++ 儿童保暖内衣套装 7A抗菌 天空蓝 — 蓝白条纹套装
gen 4 "Product photography of a children's thermal underwear set, a sky blue and white fine striped long-sleeve top neatly folded on top of matching striped thermal leggings, showing a soft brushed cotton fleece inner texture and comfortable round neckline, arranged in a tidy flat lay stack on a clean light grey studio surface, completely blank unbranded with no visible logos tags or prints, minimalist kids apparel flat lay product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

# 5. 洁碧 WaterPik WP-660 台式冲牙器 — 白色立式大水箱
gen 5 "Product photography of a modern countertop water flosser oral irrigator, clean glossy white body with a large transparent water reservoir tank and a slim curved detachable nozzle resting in its holder on top, sitting on a clean light grey studio surface at a three-quarter angle showing the rounded compact base, completely blank unbranded appliance with no visible logos or text, minimalist bathroom oral care device product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

echo ""
echo "=== 出图结果 ==="
ls -la "$OUT"
