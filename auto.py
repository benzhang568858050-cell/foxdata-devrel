#!/usr/bin/env python3
"""一键自动化发布（最简路径）：FoxData 数据 → 内容 → 多平台发布 → AI 运营。

用法：
    python3 auto.py                 # 全链路：数据快照检查 → 计划 → 发布
    python3 auto.py devto-ops       # AI 运营引擎：monitor → analyze → revive → inject → report
    python3 auto.py fetch           # 只拉数据
    python3 auto.py plan            # 只生成计划
    python3 auto.py publish         # 只发布到期内容
    python3 auto.py status          # 各平台凭据与内容状态总览
"""
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
SNAPSHOT_FILE = DATA_DIR / "raw_latest.json"


def fetch():
    DATA_DIR.mkdir(exist_ok=True)
    from clients.foxdata_client import load_key, call_api
    if not load_key():
        print("[fetch] 未配置 x_openapi_key → 跳过官方拉取")
        print("[fetch] 提示：可在对话中调用 foxdata-aichat MCP 拉取数据后，另存为 data/raw_latest.json")
        return False
    try:
        snap = {"date": datetime.now().strftime("%Y-%m-%d"), "source": "foxdata-open-api"}
        for region in ("TH", "VN"):
            try:
                snap[f"download_top_{region}"] = call_api(
                    "/app/download-ranking",
                    {"region": region, "category": "-1", "date": snap["date"]},
                )
            except Exception as e:
                print(f"[fetch] {region} 下载榜跳过: {e}")
        SNAPSHOT_FILE.write_text(json.dumps(snap, ensure_ascii=False, indent=2))
        print(f"[fetch] 数据快照已保存: {SNAPSHOT_FILE}")
        return True
    except Exception as e:
        print(f"[fetch] 失败: {e}")
        return False


def plan():
    import create_plan
    create_plan.main()


def publish():
    import daily_post
    daily_post.main()


def status():
    print("=" * 56)
    print("devrel-automation · 一键自动化状态")
    print("=" * 56)
    checks = [
        ("FoxData 官方 API", "config/foxdata_creds.json"),
        ("X", "config/x_cookies.json"),
        ("Dev.to", "config/devto_creds.json"),
        ("Product Hunt", "config/ph_creds.json"),
    ]
    for name, path in checks:
        ok = (BASE_DIR / path).exists()
        print(f"  {'✅' if ok else '⬜'} {name}")
    drafts = list((BASE_DIR / "posts" / "drafts").glob("*.txt"))
    arts = list((BASE_DIR / "content" / "articles").glob("*.md"))
    snap = SNAPSHOT_FILE.exists()
    print(f"  内容: X 短帖 {len(drafts)} 篇 | Dev.to 长文 {len(arts)} 篇 | 数据快照 {'✅' if snap else '⬜'}")
    st = BASE_DIR / "state" / "published.json"
    if st.exists():
        data = json.loads(st.read_text())
        for k, v in data.items():
            print(f"  已发布 {k}: {len(v)} 条")
    print("=" * 56)
    print("下一步：python3 auto.py fetch && python3 auto.py plan && python3 auto.py publish")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "all":
        fetch()
        plan()
        publish()
    elif cmd == "fetch":
        fetch()
    elif cmd == "plan":
        plan()
    elif cmd == "publish":
        publish()
    elif cmd == "status":
        status()
    elif cmd == "devto-ops":
        from clients.devto_engine import monitor, analyze, revive, inject, report
        monitor(); analyze(); revive(); inject(); report()
    else:
        print(__doc__)
