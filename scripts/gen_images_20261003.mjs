// gen_images_20261003.mjs
// 直接调用 minimaxi image API 绕开 mmx 网络问题
// 2026-10-03 5 个商品图 (国庆尾声+深秋换季: 取暖/寝具/桌面/宠物/滋补)
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = 'sk-cp-72DMgiCUOxy4bPYL8Qb5dpsEnMYRu_4UyisGPG-RllYcW-Gz6DGpBcXgheXyaqZ4zpdMMLhJ0mNjPOyYTMzXmzxv_S9P5x73GV0etEXJ_gnxiZJeG3r-drU';
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a large rechargeable hot water bag electric heating pouch, soft plush crystal velvet cover in warm coral pink grey, rounded oversized body for full bed coverage, discreet temperature control, lying flat on a clean light grey surface, cozy autumn winter heating appliance, no text, no logo, no watermark, soft even studio lighting, minimal e-commerce style"
  },
  {
    id: 2,
    prompt: "Product photography of a neatly folded pure cotton quilt batting inner duvet, bright white 100 percent cotton fabric, thick fluffy natural downy texture visible, four corner tie straps, stacked neatly on a minimal light beige background, autumn winter bedding textile product shot, no text, no logo, no watermark, soft natural studio lighting"
  },
  {
    id: 3,
    prompt: "Product photography of a black gas spring monitor arm desk mount, matte black powder coated steel arm with desk clamp base, VESA mounting plate, hidden cable management channel, single articulated arm holding a blank dark monitor, minimalist modern office desk setup, clean white background, no text, no logo, no watermark, soft studio lighting, industrial design e-commerce style"
  },
  {
    id: 4,
    prompt: "Product photography of a grey pet carrier backpack for cats, large transparent front window panel and mesh ventilation sides, padded structured soft interior, padded shoulder straps, standing on a clean light grey studio surface, premium modern pet travel accessory, no text, no logo, no watermark, soft even lighting"
  },
  {
    id: 5,
    prompt: "Product photography of freeze dried tremella white fungus silver ear fungus pieces in a clear glass bowl, pale ivory translucent dried fungus clusters, a small glass jar of white sugar rock candy beside it for scale, light warm wooden minimal background, autumn nourishing food ingredient, macro food product photography, no text, no logo, no watermark, soft natural lighting"
  }
];

const OUT_DIR = '/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-03/images';
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
  const files = fs.readdirSync(OUT_DIR).sort();
  for (const f of files) {
    const stat = fs.statSync(path.join(OUT_DIR, f));
    console.log(`  ${f}: ${(stat.size/1024).toFixed(1)}KB`);
  }
}

main().catch((e) => { console.error('FATAL:', e); process.exit(1); });