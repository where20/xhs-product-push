#!/usr/bin/env python3
"""
飞书推送脚本 - xhs-product-push 自动化任务
凭证从 ~/.minimax/credentials/general/feishu.json 加载 (camelCase 字段: appId / appSecret)
env.json 里 feishu.webhook_url 提供真实 webhook 地址

推送流程 (feishu-webhook.md):
  1. app credentials → tenant_access_token
  2. im/v1/images 上传每张图 → img_key
  3. 拼 interactive card (img_key 拼图)
  4. POST card 到 webhook
"""
import json, os, sys, glob, urllib.request, urllib.error

CRED_FILE = os.path.expanduser("~/.minimax/credentials/general/feishu.json")
ENV_FILE = "/Users/xiaoan/WorkBuddy/config/env.json"


def load_creds():
    if not os.path.exists(CRED_FILE):
        print(f"❌ 凭证文件不存在: {CRED_FILE}", file=sys.stderr)
        return None
    try:
        with open(CRED_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 凭证读取失败: {e}", file=sys.stderr)
        return None


def load_env():
    try:
        with open(ENV_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ env.json 读取失败: {e}", file=sys.stderr)
        return None


def get_token(app_id, app_secret):
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
        if data.get("code") != 0:
            raise RuntimeError(f"Token 失败: {data}")
        return data["tenant_access_token"]


def upload_image(token, img_path):
    fname = os.path.basename(img_path)
    boundary = f"----FormBoundary{os.urandom(16).hex()}"
    with open(img_path, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image_type"\r\n\r\n'
        f"message\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="image"; filename="{fname}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + img_data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/images",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read())
        if result.get("code") != 0:
            raise RuntimeError(f"上传失败 {fname}: {result}")
        return result["data"]["image_key"]


def build_card(image_keys, date_str, product_data=None):
    """构建飞书卡片：
    - 顶部：主商品图（单张 orig_product_N.jpg）
    - 中部：配置对比表（名称 / 价格 / 购买链接）
    - 底部：来源说明
    """
    elements = []

    # 图片（单商品）
    for fname in image_keys:
        elements.append({"tag": "img", "img_key": image_keys[fname]})

    # 配置对比
    if product_data:
        elements.append({"tag": "hr"})
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**📦 {product_data.get('name', '精选好物')}**\n_{product_data.get('subtitle', '')}_\n\n**📊 配置对比**"
            }
        })

        configs = product_data.get('configurations', [])
        for cfg in configs:
            cfg_tag = cfg.get('tag', '')
            rec_tag = ' ⭐ 推荐' if cfg.get('recommended') else ''
            price = cfg.get('price', '')
            orig = cfg.get('originalPrice', '')
            orig_str = f' ~~{orig}~~' if orig else ''
            specs = cfg.get('specs', {})
            spec_str = ' / '.join(f'{k}:{v}' for k, v in specs.items())
            links = cfg.get('links', {})

            link_parts = []
            if links.get('jd'):     link_parts.append(f'[京东购买]({links["jd"]})')
            if links.get('taobao'): link_parts.append(f'[淘宝购买]({links["taobao"]})')
            if links.get('pdd'):    link_parts.append(f'[拼多多]({links["pdd"]})')
            link_str = ' | '.join(link_parts)

            content = f"**{cfg.get('name', '')}**{rec_tag} {cfg_tag}\n"
            content += f"{price}{orig_str}\n"
            if spec_str: content += f"`{spec_str}`\n"
            if link_str: content += link_str
            content += "\n---\n"

            elements.append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": content.strip()}
            })
    else:
        # 无 data.json 时回退旧逻辑
        ordered = [f"orig_product_{i}.jpg" for i in range(1, 6)]
        for i, fname in enumerate(ordered):
            if fname in image_keys:
                elements.append({"tag": "img", "img_key": image_keys[fname]})
                if i < len(ordered) - 1:
                    elements.append({"tag": "hr"})

    elements.append({
        "tag": "note",
        "elements": [
            {"tag": "plain_text", "content": f"📅 {date_str} | AI选品推送 | xhs.220616.xyz"}
        ]
    })

    return {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"🎯 今日精选 · {date_str}"},
                "template": "blue"
            },
            "elements": elements
        }
    }


