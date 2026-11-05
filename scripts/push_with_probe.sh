#!/bin/bash
# push_with_probe.sh — 智能 push: 动态探测可用代理, 没有就直连
#
# 用法:
#   bash scripts/push_with_probe.sh [remote] [branch]
#   bash scripts/push_with_probe.sh origin main
#
# 为什么需要它(2026-10-21 实测)
# ------------------------------
# 本机 HTTP_PROXY/HTTPS_PROXY 指向的端口**会变, 而且有时有监听、有时没有**:
#
#   10-17  端口 7897  无监听 → 必须绕过代理, 直连才能推
#   10-20  端口 6696  无监听 → 同上
#   10-21  端口 6696  **有监听**(clash-verge 在跑) → **绕过反而推不上去**:
#          github.com 直连 TCP 443 直接超时, 经 6696 代理 0.75s 返回 200
#
# 所以两条旧规则都不够用:
#   ❌ "记住端口号"          → 端口会变
#   ❌ "一律显式绕过代理"    → 代理活着的时候, 绕过 = 连不上
#   ✅ **先探测, 再决定**     → 本脚本就是这个
#
# 探测顺序:
#   1. 环境变量 HTTP_PROXY / HTTPS_PROXY —— 端口有监听 且 经它访问 github.com 返回 200
#   2. 常见本地代理端口 7897 / 7890 / 7891 / 1080 / 10808 / 10809 —— 同样要实际探活
#   3. 都没有 → 直连(不设 http.proxy)
#
# 判据(不要只看 exit code):
#   push 输出里必须有 `main -> main` 或 `<sha>..<sha>` 区间行,
#   否则视为没推上去(git add 坏 pathspec 时 commit/push 会"看起来成功"却啥也没推)。
set -u

REMOTE="${1:-origin}"
BRANCH="${2:-main}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 目标仓 = 当前目录所在 git 仓(优先, 这样父仓 TimeTask 也能直接复用本脚本);
# 当前目录不在 git 仓里时, 回退到脚本所在仓(xhs-product-push)。
if git rev-parse --git-dir >/dev/null 2>&1; then
  TASK_DIR="$(pwd)"
else
  TASK_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
fi

cd "${TASK_DIR}" || exit 1
echo "📁 目标仓: ${TASK_DIR} (${REMOTE}/${BRANCH})"

# --- 候选代理列表: 环境变量优先, 再加常见本地端口 ---
CANDIDATES=()
for v in "${HTTPS_PROXY:-}" "${HTTP_PROXY:-}" "${https_proxy:-}" "${http_proxy:-}"; do
  [ -n "${v}" ] && CANDIDATES+=("${v}")
done
for p in 7897 7890 7891 1080 10808 10809 6152 9090; do
  CANDIDATES+=("http://127.0.0.1:${p}")
done

# --- 探测: 端口有监听 + 经它访问 github.com 真能通 ---
pick_proxy() {
  local c hp host port code
  for c in "${CANDIDATES[@]}"; do
    hp="${c#*://}"; hp="${hp#*@}"; hp="${hp%%/*}"
    host="${hp%%:*}"; port="${hp##*:}"
    [ "${port}" = "${host}" ] && continue
    nc -z -G 2 "${host}" "${port}" >/dev/null 2>&1 || continue
    code="$(curl -x "${c}" -sS -o /dev/null -m 20 -w '%{http_code}' https://github.com/ 2>/dev/null)"
    if [ "${code}" = "200" ]; then
      echo "${c}"; return 0
    fi
  done
  return 1
}

PROXY="$(pick_proxy || true)"

if [ -n "${PROXY}" ]; then
  echo "🔌 探测到可用代理: ${PROXY}"
  git -c http.proxy="${PROXY}" -c https.proxy="${PROXY}" push "${REMOTE}" "${BRANCH}" 2>&1 | tee /tmp/xhs_push.log
else
  echo "🔌 未探测到可用代理 → 直连推送"
  git -c http.proxy= -c https.proxy= push "${REMOTE}" "${BRANCH}" 2>&1 | tee /tmp/xhs_push.log
fi

# --- 判据: 必须有 main -> main 或 SHA 区间行 ---
#
# ⚠️ 2026-11-06 修正: 远端拒绝行本身含 "${BRANCH} -> ${BRANCH}" 字样:
#     ! [remote rejected] main -> main (fatal error in commit_refs_rules)
# 老逻辑用 grep -qE "${BRANCH} -> ${BRANCH}" 会把**拒绝**判成**成功**,
# 导致脚本 exit 0 而实际远端没更新(今天真实踩到: GitHub 瞬时故障, 推了 4 次全被拒,
# 脚本却连报 4 次 "✅ push 确认成功")。
# → 必须**先**判拒绝, 再判成功; 且成功行要求出现在行首的 SHA 区间/新分支格式上。
if grep -qE "remote rejected|! \[rejected\]|\[rejected\]|fatal error|error: failed to push" /tmp/xhs_push.log; then
  echo "❌ push 被远端拒绝(见上方 remote rejected / fatal error 行) —— 判定为未推送成功" >&2
  exit 1
fi
if grep -qE "^[[:space:]]*[0-9a-f]{7,}\.\.[0-9a-f]{7,}[[:space:]]+${BRANCH} -> ${BRANCH}|\*[[:space:]]+\[new branch\]" /tmp/xhs_push.log; then
  echo "✅ push 确认成功(见上方 SHA 区间行)"
  exit 0
fi
echo "❌ 未见 '${BRANCH} -> ${BRANCH}' 或 SHA 区间行 —— 判定为未推送成功, 请排查" >&2
exit 1
