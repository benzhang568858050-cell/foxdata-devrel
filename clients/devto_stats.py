#!/usr/bin/env python3
"""Dev.to 运营数据周报：拉取账号文章表现，生成可迭代的运营报表。

用法：python3 clients/devto_stats.py
"""
import json
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CREDS_FILE = BASE_DIR / "config" / "devto_creds.json"


def main():
    key = json.loads(CREDS_FILE.read_text())["api_key"]
    r = requests.get(
        "https://dev.to/api/articles/me",
        params={"per_page": 100, "state": "all"},
        headers={"Accept": "application/vnd.forem.api-v1+json", "api-key": key},
    )
    arts = r.json()
    if not arts:
        print("暂无文章数据")
        return

    print(f"{'='*62}")
    print(f"Dev.to 运营周报 · {datetime.now().strftime('%Y-%m-%d')}（共 {len(arts)} 篇）")
    print(f"{'='*62}")
    rows = []
    for a in arts:
        views = a.get("page_views_count") or 0
        reactions = a.get("positive_reactions_count") or 0
        comments = a.get("comments_count") or 0
        rate = (reactions / views * 100) if views else 0
        rows.append((views, reactions, comments, rate, a["title"][:48], a["url"]))
        print(f"👁 {views:>5}  ❤ {reactions:>3}  💬 {comments:>3}  | 互动率 {rate:>5.1f}%  {a['title'][:48]}")

    total_v = sum(x[0] for x in rows)
    total_r = sum(x[1] for x in rows)
    total_c = sum(x[2] for x in rows)
    print("-" * 62)
    print(f"汇总：views {total_v} | reactions {total_r} | comments {total_c} | 综合互动率 {(total_r+total_c)/total_v*100 if total_v else 0:.1f}%")
    print("=" * 62)
    print("参考基准：互动率 >3% 良好；评论是官方 promotion 的最强信号。")
    print("最佳实践：发布后 2h 内回复全部评论；每周 1-2 篇；UTC 13-18 点发布。")


if __name__ == "__main__":
    main()
