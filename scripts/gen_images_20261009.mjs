// gen_images_20261009.mjs
// 直接调用 minimaxi image API (绕开 mmx 网络问题, 与 20261007 同一模式)
// 2026-10-09 5 个商品图 (深秋换季 + 双11开门红前: 身体乳/纯钛电饭煲/越野跑鞋/充电宝/油汀取暖器)
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = 'sk-cp-72DMgiCUOxy4bPYL8Qb5dpsEnMYRu_4UyisGPG-RllYcW-Gz6DGpBcXgheXyaqZ4zpdMMLhJ0mNjPOyYTMzXmzxv_S9P5x73GV0etEXJ_gnxiZJeG3r-drU';
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a large matte pink squeeze tube of body lotion with a clean unlabeled cap, standing upright on a soft white cotton towel, a small amount of white cream swatch beside it, tiny water droplets suggesting moisturizing freshness, minimal e-commerce skincare body care product shot, no text, no logo, no watermark, no lettering, soft diffused studio lighting, clean neutral background"
  },
  {
    id: 2,
    prompt: "Product photography of a modern stainless steel rice cooker with a brushed metal body and glass lid, standing on a clean light wood kitchen counter, open lid revealing a shiny metal inner pot, a small bowl of freshly cooked white rice beside it, warm minimal kitchen appliance product photography, no text, no logo, no watermark, soft natural morning light"
  },
  {
    id: 3,
    prompt: "Product photography of a premium trail running shoe with aggressive deep lugged rubber outsole, dark green and black technical upper with protective toe cap, placed at a three-quarter angle on a rocky mountain trail surface, dramatic outdoor mountain light, rugged athletic footwear product photography, no text, no logo, no watermark, no lettering"
  },
  {
    id: 4,
    prompt: "Product photography of a slim silver power bank with a small colorful digital percentage display screen on its side and a short built-in cable, lying on a clean dark grey desk mat next to a laptop corner, one cable neatly coiled, minimal tech accessory product photography, no text, no logo, no watermark, soft even studio lighting"
  },
  {
    id: 5,
    prompt: "Product photography of a white multi-fin oil filled radiator heater standing against a clean white interior wall, gently glowing warm amber element visible between the fins, cozy warm room atmosphere with soft neutral sofa in the background, minimal home heating appliance product photography, no text, no logo, no watermark, soft warm ambient lighting"
  }
];

const OUT_DIR = '/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-09/images';
fs.mkdirSync(OUT_DIR, { recursive: true });

function genImage(prompt) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'image-01',
      prompt: prompt,
      aspect_ratio: '1:1',
      response_format: 'url',
      n: 1
    });
    const req = https.request({
      hostname: HOST,
      port: 443,
      path: '/v1/image_generation',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Length': Buffer.byteLength(data)
      },
      timeout: 90000
    }, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const j = JSON.parse(body);
            resolve(j.data?.image_urls?.[0]);
          } catch (e) {
            reject(new Error('parse fail: ' + body.substring(0, 200)));
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${body.substring(0, 200)}`));
        }
      });
    });
    req.on('error', (e) => reject(new Error(`req err: ${e.message} (${e.code})`)));
    req.on('timeout', () => { req.destroy(new Error('timeout 90s')); });
    req.write(data);
    req.end();
  });
}

function downloadTo(url, outPath) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 60000 }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadTo(res.headers.location, outPath).then(resolve, reject);
      }
      if (res.statusCode !== 200) {
        return reject(new Error(`download HTTP ${res.statusCode}`));
      }
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        fs.writeFileSync(outPath, Buffer.concat(chunks));
        resolve();
      });
      res.on('error', reject);
    }).on('error', reject);
  });
}

async function main() {
  console.log(`🚀 开始生成 5 张 1:1 商品图, 输出到 ${OUT_DIR}`);
  let ok = 0;
  for (const item of prompts) {
    process.stdout.write(`  [${item.id}/5] generating... `);
    try {
      const url = await genImage(item.prompt);
      const out = path.join(OUT_DIR, `product_${item.id}.jpg`);
      await downloadTo(url, out);
      const stat = fs.statSync(out);
      console.log(`✅ ${out} (${(stat.size/1024).toFixed(1)}KB)`);
      ok++;
    } catch (e) {
      console.log(`❌ ${e.message}`);
    }
  }
  console.log(`=== 生成完成 ${ok}/5 ===`);
  const files = fs.readdirSync(OUT_DIR).sort();
  for (const f of files) {
    const stat = fs.statSync(path.join(OUT_DIR, f));
    console.log(`  ${f}: ${(stat.size/1024).toFixed(1)}KB`);
  }
  if (ok !== 5) process.exit(1);
}

main().catch((e) => { console.error('FATAL:', e); process.exit(1); });