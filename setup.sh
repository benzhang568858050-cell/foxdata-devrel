#!/usr/bin/env bash
# foxdata-devrel 一键配置引导（新用户友好）
# 交互式创建凭据 + 安装依赖 + 校验
# 用法：bash setup.sh

export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
cd "$(dirname "$0")"

echo "=============================================="
echo "  FoxData API · DevRel Content Hub 配置向导"
echo "=============================================="
echo ""

# 1) Python 检查
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ 需要 Python 3.10+，请先安装: https://python.org"
  exit 1
fi
echo "✅ Python: $(python3 --version)"

# 2) 依赖安装
echo ""
echo "📦 安装依赖..."
python3 -m pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt 2>/dev/null
echo "✅ 依赖已安装"

# 3) 凭据配置（跳过已存在的）
mkdir -p config
echo ""
echo "🔑 凭据配置（已存在的将跳过）"

# Dev.to
if [ ! -f "config/devto_creds.json" ]; then
  echo ""
  echo "--- Dev.to（发布长文，免费）---"
  echo "获取: dev.to → Settings → Extensions → API Keys"
  read -rp "Dev.to API Key: " DEVTO_KEY
  if [ -n "$DEVTO_KEY" ]; then
    printf '{"api_key": "%s"}\n' "$DEVTO_KEY" > config/devto_creds.json
    echo "✅ 已保存 config/devto_creds.json"
  fi
fi

# X（可选）
if [ ! -f "config/x_cookies.json" ] && [ ! -f "config/x_creds.json" ]; then
  echo ""
  echo "--- X / Twitter（可选，跳过则按回车）---"
  echo "获取: Chrome 装 Cookie-Editor → 登录 x.com → 导出 cookies JSON"
  read -rp "X cookies 文件路径（留空跳过）: " X_COOKIE_PATH
  if [ -n "$X_COOKIE_PATH" ] && [ -f "$X_COOKIE_PATH" ]; then
    cp "$X_COOKIE_PATH" config/x_cookies.json
    echo "✅ 已保存 config/x_cookies.json"
  fi
fi

# Hashnode（可选）
if [ ! -f "config/hashnode_creds.json" ]; then
  echo ""
  echo "--- Hashnode（可选，跳过则按回车）---"
  echo "获取: hashnode.com → Settings → Developer → Personal Access Tokens"
  read -rp "Hashnode PAT（留空跳过）: " HN_PAT
  if [ -n "$HN_PAT" ]; then
    read -rp "publication_id（博客设置页 URL 中的 ID）: " HN_PUB
    if [ -n "$HN_PUB" ]; then
      printf '{\n  "pat": "%s",\n  "publication_id": "%s"\n}\n' "$HN_PAT" "$HN_PUB" > config/hashnode_creds.json
      echo "✅ 已保存 config/hashnode_creds.json"
    fi
  fi
fi

# FoxData API（可选）
if [ ! -f "config/foxdata_creds.json" ]; then
  echo ""
  echo "--- FoxData Open API（可选，付费订阅后填）---"
  read -rp "x_openapi_key（留空跳过）: " FD_KEY
  if [ -n "$FD_KEY" ]; then
    printf '{"x_openapi_key": "%s"}\n' "$FD_KEY" > config/foxdata_creds.json
    echo "✅ 已保存 config/foxdata_creds.json"
  fi
fi

# 4) 校验
echo ""
echo "🧪 校验..."
if [ -f "config/devto_creds.json" ]; then
  python3 -c "from clients.devto_client import verify; verify()" 2>/dev/null || echo "⚠️ Dev.to 校验失败（网络或凭据问题）"
fi

# 5) 下一步
echo ""
echo "=============================================="
echo " ✅ 配置完成！下一步："
echo "     python3 auto.py            # 拉数据 → 计划 → 发布"
echo "     python3 auto.py devto-ops  # AI 运营引擎"
echo "     python3 auto.py status     # 查看状态"
echo "=============================================="
