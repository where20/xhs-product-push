#!/bin/bash
# push_with_probe.sh — 智能 push: 动态探测可用通道, 没有就直连, 直连不通就换可达 IP
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
# 2026-11-07 新增第三层: **直连 github.com:443 本身也可能被卡**
# ------------------------------------------------------------------
# 11-07 实测: 本机**没有任何代理端口在监听**(clash 只有特权 helper, 内核没跑),
# 直连 github.com → DNS 解析正常(20.205.243.166)但 TCP 443 75s 超时,
# 而 smzdm / cloudimgs / baidu 直连全是 200 → **只有 github.com 这条路被卡**。
# 同时发现:
#   - github.com:22 (SSH)  OPEN
#   - api.github.com:443   OPEN
#   - github.com 换别的 IP(140.82.112.3 / 140.82.113.3 / 140.82.114.3 …)→ **443 返回 200**
# → 解法: `git -c http.curloptResolve=github.com:443:<可达IP>` 让 git 指定走通的 IP。
#    (注意: 该选项在**走代理**时无效, 必须先 `-c http.proxy= -c https.proxy=` 关掉代理)
#
# 探测链(逐层降级, 每层都先 curl 探活再真 push, 避免 git 干等 75s 超时):
#   1. HTTP 代理候选(环境变量 + 常见本地端口) —— 端口有监听 且 经它访问 github.com 返回 200
#   2. 直连 —— curl --noproxy '*' 访问 github.com 返回 200
#   3. 直连 + 指定可达 IP —— 动态解析 github.com 的多个 A 记录, 逐个 --resolve 试, 用通的
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

# --- 探测: 直连 github.com ---
direct_ok() {
  local code
  code="$(curl --noproxy '*' -sS -o /dev/null -m 20 -w '%{http_code}' https://github.com/ 2>/dev/null)"
  [ "${code}" = "200" ]
}

# --- 探测: 直连 + 指定可达 IP ---
# 候选来源: 多个公共 DNS 解析出的 A 记录 + 一份常见 GitHub IP 兜底。
# 每个都用 curl --resolve 实测, 不盲信。
pick_ip() {
  local ips ip code
  ips=""
  for r in 1.1.1.1 8.8.8.8 223.5.5.5; do
    ips="$ips $(dig +short +time=3 +tries=1 "@${r}" github.com 2>/dev/null | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$')"
  done
  # 兜底: 已知常见的 GitHub A 记录(即使公共 DNS 不可达也能试)
  ips="$ips 140.82.112.3 140.82.113.3 140.82.114.3 140.82.116.3 140.82.121.3 20.233.83.145 20.27.177.113 20.200.245.247 20.29.134.23 172.182.252.133 20.250.119.67 140.82.121.4 140.82.112.4 140.82.113.4 140.82.114.4 20.205.243.166"
  for ip in $ips; do
    code="$(curl --noproxy '*' --resolve "github.com:443:${ip}" -sS -o /dev/null -m 12 -w '%{http_code}' https://github.com/ 2>/dev/null)"
    if [ "${code}" = "200" ]; then
      echo "${ip}"; return 0
    fi
  done
  return 1
}

# --- 核对远端 SHA(11-06 教训: 别只信 exit code, 推完必须核一次远端 ref) ---
# 用与 push **相同**的传输参数(代理 / 指定 IP), 否则 ls-remote 会自己撞上被卡的链路。
verify_remote_sha() {
  local local_sha remote_sha
  local_sha="$(git rev-parse HEAD 2>/dev/null)"
  remote_sha="$(git "$@" ls-remote "${REMOTE}" "${BRANCH}" 2>/dev/null | awk 'NR==1{print $1}')"
  if [ -n "${remote_sha}" ] && [ "${local_sha}" = "${remote_sha}" ]; then
    echo "🔏 远端 SHA 已核对一致: ${remote_sha}"
  elif [ -n "${remote_sha}" ]; then
    echo "⚠️  远端 SHA 与本地 HEAD 不一致! local=${local_sha} remote=${remote_sha}" >&2
  else
    echo "⚠️  未能读到远端 SHA(local=${local_sha}), 请手动核 git ls-remote" >&2
  fi
}

MODE=""        # proxy | direct | ip
PROXY=""
GIT_IP=""
GIT_EXTRA=()

if PROXY="$(pick_proxy || true)"; [ -n "${PROXY}" ]; then
  MODE="proxy"
  GIT_EXTRA=(-c "http.proxy=${PROXY}" -c "https.proxy=${PROXY}")
  echo "🔌 探测到可用代理: ${PROXY}"
