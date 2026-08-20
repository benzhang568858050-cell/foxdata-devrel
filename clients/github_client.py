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
    """生成 README.md：模板 + 自动发布状态（模板见 README.template.md）。"""
    articles = sorted((BASE_DIR / "content" / "articles").glob("*.md"))
    drafts = sorted((BASE_DIR / "posts" / "drafts").glob("*.txt"))
    state = BASE_DIR / "state" / "published.json"
    pub = json.loads(state.read_text()) if state.exists() else {}

    status_lines = [
        f"- **Dev.to**: {len(pub.get('devto', []))} 篇文章已发布",
        f"- **X**: {len(pub.get('x', []))} 条短帖",
        f"- **Product Hunt**: {len(pub.get('ph', []))} 条更新",
        f"- **文章库**: {len(articles)} 篇 | **短帖池**: {len(drafts)} 条",
        "- 数据快照: `data/raw_latest.json`",
        "",
        "_自动更新: " + datetime.now().strftime('%Y-%m-%d') + "_",
    ]
    status_block = "\n".join(status_lines)

    tpl = BASE_DIR / "README.template.md"
    if tpl.exists():
        content = tpl.read_text(encoding="utf-8").replace("{{PUBLISH_STATUS}}", status_block)
    else:
        content = "\n".join([
            "# FoxData API · DevRel Content Hub", "",
            status_block,
        ])
    (BASE_DIR / "README.md").write_text(content, encoding="utf-8")
    print("README.md 已更新（模板 + 状态）")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "init"
    if cmd == "init":
        check_structure()
    elif cmd == "readme":
        gen_readme()
