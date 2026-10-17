// gen_images_20261013.mjs
// 2026-10-13 5 个商品图 (国庆消费数据验证 + 深秋换季刚需:
// 迪卡侬冲锋衣 / Amazfit 智能手表 / 九阳破壁机 / 格力除湿机 / 欧莱雅面霜)
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = process.env.MMX_API_KEY;
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a dark forest green waterproof hardshell hiking jacket with a matte finish, fully zipped, laid flat on a clean light grey stone surface with the hood down, subtle water droplets beading on the shoulder panel, minimalist outdoor technical apparel e-commerce product shot, no text, no logo, no watermark, no lettering, soft diffused studio lighting, neutral clean background"
  },
  {
    id: 2,
    prompt: "Product photography of a round black smartwatch with a dark metal case, black silicone sport band, and a clean blank AMOLED display face with no numbers, placed at a slight angle on a smooth dark grey surface, minimalist wearable technology product photography, no text, no logo, no watermark, no lettering, soft studio lighting with subtle rim light"
  },
  {
    id: 3,
    prompt: "Product photography of a modern white and light purple countertop blender with a transparent glass pitcher filled with smooth fresh soybean milk, standing on a clean white kitchen counter with soft morning light, minimalist kitchen appliance product photography, no text, no logo, no watermark, no lettering, clean bright background"
  },
  {
    id: 4,
    prompt: "Product photography of a tall white portable dehumidifier unit with a digital display panel and air outlet grille, standing on a clean light grey floor in a bright minimal room, subtle water droplets and soft humidity haze suggested in the air, minimalist home appliance product photography, no text, no logo, no watermark, no lettering, soft even studio lighting"
  },
  {
    id: 5,
    prompt: "Product photography of a round frosted glass cosmetic cream jar in warm golden amber tone with a cream-colored lid, closed and centered on a clean beige marble surface with a soft folded silk cloth beside it, luxurious skincare product photography, no text, no logo, no watermark, no lettering, soft warm natural daylight"
  }
];

const OUT_DIR = '/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-13/images';
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
  if (!API_KEY) { console.error('❌ MMX_API_KEY not set'); process.exit(1); }
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
