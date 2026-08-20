#!/usr/bin/env bash
# Hashnode 一键发布（本地执行，Windows/Mac/Linux 均可）
# 用法：把本脚本内容存为 run_hashnode.sh，执行 bash run_hashnode.sh

set -e
echo "=== Hashnode 一键发布 ==="

# 1) 拉取最新代码
if [ -d "foxdata-devrel" ]; then
  cd foxdata-devrel && git pull --rebase -q
else
  git clone -q https://github.com/benzhang568858050-cell/foxdata-devrel.git
  cd foxdata-devrel
fi

# 2) 依赖
python3 -m pip install -q requests 2>/dev/null || pip install -q requests

# 3) 凭据（已存在则跳过）
if [ ! -f "config/hashnode_creds.json" ]; then
  mkdir -p config
  cat > config/hashnode_creds.json <<'EOF'
{
  "pat": "b6797e73-9abc-4c7a-8c30-cb4c37eec95a",
  "publication_id": "6a86e7d681b62cc8b3d6ec93"
}
EOF
  echo "✅ 凭据已创建"
fi

# 4) 验证 + 发布
python3 -c "from clients.hashnode_client import verify; verify()" && echo "--- 开始发布 ---"
python3 daily_post.py

# 5) 状态回写
git add -A && git diff --cached --quiet || git commit -qm "sync: hashnode publish state"
git push -q && echo "✅ 状态已回写，完成！"
