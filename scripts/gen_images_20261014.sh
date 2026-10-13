#!/bin/bash
# gen_images_20261014.sh — 2026-10-14 5 商品 1:1 配图 (mmx image generate)
# 选品: 李宁羽毛球拍 / 恒源祥羊毛坐垫 / 爷爷的农场高铁米粉 / 公牛护眼台灯 / TATA加绒短靴
# ⚠️ proxy 端口 7897(10/13 踩坑: 6696 是死端口)
export HTTPS_PROXY=http://127.0.0.1:7897
export HTTP_PROXY=http://127.0.0.1:7897
set -u
OUT=/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-14/images
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

# 1. 羽毛球拍 — 绝不带品牌 logo (10/13 踩坑: 生成图带 THE NORTH FACE 标识)
gen 1 "Product photography of a single unbranded badminton racket with a matte carbon-black shaft and a plain white grip tape, no printed lettering on the frame, laid diagonally on a clean light grey studio surface, minimalist sports equipment e-commerce product shot, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft diffused studio lighting, neutral clean background"

# 2. 羊毛汽车坐垫 — 三件套
gen 2 "Product photography of a three-piece automotive seat cushion set in warm camel brown short-wool fleece fabric, main cushion, backrest pad and headrest pad neatly arranged side by side on a clean light grey surface, thick soft wool texture visible, minimalist car interior accessory product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft warm natural daylight"

# 3. 高铁米粉 — 有机大米米粉罐
gen 3 "Product photography of a cylindrical tin canister of infant rice cereal in soft matte cream and warm golden yellow color with a completely blank unlabelled lid and body, standing centered on a clean light wooden table with a small white ceramic bowl beside it, minimalist baby food product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft bright natural daylight"

# 4. 护眼台灯 — 白色国AA级台灯
gen 4 "Product photography of a modern white LED reading desk lamp with a curved crescent-shaped lamp head and a slim adjustable arm, plain unbranded matte white finish, switched on casting a soft neutral pool of light on a clean light wood desk surface, minimalist home lighting product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting"

# 5. 加绒短靴 — 小棕皮踝靴
gen 5 "Product photography of a pair of women's ankle boots in warm tan brown matte suede-like material with a low block heel and a plush fleece lining slightly visible at the collar, no buckle no logo, placed side by side on a clean beige neutral surface, minimalist autumn footwear product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft warm natural daylight"

echo "=== done ==="
ls -la "$OUT"