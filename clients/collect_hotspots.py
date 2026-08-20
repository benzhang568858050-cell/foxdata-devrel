#!/usr/bin/env python3
"""X 热点采集（矩阵选题源）：X 实时趋势 → posts/HOTSPOTS.md

用法：python3 clients/collect_hotspots.py
输出：posts/HOTSPOTS.md（供内容工厂选题参考；结合 foxdata 数据生成内容）
"""
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

    lines = [f"# X 热点（{datetime.now().strftime('%Y-%m-%d %H:%M')}）", ""]
    for cat in ("trending", "for-you"):
        try:
            trends = client.get_trends(category=cat, count=10)
            lines.append(f"## {cat}")
            for t in trends:
                name = getattr(t, "name", None) or getattr(t, "trend_name", str(t))
                if name and not name.startswith("#"):
                    lines.append(f"- {name}")
            lines.append("")
        except Exception as e:
            print(f"⚠️ {cat} 趋势获取失败：{e}")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 热点已更新：{OUT_FILE}")
    return True


if __name__ == "__main__":
    main()