elif direct_ok; then
  MODE="direct"
  GIT_EXTRA=(-c http.proxy= -c https.proxy=)
  echo "🔌 未探测到可用代理 → 直连推送"
elif GIT_IP="$(pick_ip || true)"; [ -n "${GIT_IP}" ]; then
  MODE="ip"
  # ⚠️ http.curloptResolve 只在**不走代理**时生效, 必须同时关掉代理
  GIT_EXTRA=(-c http.proxy= -c https.proxy= -c "http.curloptResolve=github.com:443:${GIT_IP}")
  echo "🔌 无代理且直连 github.com:443 不通 → 指定可达 IP 推送: ${GIT_IP}"
else
  echo "🔌 未探测到任何可用通道 → 直连推送(可能失败)" >&2
  MODE="direct"
  GIT_EXTRA=(-c http.proxy= -c https.proxy=)
fi

echo "   传输模式: ${MODE}"
git "${GIT_EXTRA[@]}" push "${REMOTE}" "${BRANCH}" 2>&1 | tee /tmp/xhs_push.log
PUSH_RC=${PIPESTATUS[0]}

# --- 判据: 必须有 main -> main 或 SHA 区间行 ---
#
# ⚠️ 2026-11-06 修正: 远端拒绝行本身含 "${BRANCH} -> ${BRANCH}" 字样:
#     ! [remote rejected] main -> main (fatal error in commit_refs_rules)
# 老逻辑用 grep -qE "${BRANCH} -> ${BRANCH}" 会把**拒绝**判成**成功**,
# 导致脚本 exit 0 而实际远端没更新(11-06 真实踩到: GitHub 瞬时故障, 推了 4 次全被拒,
# 脚本却连报 4 次 "✅ push 确认成功")。
# → 必须**先**判拒绝, 再判成功; 且成功行要求出现在行首的 SHA 区间/新分支格式上。
if grep -qE "remote rejected|! \[rejected\]|\[rejected\]|fatal error|error: failed to push" /tmp/xhs_push.log; then
  echo "❌ push 被远端拒绝(见上方 remote rejected / fatal error 行) —— 判定为未推送成功" >&2
  exit 1
fi
if grep -qE "^[[:space:]]*[0-9a-f]{7,}\.\.[0-9a-f]{7,}[[:space:]]+${BRANCH} -> ${BRANCH}|\*[[:space:]]+\[new branch\]" /tmp/xhs_push.log; then
  echo "✅ push 确认成功(见上方 SHA 区间行)"
  verify_remote_sha "${GIT_EXTRA[@]}"
  exit 0
fi
# "Everything up-to-date" = 远端已是最新, push 本身成功(没有 SHA 区间行是因为没东西可推)
if grep -qE "Everything up-to-date" /tmp/xhs_push.log; then
  echo "✅ push 成功(远端已是最新, 无需推送)"
  verify_remote_sha "${GIT_EXTRA[@]}"
  exit 0
fi
# 没有 SHA 区间行 → 多半是通道层失败(连不上), 不是远端业务拒绝。
# 直连失败时再试一次换 IP, 避免明天又卡在同一件事上。
if [ "${MODE}" = "direct" ] && [ "${PUSH_RC}" -ne 0 ]; then
  if GIT_IP="$(pick_ip || true)"; [ -n "${GIT_IP}" ]; then
    echo "🔁 直连失败 → 重试并指定可达 IP: ${GIT_IP}"
    git -c http.proxy= -c https.proxy= -c "http.curloptResolve=github.com:443:${GIT_IP}" \
      push "${REMOTE}" "${BRANCH}" 2>&1 | tee /tmp/xhs_push.log
    if ! grep -qE "remote rejected|! \[rejected\]|\[rejected\]|fatal error|error: failed to push" /tmp/xhs_push.log \
       && grep -qE "^[[:space:]]*[0-9a-f]{7,}\.\.[0-9a-f]{7,}[[:space:]]+${BRANCH} -> ${BRANCH}|\*[[:space:]]+\[new branch\]" /tmp/xhs_push.log; then
      echo "✅ push 确认成功(见上方 SHA 区间行)"
      exit 0
    fi
  fi
fi
echo "❌ 未见 '${BRANCH} -> ${BRANCH}' 或 SHA 区间行 —— 判定为未推送成功, 请排查" >&2
exit 1
