#!/usr/bin/env python3
"""X 任务联动桥接脚本：外部发帖/养号任务与 devrel 矩阵的对接接口。

任何环境（本地电脑/服务器/DeerFlow 线程）均可独立运行：
    python3 clients/x_matrix_bridge.py publish   # 从草稿池发 1 条未发布草稿（去重+间隔保护）
    python3 clients/x_matrix_bridge.py warmup    # 养号（每日限频，间隔随机）
    python3 clients/x_matrix_bridge.py status    # 联动状态总览

协议：
- 草稿池：posts/drafts/*.txt（文件名 = 去重 key）
- 状态：state/published.json 的 x 数组（draft 文件名去重）
- 限频：每日 ≤5 条，间隔 ≥45 分钟；养号见 state/warmup.json
"""
import json
import random
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

DRAFTS_DIR = BASE_DIR / "posts" / "drafts"
IMAGES_DIR = BASE_DIR / "posts" / "images"
STATE_FILE = BASE_DIR / "state" / "published.json"
WARMUP_FILE = BASE_DIR / "state" / "warmup.json"

MAX_PER_DAY = 5
POST_GAP_MIN = 45


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def publish_one():
    """从草稿池发布一条未发布草稿（去重 + 每日限频 + 间隔保护）。"""
    from clients.x_client import post_tweet
    pub = load_json(STATE_FILE, {"x": [], "devto": [], "ph": []})
    now = datetime.now()

    # 每日限频
    today_posts = [d for d in pub.get("x", [])
                   if d.get("published_at", "").startswith(now.strftime("%Y-%m-%d"))]
    if len(today_posts) >= MAX_PER_DAY:
        print(f"⚠️ 今日已达上限 {MAX_PER_DAY} 条，跳过")
        return False

    # 间隔保护
    if today_posts:
        last = max(d["published_at"] for d in today_posts)
        gap = (now - datetime.fromisoformat(last)).total_seconds() / 60
        if gap < POST_GAP_MIN:
            print(f"⚠️ 距上次发布 {gap:.0f} 分钟 < {POST_GAP_MIN}，跳过")
            return False

    # 挑未发布草稿（优先 x-promo 引流草稿）
    published_names = {d.get("draft") for d in pub.get("x", [])}
    candidates = [f for f in DRAFTS_DIR.glob("*.txt") if f.name not in published_names]
    if not candidates:
        print("草稿池无未发布内容")
        return False
    candidates.sort(key=lambda f: 0 if f.name.startswith("x-promo") else 1)
    draft = candidates[0]

    # 配图（60% 概率）
    images = []
    if random.random() < 0.6 and IMAGES_DIR.exists():
        imgs = [p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
        if imgs:
            images = [str(random.choice(imgs))]

    text = draft.read_text(encoding="utf-8").strip()
    result = post_tweet(text, images or None)
    pub.setdefault("x", []).append({"draft": draft.name, "published_at": now.isoformat(),
                                    "url": result.get("url", "")})
    save_json(STATE_FILE, pub)
    print(f"✅ 已发布: {draft.name} → {result.get('url', '')}")
    return True


def warmup():
    """养号（每日限频、间隔随机、去重）——仅在固定 IP 环境运行。"""
    from clients.x_client import get_client
    state = load_json(WARMUP_FILE, {"date": "", "liked": [], "followed": [], "likes_done": 0, "follows_done": 0})
    today = datetime.now().strftime("%Y-%m-%d")
    if state.get("date") != today:
        state = {"date": today, "liked": [], "followed": [], "likes_done": 0, "follows_done": 0}

    client = get_client()
    targets = ["mashable", "TechCrunch", "producthunt", "indiehackers",
               "MobileDevMemo", "appfigures", "SensorTower"]
    random.shuffle(targets)
    likes_target = random.randint(8, 15)
    follows_target = random.randint(1, 3)

    for u in targets:
        if state["likes_done"] >= likes_target:
            break
        try:
            user = client.get_user_by_screen_name(u)
            for tw in client.get_user_tweets(user.id, count=5):
                tid = str(tw.id)
                if tid in state["liked"]:
                    continue
                client.favorite_tweet(tid)
                state["liked"].append(tid)
                state["likes_done"] += 1
                print(f"❤️ @{u}: {tid}")
                time.sleep(random.randint(25, 90))
                if state["likes_done"] >= likes_target:
                    break
        except Exception as e:
            print(f"⚠️ @{u}: {e}")

    for u in targets:
        if state["follows_done"] >= follows_target or u in state["followed"]:
            continue
        try:
            user = client.get_user_by_screen_name(u)
            client.follow_user(user.id)
            state["followed"].append(u)
            state["follows_done"] += 1
            print(f"➕ @{u}")
            time.sleep(random.randint(25, 90))
        except Exception as e:
            print(f"⚠️ @{u}: {e}")

    save_json(WARMUP_FILE, state)
    print(f"养号完成：点赞 {state['likes_done']}/{likes_target}，关注 {state['follows_done']}/{follows_target}")


def status():
    pub = load_json(STATE_FILE, {"x": [], "devto": [], "ph": []})
    drafts = list(DRAFTS_DIR.glob("*.txt"))
    pending = [f.name for f in drafts if f.name not in {d.get("draft") for d in pub.get("x", [])}]
    print(f"X 已发布: {len(pub.get('x', []))} 条")
    print(f"草稿池: {len(drafts)} 条，待发布: {len(pending)} 条")
    for n in pending[:10]:
        print(f"  - {n}")
    w = load_json(WARMUP_FILE, {})
    if w:
        print(f"今日养号: 点赞 {w.get('likes_done', 0)} / 关注 {w.get('follows_done', 0)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "publish":
        publish_one()
    elif cmd == "warmup":
        warmup()
    else:
        status()
