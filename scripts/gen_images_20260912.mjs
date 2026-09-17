// gen_images_20260912.mjs
// 直接调用 minimaxi image API 绕开 mmx 网络问题
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = 'sk-cp-72DMgiCUOxy4bPYL8Qb5dpsEnMYRu_4UyisGPG-RllYcW-Gz6DGpBcXgheXyaqZ4zpdMMLhJ0mNjPOyYTMzXmzxv_S9P5x73GV0etEXJ_gnxiZJeG3r-drU';
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a HUAWEI WATCH FIT 3 smartwatch in midnight black, 1.82-inch AMOLED display, 26g ultra-light body, fluoroelastomer strap, minimalist health and fitness design, modern tech wearable, e-commerce style, white background, no text, no watermark"
  },
  {
    id: 2,
    prompt: "Product photography of a JBL GO4 portable Bluetooth speaker in caramel black, 4.2W speaker, IP67 dustproof and waterproof, bluetooth 5.3 with AURACAST, integrated braided lanyard loop, fabric mesh grille, 7-hour battery life, compact pocket-sized design, minimalist e-commerce style, white background, no text, no watermark"
  },
  {
    id: 3,
    prompt: "Product photography of a KINGDOM K9 ultrasonic beauty device in soft pink, micro-current import and export, LED red light skin care, ultrasonic vibration technology, mini handheld facial massager, 175g lightweight portable, minimalist e-commerce style, white background, no text, no watermark"
  },
  {
    id: 4,
    prompt: "Product photography of an 8H H1 ergonomic memory foam pillow in mixed grey, three-curve cervical support design, 50D German BASF memory foam, removable washable CoolLite cool-feel cover with CleanCool antimicrobial inner cover, 50x30x10-7cm dimensions, minimalist e-commerce style, white background, no text, no watermark"
  },
  {
    id: 5,
    prompt: "Product photography of an AIRMATE HP21-K72 graphene ceramic heater in orange, 2100W high-tower dual-DC motor low-noise design, graphene far-infrared heating technology, multi-angle air supply with left-right swing, ABS flame-retardant material with tip-over protection, minimalist e-commerce style, white background, no text, no watermark"
  }
];

const OUT_DIR = '/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-12/images';
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
  for (const item of prompts) {
    process.stdout.write(`  [${item.id}/5] generating... `);
    try {
      const url = await genImage(item.prompt);
      const out = path.join(OUT_DIR, `product_${item.id}.jpg`);
      await downloadTo(url, out);
      const stat = fs.statSync(out);
      console.log(`✅ ${out} (${(stat.size/1024).toFixed(1)}KB)`);
    } catch (e) {
      console.log(`❌ ${e.message}`);
    }
  }
  console.log('=== 生成完成 ===');
  // List files
  const files = fs.readdirSync(OUT_DIR).sort();
  for (const f of files) {
    const stat = fs.statSync(path.join(OUT_DIR, f));
    console.log(`  ${f}: ${(stat.size/1024).toFixed(1)}KB`);
  }
}

main().catch((e) => { console.error('FATAL:', e); process.exit(1); });
