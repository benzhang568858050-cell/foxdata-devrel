#!/usr/bin/env python3
"""统一发布计划生成器：短帖（X）低频计划 + 长文（Dev.to）到期检测。"""
import hashlib
import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent
DRAFTS_DIR = BASE_DIR / "posts" / "drafts"
IMAGES_DIR = BASE_DIR / "posts" / "images"
ARTICLES_DIR = BASE_DIR / "content" / "articles"
PLANS_DIR = BASE_DIR / "plans"
STATE_FILE = BASE_DIR / "state" / "published.json"
SETTINGS_FILE = BASE_DIR / "config" / "settings.json"

DEFAULT_SETTINGS = {
    "x": {"enabled": False, "min_per_day": 0, "max_per_day": 2},
    "devto": {"enabled": True, "max_per_day": 1},
    "ph": {"enabled": False, "max_per_day": 1},
    "window_hours": 24,
    "post_gap_min": 60,
    "image_prob": 0.6,
}


def load_settings():
    settings = DEFAULT_SETTINGS.copy()
    if SETTINGS_FILE.exists():
        settings.update(json.loads(SETTINGS_FILE.read_text()))
    return settings


def load_published():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"x": [], "devto": [], "ph": []}


def draft_fingerprint(text):
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]


def pick_images(n=1):
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    imgs = [p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in exts] if IMAGES_DIR.exists() else []
    if not imgs:
        return []
    return [str(random.choice(imgs)) for _ in range(min(n, len(imgs)))]


def main():
    settings = load_settings()
    published = load_published()
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()

    # ========== X 短帖计划 ==========
    drafts = []
    for f in sorted(DRAFTS_DIR.glob("*.txt")):
        text = f.read_text(encoding="utf-8").strip()
        if not text:
            continue
        fp = draft_fingerprint(text)
        used = any(d.get("draft") == f.name for d in published.get("x", []))
        if not used:
            drafts.append({"file": f.name, "text": text, "fp": fp})

    posts = []
    if settings["x"].get("enabled", True) and drafts:
        pool = list(drafts)
        random.shuffle(pool)
        max_n = min(settings["x"].get("max_per_day", 2), len(pool))
        min_n = min(settings["x"].get("min_per_day", 0), max_n)
        n = random.randint(min_n, max_n)
        ws = now + timedelta(minutes=15)
        we = now + timedelta(hours=settings["window_hours"])
        for _ in range(n):
            d = pool.pop()
            t = ws + timedelta(seconds=random.randint(0, int((we - ws).total_seconds())))
            item = {"platform": "x", "time": t.isoformat(), "draft": d["file"], "fp": d["fp"], "text": d["text"], "images": []}
            if random.random() < settings["image_prob"]:
                item["images"] = pick_images(1)
            posts.append(item)
        posts.sort(key=lambda x: x["time"])
        for i in range(1, len(posts)):
            prev = datetime.fromisoformat(posts[i - 1]["time"])
            cur = datetime.fromisoformat(posts[i]["time"])
            if (cur - prev).total_seconds() < settings["post_gap_min"] * 60:
                posts[i]["time"] = (prev + timedelta(minutes=settings["post_gap_min"])).isoformat()

    # ========== Dev.to 长文 ==========
    devto_due = []
    if settings["devto"].get("enabled", True):
        from clients.devto_client import is_due
        for a in sorted(ARTICLES_DIR.glob("*.md")):
            used = any(d.get("draft") == a.name for d in published.get("devto", []))
            if not used and is_due(a):
                devto_due.append({"platform": "devto", "time": now.isoformat(), "draft": a.name, "fp": draft_fingerprint(a.read_text(encoding="utf-8")), "path": str(a)})
        posts.extend(devto_due)

    # ========== Product Hunt ==========
    ph_due = []
    if settings["ph"].get("enabled", False):
        ph_dir = BASE_DIR / "content" / "ph"
        for f in sorted(ph_dir.glob("*.json")) if ph_dir.exists() else []:
            data = json.loads(f.read_text())
            fp = draft_fingerprint(json.dumps(data))
            used = any(d.get("fp") == fp for d in published.get("ph", []))
            sched = data.get("scheduled", "")
            if not used and (not sched or datetime.fromisoformat(sched).date() <= now.date()):
                ph_due.append({"platform": "ph", "time": now.isoformat(), "draft": f.name, "fp": fp, "payload": data})
        posts.extend(ph_due)

    if not posts:
        print("本次无任何到期/可排期内容")
        return

    out = PLANS_DIR / f"plan_{now.strftime('%Y%m%d')}.json"
    existing = json.loads(out.read_text()) if out.exists() else {"posts": []}
    # 只保留未到期的旧条目（到期条目视为已处理）
    existing["posts"] = [
        p for p in existing["posts"]
        if datetime.fromisoformat(p["time"]) > now
    ]
    seen = {(p["platform"], p["fp"]) for p in existing["posts"]}
    for p in posts:
        if (p["platform"], p["fp"]) not in seen:
            existing["posts"].append(p)
            seen.add((p["platform"], p["fp"]))
    out.write_text(json.dumps(existing, ensure_ascii=False, indent=2))

    print(f"计划已生成：{out}")
    for p in posts:
        t = datetime.fromisoformat(p["time"]).strftime("%m-%d %H:%M")
        extra = " +图" if p.get("images") else ""
        print(f"  [{p['platform']}] {t}  {p['draft'][:50]}{extra}")


if __name__ == "__main__":
    main()
