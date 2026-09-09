// gen_images_20260910.mjs
// 直接调用 minimaxi image API 绕开 mmx 网络问题
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = 'sk-cp-72DMgiCUOxy4bPYL8Qb5dpsEnMYRu_4UyisGPG-RllYcW-Gz6DGpBcXgheXyaqZ4zpdMMLhJ0mNjPOyYTMzXmzxv_S9P5x73GV0etEXJ_gnxiZJeG3r-drU';
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a Hero brand Chinese style fountain pen gift box in matte black with gold embossed pattern, three pen tips (0.5mm fountain, 0.5mm ballpoint, 0.38mm extra fine), metal bookmark, blue-black ink cartridge, traditional Chinese cultural creative design, minimalist e-commerce style, white background, no text, no watermark"
  },
  {
    id: 2,
    prompt: "Product photography of a Level 8 (LEVEL8) brand 20-inch PC hardshell carry-on luggage in charcoal grey, German Covestro Makrolon triple-layer polycarbonate, signature yellow 8 logo, super silent 360 spinner wheels, TSA customs combination lock, YKK zipper, four-step adjustable aluminum-magnesium alloy telescopic handle, minimalist e-commerce style, white background, no text, no watermark"
  },
  {
    id: 3,
    prompt: "Product photography of a Mijia Xiaomi instant hot water dispenser S1 in pure white, ceramic heating technology, 3 second instant heating, 3 liter water tank, 1 degree precise temperature control, minimalist modern design, cup-sensing auto wake screen, child safety lock, white background, no text, no watermark"
  },
  {
    id: 4,
    prompt: "Product photography of a Wuyi Star brand Da Hong Pao (Big Red Robe) rock tea gift box in dark brown with gold embossed Chinese characters, 160 grams (8g x 20 small cans independent packaging), traditional Wuyi rock tea ceremony aesthetic, premium Chinese tea gift box, minimalist e-commerce style, white background, no text, no watermark"
  },
  {
    id: 5,
    prompt: "Product photography of a Supor brand 2026 new air fryer in cream white, 5.3L large capacity, zero fluorine titanium coated non-stick basket, steam-roast-fry all-in-one, dual heat source no-flip design, mechanical rotary knob control, minimalist modern kitchen appliance, white background, no text, no watermark"
  }
];

const OUT_DIR = '/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-09-10/images';
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
