#!/usr/bin/env python3
"""按计划发布到期内容：X 短帖 / Dev.to 长文 / Product Hunt 更新。"""
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
PLANS_DIR = BASE_DIR / "plans"
STATE_FILE = BASE_DIR / "state" / "published.json"
LOG_FILE = BASE_DIR / "logs" / "daily.log"

sys.path.insert(0, str(BASE_DIR))
from create_plan import load_settings  # noqa: E402


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_published():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"x": [], "devto": [], "ph": []}


def save_published(pub):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(pub, ensure_ascii=False, indent=2))


def last_post_time(pub, platform):
    ts = [d.get("published_at") for d in pub.get(platform, []) if d.get("published_at")]
    return max(ts) if ts else None


def main():
    settings = load_settings()
    pub = load_published()
    now = datetime.now()

    plan_files = sorted(PLANS_DIR.glob("plan_*.json"))
    if not plan_files:
        log("没有计划文件，请先运行 create_plan.py")
        return

    # 平台启用开关
    enabled_map = {
        p: (cfg.get("enabled", True) if isinstance(cfg, dict) else True)
        for p, cfg in settings.items()
    }
    due = []
    for pf in plan_files:
        try:
            data = json.loads(pf.read_text())
        except json.JSONDecodeError:
            continue
        for p in data.get("posts", []):
            if not enabled_map.get(p["platform"], True):
                continue
            if datetime.fromisoformat(p["time"]) <= now:
                due.append(p)

    if not due:
        log("本轮无到期内容")
        return

    done = 0
    for p in due:
        platform = p["platform"]
        if any(d.get("draft") == p["draft"] for d in pub.get(platform, [])):
            log(f"[{platform}] 跳过（已发布过）: {p['draft']}")
            continue

        # X 间隔保护
        if platform == "x":
            last = last_post_time(pub, "x")
            if last:
                gap = (now - datetime.fromisoformat(last)).total_seconds() / 60
                if gap < settings["post_gap_min"]:
                    log(f"[x] 跳过（距上次 {gap:.0f} 分钟 < {settings['post_gap_min']}）: {p['draft']}")
                    continue

        try:
            if platform == "x":
                from clients.x_client import post_tweet
                result = post_tweet(p["text"], p.get("images") or None)
                url = result.get("url", "")
            elif platform == "devto":
                from clients.devto_client import publish_article
                result = publish_article(p["path"], published=True)
                url = result.get("url", "")
            elif platform == "ph":
                from clients.ph_client import create_post
                pl = p.get("payload", {})
                result = create_post(
                    slug=pl.get("slug", ""),
                    name=pl.get("name", ""),
                    tagline=pl.get("tagline", ""),
                    description=pl.get("description", ""),
                    url=pl.get("url", ""),
                    topics=pl.get("topics", []),
                )
                url = (result or {}).get("url", "")
            else:
                log(f"未知平台: {platform}")
                continue

            pub.setdefault(platform, []).append({
                "draft": p["draft"], "fp": p.get("fp", ""), "published_at": now.isoformat(), "url": url,
            })
            save_published(pub)
            log(f"[{platform}] 发布成功: {p['draft']} → {url}")
            done += 1
        except Exception as e:
            log(f"[{platform}] 发布失败（不重试）: {p['draft']} | {e}")

    log(f"本轮完成，成功 {done} 条")


if __name__ == "__main__":
    main()
