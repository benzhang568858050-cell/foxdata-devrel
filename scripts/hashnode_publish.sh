#!/usr/bin/env bash
# Hashnode 每日自动发布（本地定时任务版）
# 兼容 cron 环境：显式 PATH、非交互 git、幂等（不会重复发布）
# 用法：bash run_hashnode.sh
# cron 示例：30 8 * * * bash /path/to/run_hashnode.sh >> /path/to/hashnode.log 2>&1

# cron 环境 PATH 兜底
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Hashnode 自动发布开始 ==="

WORK="$HOME/foxdata-devrel"
if [ ! -d "$WORK" ]; then
  git clone -q https://github.com/benzhang568858050-cell/foxdata-devrel.git "$WORK" || { echo "❌ clone 失败"; exit 1; }
fi
cd "$WORK" || exit 1

# 拉取最新（含新文章与状态）
git pull --rebase -q 2>/dev/null || echo "⚠️ pull 失败（网络？），继续用本地版本"

# 依赖
python3 -m pip install -q requests 2>/dev/null || pip3 install -q requests 2>/dev/null

# 凭据（幂等）
if [ ! -f "config/hashnode_creds.json" ]; then
  mkdir -p config
  printf '{\n  "pat": "b6797e73-9abc-4c7a-8c30-cb4c37eec95a",\n  "publication_id": "6a86e7d681b62cc8b3d6ec93"\n}\n' > config/hashnode_creds.json
  echo "✅ 凭据已创建"
fi

# 发布（幂等：按文件名去重，已发布自动跳过）
python3 daily_post.py || echo "⚠️ 发布过程有失败项（看上面日志）"

# 状态回写（有变化才提交）
git add -A
if ! git diff --cached --quiet; then
  git -c user.name="devrel-bot" -c user.email="devrel-bot@users.noreply.github.com" commit -qm "sync: hashnode publish state [$(date +%Y-%m-%d)]"
  if git push -q 2>/dev/null; then
    echo "✅ 状态已回写 GitHub"
  else
    echo "⚠️ push 失败：cron 环境需要 git 认证。"
    echo "   解决：执行一次 git config --global credential.helper store && git push（输一次密码）"
  fi
else
  echo "ℹ️ 无新发布，跳过提交"
fi

echo "=== 完成 [$(date '+%Y-%m-%d %H:%M:%S')] ==="
