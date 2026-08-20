#!/usr/bin/env python3
"""Hashnode 客户端 —— 官方 GraphQL API 发布开发者长文（免费）。

凭据：config/hashnode_creds.json
    {"pat": "xxx", "publication_id": "yyy"}
- PAT：https://hashnode.com/settings/developer → Personal Access Tokens 生成
- publication_id：查询 me { publications { id } } 或博客设置页

用法：
    verify()          校验凭据（列出 publications）
    publish_article(path, published=True)  发布 content/articles/*.md
"""
import json
import sys
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from clients.devto_client import parse_frontmatter  # noqa: E402

CREDS_FILE = BASE_DIR / "config" / "hashnode_creds.json"
API = "https://api.hashnode.com"


def load_creds():
    if not CREDS_FILE.exists():
        return None
    return json.loads(CREDS_FILE.read_text())


def _gql(query, variables=None):
    creds = load_creds()
    if not creds:
        raise RuntimeError("未配置 Hashnode 凭据（config/hashnode_creds.json：pat + publication_id）")
    r = requests.post(
        API,
        json={"query": query, "variables": variables or {}},
        headers={"Authorization": f"Bearer {creds['pat']}", "Content-Type": "application/json"},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"Hashnode API 错误（{r.status_code}）：{r.text[:200]}")
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(f"Hashnode API 错误：{data['errors'][0].get('message', data['errors'][:1])}")
    return data.get("data", {})


def verify():
    """校验凭据并输出 publications 列表。"""
    q = """
    query {
      me {
        id name username
        publications(first: 10) { edges { node { id title url } } }
      }
    }
    """
    try:
        d = _gql(q)
        me = d.get("me", {})
        pubs = [e["node"] for e in (me.get("publications") or {}).get("edges", [])]
        print(f"Hashnode 登录 OK：{me.get('name')}（@{me.get('username')}）")
        for p in pubs:
            print(f"  📚 {p['title']}: {p['url']} (id={p['id']})")
        return bool(pubs)
    except Exception as e:
        print(f"Hashnode 校验失败：{e}")
        return False


def publish_article(path, published=True):
    """发布一篇长文到 Hashnode。返回 {id, url, title}。"""
    creds = load_creds()
    text = Path(path).read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    body = "\n".join(ln for ln in body.splitlines() if not ln.startswith("scheduled:"))

    tags = []
    for t in meta.get("tags", "").split(","):
        t = t.strip().lstrip("#")
        if t:
            tags.append({"name": t, "slug": t.lower().replace(" ", "-")})

    q = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post { id title slug url }
      }
    }
    """
    variables = {
        "input": {
            "title": meta.get("title", "Untitled"),
            "publicationId": creds["publication_id"],
            "contentMarkdown": body,
            "tags": tags[:5],
            "settings": {"isDelisted": not published},
        }
    }
    d = _gql(q, variables)
    post = d.get("publishPost", {}).get("post", {})
    return {"id": post.get("id"), "url": post.get("url"), "title": post.get("title")}


if __name__ == "__main__":
    verify()
