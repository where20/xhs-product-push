#!/bin/bash
# gen_images_20261012.sh — 2026-10-12 5 商品 1:1 配图 (mmx image generate)
set -u
OUT=/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-12/images
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

gen 1 "Product photography of a matte kraft-paper stand-up pouch bag of freeze-dried cat food with a blank label area, several golden freeze-dried chicken cubes scattered neatly in front, on a clean light beige surface, minimalist pet food e-commerce product shot, no text, no logo, no watermark, no lettering, soft diffused studio lighting"
gen 2 "Product photography of a set of transparent vacuum compression storage bags with white sealing strips and a small round silicone one-way air valve, one bag compressed holding a folded grey winter quilt, neatly stacked on a clean white closet shelf, minimalist home storage product photography, no text, no logo, no watermark, soft even studio lighting"
gen 3 "Product photography of a neatly folded women's thermal underwear set in warm beige and soft cream color, soft knit vest style top folded neatly on a clean white surface with a small cardigan beside it, autumn winter thermal base layer apparel product photography, no text, no logo, no watermark, no lettering, soft warm natural daylight"
gen 4 "Product photography of a large black tarp camping canopy set up outdoors on green grass, taut waterproof fabric stretched over foldable aluminum poles with guy lines, empty underneath, natural daylight and soft shadows, minimalist outdoor camping gear product photography, no text, no logo, no watermark, no lettering"
gen 5 "Product photography of a neat stack of clean soft white baby diapers with feather-soft surface texture, arranged in a small pile on a light pastel blue background, a single folded cotton baby onesie placed beside, minimalist baby care product photography, no text, no logo, no watermark, no lettering, soft diffused studio lighting"

echo "=== DONE ==="
ls -la "$OUT"