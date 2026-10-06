// gen_images_20261007.mjs
// 直接调用 minimaxi image API 绕开 mmx 网络问题
// 2026-10-07 5 个商品图 (国庆返程 + 双11开门红 + 深秋换季: 个护/厨房/运动/床品/美妆)
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = 'sk-cp-72DMgiCUOxy4bPYL8Qb5dpsEnMYRu_4UyisGPG-RllYcW-Gz6DGpBcXgheXyaqZ4zpdMMLhJ0mNjPOyYTMzXmzxv_S9P5x73GV0etEXJ_gnxiZJeG3r-drU';
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a modern white high-speed hair dryer with sleek matte body and gold accent ring, minimalist cordless styling, magnetic nozzle attachment placed beside it, standing upright on a clean light beige studio surface, premium beauty appliance industrial design e-commerce shot, no text, no logo, no watermark, soft even studio lighting, minimal background"
  },
  {
    id: 2,
    prompt: "Product photography of a red ceramic lightweight enamel cast iron casserole pot with two side handles and a matching lid, glossy vibrant red exterior, sitting on a clean light grey kitchen counter, warm autumn still life mood, cookware product photography, no text, no logo, no watermark, soft natural studio lighting"
  },
  {
    id: 3,
    prompt: "Product photography of a rolled out light blue TPE yoga mat with anti-slip textured surface, partially unrolled on a clean light wooden floor, soft morning light from window, minimal wellness home fitness atmosphere, sports equipment product photography, no text, no logo, no watermark, soft natural lighting"
  },
  {
    id: 4,
    prompt: "Product photography of a neatly folded set of grey cotton flannel bedding sheets, soft brushed texture visible, stacked folds on a clean minimal white surface, autumn winter home textile bedding product shot, cozy muted color palette, no text, no logo, no watermark, soft natural studio lighting"
  },
  {
    id: 5,
    prompt: "Product photography of a matte lip mud tint tube in warm terracotta brown color with a small applicator wand beside it, creamy blurred swatch on a clean neutral beige stone surface, minimalist K-beauty cosmetics product photography, macro detail, no text, no logo, no watermark, soft natural studio lighting"
  }
];

const OUT_DIR = '/Users/xiaoan/WorkBuddy/xhs-product-push/output/2026-10-07/images';
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