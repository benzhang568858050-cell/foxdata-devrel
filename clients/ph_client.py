#!/usr/bin/env python3
"""Product Hunt 客户端 —— GraphQL API（v2）。

凭据：config/ph_creds.json  {"token": "xxx"}
Token 获取：https://www.producthunt.com/v2/oauth/applications 创建应用 → 生成 Developer Token
"""
import json
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CREDS_FILE = BASE_DIR / "config" / "ph_creds.json"
API = "https://api.producthunt.com/v2/api/graphql"


def load_token():
    if not CREDS_FILE.exists():
        raise RuntimeError("未配置 Product Hunt 凭据：config/ph_creds.json（token）")
    return json.loads(CREDS_FILE.read_text())["token"]


def _gql(query, variables=None):
    token = load_token()
    r = requests.post(
        API,
        json={"query": query, "variables": variables or {}},
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"PH API 错误（{r.status_code}）：{r.text[:300]}")
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(f"PH API 错误：{data['errors'][:2]}")
    return data.get("data", {})


def verify():
    q = "{ viewer { id name } }"
    try:
        data = _gql(q)
        v = data.get("viewer", {})
        print(f"Product Hunt 登录 OK：{v.get('name')}（id={v.get('id')}）")
        return True
    except Exception as e:
        print(f"Product Hunt 校验失败：{e}")
        return False


def get_product(slug):
    q = """
    query($slug: String!) {
      product(slug: $slug) { id name tagline website url thumbnail { url } }
    }
    """
    return _gql(q, {"slug": slug}).get("product")


def create_post(slug, name, tagline, description, url, topics=None):
    product = get_product(slug)
    if not product:
        raise RuntimeError(f"未找到产品：{slug}（需先在 producthunt.com 创建产品页）")
    q = """
    mutation($input: CreatePostInput!) {
      createPost(input: $input) { post { id name tagline url } }
    }
    """
    variables = {
        "input": {
            "productId": product["id"],
            "name": name,
            "tagline": tagline[:60],
            "description": description[:260],
            "url": url,
            "topics": topics or [],
        }
    }
    data = _gql(q, variables)
    return data.get("createPost", {}).get("post")


if __name__ == "__main__":
    verify()
