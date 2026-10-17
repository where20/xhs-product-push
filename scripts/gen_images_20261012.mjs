// gen_images_20261012.mjs
// 2026-10-12 5 个商品图 (深秋换季 + 双11 预售前夜: 冻干猫粮/真空压缩袋/德绒保暖内衣/黑胶露营天幕/纸尿裤)
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';

const API_KEY = process.env.MMX_API_KEY;
const HOST = 'api.minimaxi.com';

const prompts = [
  {
    id: 1,
    prompt: "Product photography of a matte kraft-paper stand-up pouch bag of freeze-dried cat food with a simple blank label area, several golden freeze-dried chicken cubes scattered neatly in front of the pouch, placed on a clean light beige surface, minimalist pet food e-commerce product shot, no text, no logo, no watermark, no lettering, soft diffused studio lighting, clean neutral background"
  },
  {
    id: 2,
    prompt: "Product photography of a set of transparent vacuum compression storage bags with white sealing strips and a small round silicone one-way air valve, one bag slightly compressed holding a folded grey winter quilt, neatly stacked on a clean white closet shelf, minimalist home storage product photography, no text, no logo, no watermark, soft even studio lighting"
  },
  {
    id: 3,
    prompt: "Product photography of a neatly folded set of women's thermal underwear in warm beige and soft cream color, a soft knit vest style top folded neatly on a clean white surface with a small cardigan beside it, autumn winter thermal base layer apparel product photography, no text, no logo, no watermark, no lettering, soft warm natural daylight"
  },
  {
    id: 4,
    prompt: "Product photography of a large black tarp camping canopy tent set up outdoors on green grass, taut waterproof fabric stretched over foldable aluminum poles with guy lines, empty underneath with natural daylight and soft shadows, minimalist outdoor camping gear product photography, no text, no logo, no watermark, no lettering"
  },
  {
    id: 5,
    prompt: "Product photography of a stack of clean soft white baby diapers with a gentle feather-soft surface texture, arranged neatly in a small pile on a light pastel blue background, with a single folded cotton baby onesie placed beside, minimalist baby care product photography, no text, no logo, no watermark, no lettering, soft diffused studio lighting"
  }
];

const OUT_DIR = '/Users/xiaoan/Documents/TimeTask/xhs-product-push/output/2026-10-12/images';
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