def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else None
    date_str   = sys.argv[2] if len(sys.argv) > 2 else None
    if not output_dir or not date_str:
        print("用法: feishu_push_optimized.py <output_dir> <date>")
        sys.exit(2)

    # 加载凭证
    creds = load_creds()
    if not creds:
        print("⚠️ 跳过飞书推送 (凭证缺失)")
        sys.exit(0)

    env_cfg = load_env()
    if not env_cfg:
        print("⚠️ 跳过飞书推送 (env.json 缺失)")
        sys.exit(0)

    # camelCase 兼容
    app_id = creds.get("appId") or creds.get("app_id", "")
    app_secret = creds.get("appSecret") or creds.get("app_secret", "")
    webhook_url = env_cfg.get("feishu", {}).get("webhook_url", "")

    if not app_id or not app_secret:
        print("⚠️ 跳过飞书推送 (app_id/secret 缺失)")
        sys.exit(0)

    if not webhook_url or "placeholder" in webhook_url.lower():
        print("⚠️ 跳过飞书推送 (webhook_url 为占位)")
        sys.exit(0)

    # 读取 data.json 拿 product info（单商品+多配置）
    product_data = None
    data_json_path = os.path.join(output_dir, "data.json")
    if os.path.exists(data_json_path):
        try:
            with open(data_json_path) as f:
                dj = json.load(f)
                product_data = dj.get("product")
                if product_data:
                    print(f"✅ 读取到精选商品: {product_data.get('name', '?')}")
                    print(f"   配置数: {len(product_data.get('configurations', []))}")
        except Exception as e:
            print(f"⚠️ data.json 读取失败: {e}")

    print(f"✅ 凭证有效,开始推送 {date_str} 的素材到飞书...")

    # Step 1: token
    print("  [1/4] 获取 tenant_access_token ...", end=" ", flush=True)
    token = get_token(app_id, app_secret)
    print(f"✅")

    # Step 2: 上传图片
    # 新结构：只上传精选商品的 orig_product_{id}.jpg
    # 旧结构回退：扫全部 orig_product_*.jpg
    image_keys = {}
    if product_data and product_data.get("id") and product_data.get("image"):
        # 新结构：单商品精准上传
        fname = product_data["image"]
        img_path = os.path.join(output_dir, fname)
        if os.path.exists(img_path):
            print(f"  [2/4] 上传精选图 {fname} ...", end=" ", flush=True)
            try:
                image_keys[fname] = upload_image(token, img_path)
                print(f"✅ img_key={image_keys[fname][:30]}...")
            except Exception as e:
                print(f"❌ {e}")
    else:
        # 旧结构回退：扫全部
        image_files = sorted(glob.glob(os.path.join(output_dir, "orig_product_*.jpg")))
        for img_path in image_files:
            fname = os.path.basename(img_path)
            print(f"  [2/4] 上传 {fname} ...", end=" ", flush=True)
            try:
                image_keys[fname] = upload_image(token, img_path)
                print(f"✅ img_key={image_keys[fname][:30]}...")
            except Exception as e:
                print(f"❌ {e}")

    if not image_keys:
        print("⚠️ 没有成功上传的图片,跳过推送")
        sys.exit(0)

    # Step 3: 拼卡
    print("  [3/4] 构建 interactive card ...", end=" ", flush=True)
    card = build_card(image_keys, date_str, product_data)
    print(f"✅")

    # Step 4: POST webhook
    print("  [4/4] POST 到飞书 webhook ...", end=" ", flush=True)
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(card).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            code = result.get("code", result.get("StatusCode"))
            if code == 0:
                print(f"✅ 飞书推送成功! StatusCode={code}")
            else:
                print(f"⚠️ 飞书返回: {result}")
    except Exception as e:
        print(f"❌ webhook POST 失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
