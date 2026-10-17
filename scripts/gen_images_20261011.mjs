// gen_images_20261011.mjs
// 2026-10-11 5 个商品图 (深秋 + 双11预售前夜: 智能门锁/扫振牙刷/扫地机器人/开放式耳机/意式咖啡机)
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = 'sk-cp-72DMgiCUOxy4bPYL8Qb5dpsEnMYRu_4UyisGPG-RllYcW-Gz6DGpBcXgheXyaqZ4zpdMMLhJ0mNjPOyYTMzXmzxv_S9P5x73GV0etEXJ_gnxiZJeG3r-drU';
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a modern matte black smart door lock with a rounded rectangular body and a small camera lens at the top, brushed metal finish, standing on a clean light oak door surface, minimalist smart home security product shot, no text, no logo, no watermark, no lettering, soft diffused studio lighting, clean neutral background"
  },
  {
    id: 2,
    prompt: "Product photography of a slim white electric toothbrush with a small rectangular color display screen on the handle and a soft brush head, standing upright on a clean marble bathroom counter, a small water droplet beside it, minimal personal care appliance product photography, no text, no logo, no watermark, soft even studio lighting"
  },
  {
    id: 3,
    prompt: "Product photography of a white round robot vacuum cleaner with a raised lidar turret on top, glossy clean surface, placed on a light wood floor in a minimal living room, slight reflection on the floor, modern home appliance product photography, no text, no logo, no watermark, no lettering, soft natural daylight"
  },
  {
    id: 4,
    prompt: "Product photography of a pair of open-ear wireless earbuds with a curved ear hook design in soft matte cream color, resting on a smooth light grey stone surface, one earbud standing showing the slim profile, minimal tech audio accessory product photography, no text, no logo, no watermark, soft diffused studio lighting"
  },
  {
    id: 5,
    prompt: "Product photography of a compact stainless steel semi-automatic espresso coffee machine with a chrome and black finish, group head and steam wand visible, standing on a clean white kitchen counter, a small espresso cup with fresh crema beside it, minimal kitchen appliance product photography, no text, no logo, no watermark, soft warm morning light"
  }
];

const OUT_DIR = '/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-11/images';
fs.mkdirSync(OUT_DIR, { recursive: true });

function genImage(prompt) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      model: 'image-01',
      prompt: prompt,
      aspect_ratio: '1:1',
      response_format: 'url'
    });

    const options = {
      hostname: HOST,
      path: '/v1/image_generation',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(body);
          if (parsed.code !== 0 && parsed.base_resp?.status_code !== 0) {
            reject(new Error(`API error: ${body.slice(0, 300)}`));
            return;
          }
          const url = parsed.data?.image_urls?.[0];
          if (!url) { reject(new Error(`No URL in response: ${body.slice(0, 300)}`)); return; }
          resolve(url);
        } catch (e) { reject(e); }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return download(res.headers.location, dest).then(resolve).catch(reject);
      }
      const file = fs.createWriteStream(dest);
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve()));
    }).on('error', reject);
  });
}

(async () => {
  for (const item of prompts) {
    const dest = path.join(OUT_DIR, `product_${item.id}.jpg`);
    try {
      console.log(`🎨 生成图片 ${item.id}...`);
      const url = await genImage(item.prompt);
      await download(url, dest);
      const size = fs.statSync(dest).size;
      console.log(`✅ product_${item.id}.jpg (${Math.round(size / 1024)} KB)`);
    } catch (e) {
      console.error(`❌ product_${item.id} 失败: ${e.message}`);
      process.exitCode = 1;
    }
  }
  console.log('✅ 全部图片生成完成');
})();
