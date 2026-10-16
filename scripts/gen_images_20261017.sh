#!/bin/bash
# gen_images_20261017.sh — 2026-10-17 5 商品 1:1 配图 (mmx image generate)
# 选品: 无雾空气加湿器 / 磁吸风镜骑行头盔 / 0涂层破壁机 / 剑麻布猫抓板 / 双温电热毯
# ⚠️ 10/17 踩坑: 父 shell 仍 export HTTPS_PROXY/HTTP_PROXY=http://127.0.0.1:7897
#    (7897 无进程监听), mmx 继承后全部 code:6 Network request failed
#    修正: 显式 unset 代理变量 + 补 NO_PROXY, 直连 api.minimaxi.com 正常

unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy
export NO_PROXY="*"
export no_proxy="*"

set -u
OUT=/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-17/images
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

# 1. 无雾空气加湿器 — 白色圆柱形冷蒸发无雾加湿器
gen 1 "Product photography of a modern ultrasonic-free evaporative humidifier in matte pure white, a clean slim cylindrical body with a softly rounded top and a small dark digital humidity display panel showing no characters, minimal minimalist design, completely blank unbranded surface, standing on a light wood bedside table against a soft warm beige wall, minimalist home appliance product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused morning daylight"

# 2. 磁吸风镜骑行头盔 — 米白色一体成型骑行头盔 带磁吸风镜
gen 2 "Product photography of a modern cycling safety helmet in matte cream off-white, a streamlined aerodynamic shell with integrated rear ventilation slots and a small dark tinted magnetic visor clipped to the front, thin clean strap system visible, completely blank unbranded surface, floating at a three-quarter angle on a clean light grey studio backdrop, minimalist sports equipment product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting with a gentle shadow"

# 3. 0涂层破壁机 — 深灰玻璃机身 破壁料理机
gen 3 "Product photography of a modern countertop blender in dark matte graphite grey, a tall cylindrical body with a thick clear glass jug on top, a slim control panel area with no visible buttons or characters, sturdy minimal base, completely blank unbranded surface, standing on a light wood kitchen counter against a pale neutral wall, minimalist kitchen appliance product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft bright natural daylight"

# 4. 剑麻布猫抓板 — 米色剑麻布平板猫抓板 猫窝一体
gen 4 "Product photography of a large flat oval cat scratching board wrapped in natural beige sisal rope fabric, a shallow concave surface with soft rounded edges and a subtle woven texture, completely blank unbranded with no patterns or prints, sitting on a clean light grey studio surface, minimalist pet product photography, no cats, no animals, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused daylight with a gentle shadow"

# 5. 双温双控电热毯 — 浅粉色折叠电热毯
gen 5 "Product photography of a neatly folded soft electric blanket in dusty rose pink, a thick quilted fabric surface with subtle stitched channel lines and a smooth wired controller cable resting beside the fold, no visible buttons or characters on the controller, completely blank unbranded surface, arranged on a clean light grey studio backdrop, minimalist home textile product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting"

echo "=== done ==="
ls -la "$OUT"
