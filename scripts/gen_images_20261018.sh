#!/bin/bash
# gen_images_20261018.sh — 2026-10-18 5 商品 1:1 配图 (mmx image generate)
# 选品: 垆土铁棍山药 / JBL 便携蓝牙音箱 / 小米智能门锁 / 绽家洗衣凝珠 / 膳魔师保温杯
# ⚠️ 沿用 10/17 踩坑修复: 父 shell 仍 export HTTPS_PROXY/HTTP_PROXY=http://127.0.0.1:7897
#    (7897 无进程监听), mmx 继承后全部 code:6 Network request failed
#    修正: 显式 unset 代理变量 + 补 NO_PROXY, 直连 api.minimaxi.com 正常

unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy
export NO_PROXY="*"
export no_proxy="*"

set -u
OUT=/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-18/images
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

# 1. 莱阳秋月梨 — 秋冬润燥 应季水果 (注意: 最初选品是垆土铁棍山药,
#    后来换成秋月梨, prompt 已同步改, 否则图文不符)
gen 1 "Product photography of several ripe Chinese autumn pear fruits with golden yellow skin and faint russet speckles, classic round squat pear shape, one pear sliced in half showing crisp white juicy flesh and a small seed cavity, arranged in a natural still life on a rustic light wood table with a soft neutral linen cloth, a few water droplets on the skin, completely blank unbranded presentation, soft warm autumn afternoon daylight from a side window, minimalist fresh fruit product photography, no text, no logo, no watermark, no lettering, no packaging"

# 2. 便携蓝牙音箱 — IP67 防水 便携蓝牙音箱
gen 2 "Product photography of a compact portable bluetooth speaker in matte charcoal black with a rugged soft-touch protective bumper wrap, an oval pebble body with a metal woven mesh grille and a small integrated silicone carry loop, completely blank unbranded surface with no visible logos, floating at a three-quarter angle on a clean light grey studio backdrop, minimalist consumer electronics product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting with a gentle soft shadow"

# 3. 智能指纹门锁 — 半导体指纹智能门锁
gen 3 "Product photography of a modern smart fingerprint door lock in sleek dark bronze metallic finish, a tall slim rectangular lock panel with a clean black glass touch surface, a rounded numeric-less touch keypad area with no visible digits, a slim handle below, completely blank unbranded surface, mounted vertically at a three-quarter angle on a minimal pale grey door surface, minimalist smart home security product photography, no text, no logo, no watermark, no lettering, no numbers, no brand marks of any kind, soft diffused daylight with a gentle shadow"

# 4. 绽家香氛洗衣凝珠 — 四腔香氛洗衣凝珠
gen 4 "Product photography of a clear frosted translucent plastic jar filled with glossy translucent oval laundry detergent pods, soft pastel gradient colors inside the pods visible through the frosted wall, a plain matte cream cylindrical jar lid with a completely blank label area, a few pods resting beside the jar showing their layered multi-chamber structure, completely blank unbranded packaging, on a clean light grey studio surface, minimalist home care product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft bright diffused studio lighting"

# 5. 316不锈钢保温杯 — 渐变彩虹配色保温杯
gen 5 "Product photography of a sleek stainless steel insulated thermos bottle with a soft iridescent pastel gradient finish shifting between pale pink, mint and sky blue, a slim cylindrical body with a matte powder-coated texture and a matching one-touch flip lid, completely blank unbranded surface, standing upright on a clean light wood desk against a soft neutral beige wall, minimalist drinkware product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft bright morning daylight with a gentle natural shadow"

echo "=== done ==="
ls -la "$OUT"
