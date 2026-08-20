#!/usr/bin/env python3
"""GitHub 辅助：内容索引 README 生成 + 仓库自检。"""
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def check_structure():
    required = [
        "clients/x_client.py",
        "clients/devto_client.py",
        "clients/ph_client.py",
        "create_plan.py",
        "daily_post.py",
        "content/articles",
        "posts/drafts",
        ".github/workflows/publish.yml",
    ]
    missing = [p for p in required if not (BASE_DIR / p).exists()]
    if missing:
        print("缺失文件：")
        for m in missing:
            print(f"  - {m}")
        return False
    print("仓库结构完整 ✅")
    return True


def gen_readme():
    articles = sorted((BASE_DIR / "content" / "articles").glob("*.md"))
    drafts = sorted((BASE_DIR / "posts" / "drafts").glob("*.txt"))
    state = BASE_DIR / "state" / "published.json"
    pub = json.loads(state.read_text()) if state.exists() else {}

    lines = [
        "# FoxData API · DevRel Content Hub",
        "",
        "自动化的开发者内容运营仓库：X / Dev.to / GitHub / Product Hunt 多平台分发。",
        "",
        f"> 自动更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 📄 长文（Dev.to / Product Hunt）",
        "",
    ]
    for a in articles:
        lines.append(f"- {a.stem}（{a.name}）")
    lines += ["", "## 📝 短帖草稿（X）", ""]
    for d in drafts:
        lines.append(f"- {d.name}")
    lines += [
        "",
        "## 📊 发布状态",
        "",
        f"- X：{len(pub.get('x', []))} 条",
        f"- Dev.to：{len(pub.get('devto', []))} 篇",
        f"- Product Hunt：{len(pub.get('ph', []))} 条",
        "",
        "---",
        "由 devrel-automation 自动维护",
    ]
    (BASE_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print("README.md 已更新")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "init"
    if cmd == "init":
        check_structure()
    elif cmd == "readme":
        gen_readme()
