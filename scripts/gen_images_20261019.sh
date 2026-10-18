#!/bin/bash
# gen_images_20261019.sh — 2026-10-19 5 商品 1:1 配图 (mmx image generate)
# 选品: 飞利浦发热披肩 / 玖慕山羊绒围巾 / 京东京造纯钛炒锅 / 京东京造扫把簸箕 / 米家智能晾衣机
# ⚠️ 沿用 10/17~10/18 踩坑修复: 父 shell 仍 export HTTPS_PROXY/HTTP_PROXY=http://127.0.0.1:7897
#    (7897 无进程监听), mmx 继承后全部 code:6 Network request failed
#    修正: 显式 unset 代理变量 + 补 NO_PROXY, 直连 api.minimaxi.com 正常
#
# ⚠️ 10/18 踩坑 #2: 选品中途换 SKU 后 prompt 没同步 → 图文不符
#    本次出图后必须肉眼核对切片, 确认 5 张图与 data.json 的 5 个商品名一一对应

unset HTTPS_PROXY HTTP_PROXY https_proxy http_proxy
export NO_PROXY="*"
export no_proxy="*"

set -u
OUT=/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-19/images
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

# 1. 飞利浦小云肩 Air 加热披肩 — 石墨烯速热 可机洗 附充电宝
gen 1 "Product photography of a folded electric heating shoulder shawl in warm camel brown, a soft plush fleece throw draped in a neat neat stack with its detachable wired heating controller and a slim dark grey power bank placed beside it, completely blank unbranded fabric with no visible logos or tags, on a clean light beige studio surface, minimalist home appliance product photography, no text, no logo, no watermark, no lettering, no brand marks of any kind, soft even studio lighting with a gentle soft shadow"

# 2. 玖慕 100%小山羊绒围巾 — 驼咖格渐变晕染
gen 2 "Product photography of a luxurious folded cashmere scarf in a warm camel and coffee brown gradient plaid pattern, showing the soft fuzzy cashmere fiber texture and delicate drape, the scarf loosely coiled into an elegant S-fold on a clean light grey studio backdrop, completely blank unbranded with no visible logos, no fringes labels or tags, minimalist luxury textile product photography, no text, no logo, no watermark, no lettering, soft diffused studio light with a gentle soft shadow"

# 3. 京东京造 纯钛炒锅 32cm — 0涂层 不锈钢/钛质轻量炒锅
gen 3 "Product photography of a modern lightweight pure titanium wok pan with a matte silvery grey brushed metal interior and a slim matte black handle, sitting on a clean light grey studio surface at a three-quarter angle, the wide shallow bowl showing a smooth completely coating-free metallic cooking surface, a plain glass lid resting slightly tilted beside it, completely blank unbranded with no visible logos or text, minimalist premium cookware product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

# 4. 京东京造 可折叠扫把簸箕套装 — 加密梳齿 不粘头发
gen 4 "Product photography of a household cleaning broom and dustpan set, a dark teal green broom with dense soft bristles standing upright beside a matching dustpan with fine comb teeth along its edge, the dustpan handle visibly foldable, arranged neatly on a clean light studio surface against a soft neutral background, completely blank unbranded plastic with no visible logos or text, minimalist utility home cleaning product photography, no text, no logo, no watermark, no lettering, soft even studio lighting with a gentle soft shadow"

# 5. 米家智能晾衣机 3 — 隐形电动晾衣架 四分区 42寸灯板
gen 5 "Product photography of a modern ceiling mounted electric clothes drying rack in clean white matte finish, with a wide slim rectangular housing and a long horizontal bar with several evenly spaced hanging hooks and clips, a large flush rectangular LED light panel integrated into the housing, mounted against a clean white balcony ceiling at a slight upward angle, completely blank unbranded with no visible logos or text, minimalist smart home appliance product photography, no text, no logo, no watermark, no lettering, soft bright even studio lighting with a gentle soft shadow"

echo ""
echo "=== 出图结果 ==="
ls -la "$OUT"
