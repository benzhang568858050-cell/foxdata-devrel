#!/usr/bin/env python3
"""X 热点采集（矩阵选题源）：X 实时趋势 → posts/HOTSPOTS.md

用法：python3 clients/collect_hotspots.py
"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from clients.x_client import get_client  # noqa: E402

OUT_FILE = BASE_DIR / "posts" / "HOTSPOTS.md"


def main():
    try:
        client = get_client()
    except Exception as e:
        print(f"⚠️ X 未配置/登录失败，跳过热点采集：{e}")
        return False

    async def _fetch():
        lines = [f"# X 热点（{datetime.now().strftime('%Y-%m-%d %H:%M')}）", ""]
        for cat in ("trending", "for-you"):
            try:
                trends = await client.get_trends(category=cat, count=10)
                lines.append(f"## {cat}")
                for t in trends:
                    name = getattr(t, "name", None) or getattr(t, "trend_name", str(t))
                    if name and not name.startswith("#"):
                        lines.append(f"- {name}")
                lines.append("")
            except Exception as e:
                print(f"⚠️ {cat} 趋势获取失败：{e}")
        return "\n".join(lines)

    content = asyncio.run(_fetch())
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(content, encoding="utf-8")
    print(f"✅ 热点已更新：{OUT_FILE}")
    return True


if __name__ == "__main__":
    main()
