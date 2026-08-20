#!/usr/bin/env python3
"""Dev.to 客户端 —— 官方 API 发长文（免费，Markdown，Forem API V1）。

凭据：config/devto_creds.json  {"api_key": "xxx"}（dev.to → Settings → Extensions → API Keys）
文章：content/articles/*.md，frontmatter 格式：

    ---
    title: 标题
    tags: api, aso  (最多 4 个，去掉 # 号)
    series: FoxData API 系列(可选)
    scheduled: 2026-08-21  (发布日期；留空/过去 = 立即发布)
    published: false       (true 直接公开，false 存草稿)
    ---
    正文 Markdown...
"""
import json
import re
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CREDS_FILE = BASE_DIR / "config" / "devto_creds.json"
ARTICLES_DIR = BASE_DIR / "content" / "articles"
API = "https://dev.to/api/articles"

# Forem API V1（V0 已标记弃用）
V1_HEADERS = {"Accept": "application/vnd.forem.api-v1+json", "Content-Type": "application/json"}


def load_key():
    if not CREDS_FILE.exists():
        raise RuntimeError("未配置 Dev.to 凭据：config/devto_creds.json（api_key）")
    return json.loads(CREDS_FILE.read_text())["api_key"]


def auth_headers():
    h = V1_HEADERS.copy()
    h["api-key"] = load_key()
    return h


def verify():
    key = load_key()
    r = requests.get(
        "https://dev.to/api/users/me",
        headers={"Accept": "application/vnd.forem.api-v1+json", "api-key": key},
        timeout=30,
    )
    if r.status_code == 200:
        d = r.json()
        print(f"Dev.to 登录 OK：@{d.get('username')}（{d.get('name')}）")
        return True
    print(f"Dev.to 校验失败（{r.status_code}）：{r.text[:200]}")
    return False


def parse_frontmatter(text):
    """解析文章 frontmatter，返回 (meta, body_markdown)。"""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text.strip()
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, m.group(2).strip()


def is_due(path):
    """是否到期可发布（按 scheduled 日期）。"""
    text = path.read_text(encoding="utf-8")
    meta, _ = parse_frontmatter(text)
    sched = meta.get("scheduled", "")
    if not sched:
        return True  # 无日期 = 立即
    try:
        return datetime.fromisoformat(sched).date() <= datetime.now().date()
    except ValueError:
        return True


def publish_article(path, published=True):
    """发布一篇 Dev.to 文章。返回 {id, url}。"""
    key = load_key()
    text = Path(path).read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    # 剥离本地调度字段（scheduled），避免 Dev.to YAML 解析 Date 报错
    body = "\n".join(ln for ln in body.splitlines() if not ln.startswith("scheduled:"))

    tags = [t.strip().lstrip("#") for t in meta.get("tags", "").split(",") if t.strip()][:4]
    payload = {
        "article": {
            "title": meta.get("title", "Untitled"),
            "body_markdown": body,
            "published": bool(published),
            "tags": tags,
        }
    }
    if meta.get("series"):
        payload["article"]["series"] = meta["series"]

    r = requests.post(API, json=payload, headers=auth_headers(), timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Dev.to 发布失败（{r.status_code}）：{r.text[:300]}")
    d = r.json()
    return {"id": d.get("id"), "url": d.get("url"), "title": d.get("title")}


def update_article(article_id, title=None, tags=None, body_markdown=None,
                   series=None, published=True):
    """更新已发布文章（Forem API V1，正确姿势）。

    注意：title/tags/series 必须走【顶层参数】，body_markdown 只传纯正文
    （严禁把 frontmatter 整个塞进 body——会导致文章被重建、标题带引号）。
    """
    payload = {"article": {}}
    if title is not None:
        payload["article"]["title"] = title
    if tags is not None:
        payload["article"]["tags"] = tags[:4]
    if body_markdown is not None:
        payload["article"]["body_markdown"] = body_markdown
    if series is not None:
        payload["article"]["series"] = series
    payload["article"]["published"] = bool(published)

    r = requests.put(f"{API}/{article_id}", json=payload, headers=auth_headers(), timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"Dev.to 更新失败（{r.status_code}）：{r.text[:300]}")
    d = r.json()
    return {"id": d.get("id"), "url": d.get("url"), "title": d.get("title")}


if __name__ == "__main__":
    verify()
