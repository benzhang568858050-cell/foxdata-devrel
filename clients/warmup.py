#!/usr/bin/env python3
"""X 养号模块（矩阵风控必备）：低频点赞 + 关注，模拟真人行为。

设计（沿用 x-automation 规范）：
- 每天点赞 8-15 次、关注 1-3 人（可配置）
- 动作间隔 25-90 秒随机
- 自动去重（done_ids / followed_ids）与每日限频
- 从矩阵内容池（Dev.to 文章链接、热点话题）中挑选互动目标

用法：python3 clients/warmup.py
"""
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from clients.x_client import get_client  # noqa: E402

STATE_FILE = BASE_DIR / "state" / "warmup.json"
LOG_FILE = BASE_DIR / "logs" / "warmup.log"

DEFAULT = {"likes_min": 8, "likes_max": 15, "follows_min": 1, "follows_max": 3,
           "delay_min": 25, "delay_max": 90}


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"date": "", "liked": [], "followed": [], "likes_done": 0, "follows_done": 0}


def main():
    cfg = DEFAULT
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    if state.get("date") != today:
        state = {"date": today, "liked": [], "followed": [], "likes_done": 0, "follows_done": 0}

    try:
        client = get_client()
    except Exception as e:
        log(f"⚠️ X 未配置，跳过养号：{e}")
        return

    # 目标账号池：科技/出海/API 领域（可扩展）
    targets = ["mashable", "TechCrunch", "producthunt", "indiehackers",
               "MobileDevMemo", "appfigures", "SensorTower", "growtix"]
    random.shuffle(targets)

    likes_target = random.randint(cfg["likes_min"], cfg["likes_max"])
    follows_target = random.randint(cfg["follows_min"], cfg["follows_max"])

    # 点赞（从目标账号时间线找近期推文）
    for u in targets:
        if state["likes_done"] >= likes_target:
            break
        try:
            user = client.get_user_by_screen_name(u)
            tweets = client.get_user_tweets(user.id, count=5)
            for tw in tweets:
                tid = str(tw.id)
                if tid in state["liked"]:
                    continue
                client.favorite_tweet(tid)
                state["liked"].append(tid)
                state["likes_done"] += 1
                log(f"❤️ 点赞 @{u}: {tid}")
                time.sleep(random.randint(cfg["delay_min"], cfg["delay_max"]))
                if state["likes_done"] >= likes_target:
                    break
        except Exception as e:
            log(f"⚠️ @{u} 点赞失败：{e}")

    # 关注
    for u in targets:
        if state["follows_done"] >= follows_target:
            break
        if u in state["followed"]:
            continue
        try:
            user = client.get_user_by_screen_name(u)
            client.follow_user(user.id)
            state["followed"].append(u)
            state["follows_done"] += 1
            log(f"➕ 关注 @{u}")
            time.sleep(random.randint(cfg["delay_min"], cfg["delay_max"]))
        except Exception as e:
            log(f"⚠️ @{u} 关注失败：{e}")

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))
    log(f"养号完成：点赞 {state['likes_done']}/{likes_target}，关注 {state['follows_done']}/{follows_target}")


if __name__ == "__main__":
    main()
