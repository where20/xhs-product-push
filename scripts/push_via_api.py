#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""push_via_api.py — 通过 GitHub Git Data API 推送 commit

背景 (2026-10-17 踩坑):
  github.com 的 HTTPS / git-upload-pack 在本机网络下超时 (Recv failure: Operation timed out),
  但 api.github.com / codeload / objects 全部可达, SSH 22 端口也能握手(只是本机公钥没在
  GitHub 注册, 且 token 缺 admin:public_key scope, 无法自动注册)。
  所以改走 Git Data API 建 commit —— 全程只用 api.github.com, 绕开被墙的 github.com。

用法: python3 scripts/push_via_api.py
"""

import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_OWNER = "where20"
REPO_NAME = "xhs-product-push"
API = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
ROOT = Path("/Users/xiaoan/Documents/TimeTask/xhs-product-push")
VERSION = sys.argv[2] if len(sys.argv) > 2 else ""
TODAY = sys.argv[1] if len(sys.argv) > 1 else ""

FILES = [
    ".last_version",
    "data.json",
    "vs-data.json",
    "index.html",
    f"history/{TODAY}.json",
    "history/history.json",
    f"memory/{TODAY}.md",
    f"output/{TODAY}/data.json",
    f"output/{TODAY}/vs-data.json",
    f"output/{TODAY}/uploaded_urls.json",
    f"output/{TODAY}/product_card_full.jpg",
    f"output/{TODAY}/product_slice_1.jpg",
    f"output/{TODAY}/product_slice_2.jpg",
    f"output/{TODAY}/product_slice_3.jpg",
    f"output/{TODAY}/product_slice_4.jpg",
    f"output/{TODAY}/product_slice_5.jpg",
    f"output/{TODAY}/images/product_1.jpg",
    f"output/{TODAY}/images/product_2.jpg",
    f"output/{TODAY}/images/product_3.jpg",
    f"output/{TODAY}/images/product_4.jpg",
    f"output/{TODAY}/images/product_5.jpg",
    "scripts/validate_schema.py",
]


def collect_files(today: str, version: str) -> list:
    """当天产物 + 当天生成的脚本 + (若有)版本化路径"""
    ymd = today.replace("-", "")
    files = [
        ".last_version", "data.json", "vs-data.json", "index.html",
        f"history/{today}.json", "history/history.json",
        f"memory/{today}.md",
        f"output/{today}/data.json",
        f"output/{today}/vs-data.json",
        f"output/{today}/uploaded_urls.json",
        f"output/{today}/product_card_full.jpg",
        f"scripts/validate_schema.py",
    ]
    files += [f"output/{today}/product_slice_{i}.jpg" for i in range(1, 6)]
    files += [f"output/{today}/images/product_{i}.jpg" for i in range(1, 6)]
    if version:
        files += [f"v/{version}/data.json", f"v/{version}/vs-data.json"]
    # 当天新建的脚本
    for pattern in (f"scripts/build_data_{ymd}.py", f"scripts/build_vs_data_{ymd}.py",
                    f"scripts/compose_cards_{ymd}.py", f"scripts/gen_images_{ymd}.sh"):
        if (ROOT / pattern).is_file():
            files.append(pattern)
    # 推送脚本自身也进仓 —— 万一本地机器丢了, 远端还留着怎么推
    for pattern in ("scripts/push_via_api.py", "scripts/push_via_api_20261017.py"):
        if (ROOT / pattern).is_file():
            files.append(pattern)
    # 去重并保持顺序
    seen, uniq = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def get_token():
    out = subprocess.run(
        ["git", "credential-osxkeychain", "get"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True,
    ).stdout
    for line in out.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("❌ 未能从 keychain 取到 GitHub token")


TOKEN = get_token()


def api(method, path, payload=None):
    """走 curl。payload 一律写临时文件再用 -d @file 传 ——
    大图 base64 后有 3MB+, 走 argv 会撞 ARG_MAX (OSError: Argument list too long)。"""
    cmd = [
        "curl", "-s", "--noproxy", "*", "-X", method,
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Accept: application/vnd.github+json",
        "--max-time", "180",
    ]
    tmp = None
    if payload is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(payload, tmp, ensure_ascii=False)
        tmp.close()
        cmd += ["-H", "Content-Type: application/json", "-d", f"@{tmp.name}"]
    cmd.append(API + path)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        if tmp is not None:
            os.unlink(tmp.name)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"❌ {method} {path} 非 JSON 响应: {r.stdout[:300]}")


def main():
    # 0. 连通性 sanity
    print(f"🚀 repo: {REPO_OWNER}/{REPO_NAME}")

    # 1. 当前 main 的 head commit
    ref = api("GET", "/git/ref/heads/main")
    if "object" not in ref:
        raise SystemExit(f"❌ 取 main ref 失败: {ref}")
    head_sha = ref["object"]["sha"]
    head_commit = api("GET", f"/git/commits/{head_sha}")
    base_tree = head_commit["tree"]["sha"]
    print(f"   HEAD = {head_sha[:12]}  base_tree = {base_tree[:12]}")

    # 2. 每个文件建 blob
    tree_entries = []
    missing = []
    for rel in collect_files(TODAY, VERSION):
        p = ROOT / rel
        if not p.is_file():
            missing.append(rel)
            continue
        raw = p.read_bytes()
        blob = api("POST", "/git/blobs", {
            "content": base64.b64encode(raw).decode(),
            "encoding": "base64",
        })
        if "sha" not in blob:
            raise SystemExit(f"❌ blob 失败 {rel}: {blob.get('message')}")
        tree_entries.append({
            "path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"],
        })
        print(f"   ✅ blob {rel} ({len(raw)//1024}KB) → {blob['sha'][:10]}")

    if missing:
        print(f"⚠️ 跳过缺失文件: {missing}")

    # 3. 以当前 tree 为 base 建新 tree (只含改动文件, 其余继承)
    tree = api("POST", "/git/trees", {"base_tree": base_tree, "tree": tree_entries})
    if "sha" not in tree:
        raise SystemExit(f"❌ tree 失败: {tree.get('message')}")
    print(f"   🌳 new tree = {tree['sha'][:12]}")

    # 4. 建 commit
    names = "、".join(p["name"].split()[0] for p in json.loads((ROOT / f"output/{TODAY}/data.json").read_text(encoding="utf-8"))["products"])
    msg = f"xhs-push: {TODAY} 商品图文 (5个精选商品: {names})"
    commit = api("POST", "/git/commits", {
        "message": msg, "tree": tree["sha"], "parents": [head_sha],
    })
    if "sha" not in commit:
        raise SystemExit(f"❌ commit 失败: {commit.get('message')}")
    new_sha = commit["sha"]
    print(f"   📝 new commit = {new_sha[:12]}")

    # 5. 快进 main ref
    upd = api("PATCH", "/git/refs/heads/main", {"sha": new_sha, "force": False})
    if "object" not in upd:
        raise SystemExit(f"❌ ref 更新失败: {upd.get('message')}")
    print(f"🎉 main 已更新到 {new_sha[:12]} ({len(tree_entries)} 个文件)")


if __name__ == "__main__":
    main()
