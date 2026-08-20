# Hashnode 本地发布指南

> 背景：沙箱与 GitHub Actions 共用出口代理，访问 `api.hashnode.com` 返回 TLS 421
> （Fastly 边缘证书不匹配，平台侧网络问题）。**你的本地网络不受影响**——用本指南在本地发布。

## 一次性准备（2 分钟）

```bash
git clone https://github.com/benzhang568858050-cell/foxdata-devrel.git
cd foxdata-devrel
python3 -m pip install requests
```

## 凭据（本地 config/ 目录，git 已忽略）

创建 `config/hashnode_creds.json`：

```json
{
  "pat": "b6797e73-9abc-4c7a-8c30-cb4c37eec95a",
  "publication_id": "6a86e7d681b62cc8b3d6ec93"
}
```

## 发布（日常操作）

```bash
# 方式一：发布所有到期文章到 Hashnode
git pull --rebase          # 先拉最新文章库
python3 daily_post.py      # 发布到期内容（Dev.to + Hashnode 自动判断）

# 方式二：仅验证 Hashnode 凭据
python3 -c "from clients.hashnode_client import verify; verify()"
# 预期输出：Hashnode 登录 OK：<名字>  📚 <博客>: <url>

# 方式三：只发某篇到 Hashnode
python3 - <<'EOF'
from clients.hashnode_client import publish_article
r = publish_article("content/articles/sea-app-market-watch.md", published=True)
print("已发布:", r["url"])
EOF
```

## 发布后同步状态

```bash
git add -A && git commit -m "sync: hashnode publish state" && git push
```

## 注意事项

- 每篇只发布一次（published.json 按文件名去重，跨环境防重）
- 文章库与 Dev.to 共用：Dev.to 已发的文章会在 Hashnode 首发时补发
- 如果要在 Hashnode 设置 canonical URL 指向 Dev.to（防 SEO 重复），后续可加
