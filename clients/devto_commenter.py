#!/usr/bin/env python3
"""Dev.to 评论互动自动化（Playwright，保守策略）。

风控设计：
- 每天 2-3 篇，随机间隔 3-8 分钟
- 评论内容高质量（基于文章标签生成数据洞察，非 "nice post"）
- 随机鼠标移动 + 滚动 + 停顿（模拟真人阅读）
- 反检测：stealth 模式（隐藏 webdriver 标识）
- 每日限频 + 去重（不评论同一篇两次）

凭据：config/devto_cookies.json（Cookie-Editor 导出）
用法：python3 clients/devto_commenter.py
"""
import asyncio
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

CREDS_FILE = BASE_DIR / "config" / "devto_creds.json"
COOKIES_FILE = BASE_DIR / "config" / "devto_cookies.json"
STATE_FILE = BASE_DIR / "state" / "devto_comments.json"
LOG_FILE = BASE_DIR / "logs" / "devto_comments.log"

API_KEY = json.loads(CREDS_FILE.read_text())["api_key"] if CREDS_FILE.exists() else None
API_H = {"Accept": "application/vnd.forem.api-v1+json", "api-key": API_KEY} if API_KEY else {}

DAILY_MIN = 2
DAILY_MAX = 3
DELAY_MIN = 180
DELAY_MAX = 480
READ_TIME_MIN = 20
READ_TIME_MAX = 60

TARGET_TAGS = ["api", "aso", "data", "showdev", "mobile", "productivity"]

COMMENT_TEMPLATES = {
    "api": [
        "Great breakdown. The API cost comparison is spot on — we've been using a similar approach with the FoxData API and the math checks out. One thing I'd add: watch the per-call credit costs, they add up fast at scale.",
        "Really useful. The point about pagination is underrated — we hit rate limits before realizing our loop was making redundant calls. Your `next` key approach is the right pattern.",
        "This is a solid teardown. The data pipeline vs dashboard distinction is exactly the decision teams need to make. We went API-first and never looked back.",
    ],
    "aso": [
        "Interesting data. The keyword coverage gap you identified is a real blind spot — we found similar patterns in SEA markets where Temu out-covers Shopee by 2x+ on keywords.",
        "Great analysis. The misspelling defense point is often overlooked. We tracked our brand misspellings and found 2-3x conversion rates vs generic terms.",
        "This matches our experience. Rating stability over rating level is an underrated ASO signal — store algorithms definitely penalize volatility.",
    ],
    "data": [
        "Love the data-driven approach. The daily velocity metric is something we track too — it reveals product health shifts weeks before the average moves.",
        "Really insightful. The cross-category analysis is particularly interesting — we see similar overlap between shopping and fintech apps in SEA.",
        "Solid teardown. The correlation between version cadence and review velocity is something we've observed too. Shipping fixes on a regular cycle directly impacts 1-star trends.",
    ],
    "showdev": [
        "Nice project! The automation angle is impressive — we're doing something similar with app market data APIs. The GitHub Actions scheduling approach is clean.",
        "Cool build. The self-hosted angle is refreshing in a world of SaaS-only tools. What's your stack for the content pipeline?",
        "Great work. The open-source DevRel automation space needs more of this. Real data makes content so much more credible.",
    ],
    "default": [
        "Really enjoyed this. The practical examples make it actionable — too many posts stay theoretical. Bookmarked for our team's reference.",
        "Solid writeup. The structured approach is exactly what developers need — clear steps, real data, reproducible code.",
        "Great content. This kind of data-driven analysis is rare in the dev community. We need more posts like this.",
    ],
}


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"date": "", "commented": [], "count": 0}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def find_articles():
    articles = []
    for tag in TARGET_TAGS:
        try:
            r = requests.get("https://dev.to/api/articles",
                             params={"tag": tag, "per_page": 10, "top": 7}, headers=API_H, timeout=30)
            for a in r.json():
                if "_a29a85391c475e16a6bed4" in a.get("url", ""):
                    continue
                articles.append({"id": a["id"], "url": a["url"], "title": a["title"],
                                 "tags": a.get("tag_list", []), "reactions": a.get("positive_reactions_count", 0)})
        except Exception as e:
            log(f"⚠️ 获取 #{tag} 文章失败: {e}")
    seen = set()
    unique = []
    for a in articles:
        if a["id"] not in seen:
            seen.add(a["id"])
            unique.append(a)
    unique.sort(key=lambda x: x["reactions"], reverse=True)
    return unique


def pick_comment(article):
    tags = [t.lower() for t in article.get("tags", [])]
    for tag in ["api", "aso", "data", "showdev"]:
        if tag in tags:
            return random.choice(COMMENT_TEMPLATES[tag])
    return random.choice(COMMENT_TEMPLATES["default"])


def load_cookies():
    if not COOKIES_FILE.exists():
        return None
    raw = json.loads(COOKIES_FILE.read_text())
    if isinstance(raw, list):
        return [{"name": c["name"], "value": c["value"], "domain": c.get("domain", ".dev.to"),
                 "path": c.get("path", "/"), "secure": c.get("secure", True),
                 "httpOnly": c.get("httpOnly", False), "sameSite": "Lax"} for c in raw]
    return raw


async def run():
    from playwright.async_api import async_playwright

    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    if state.get("date") != today:
        state = {"date": today, "commented": [], "count": 0}

    target_count = random.randint(DAILY_MIN, DAILY_MAX)
    if state["count"] >= target_count:
        log(f"今日已评论 {state['count']} 篇，达到上限 {target_count}，跳过")
        return

    cookies = load_cookies()
    if not cookies:
        log("⚠️ 未配置 Dev.to cookies（config/devto_cookies.json）")
        log("   获取：Chrome 装 Cookie-Editor → 登录 dev.to → 导出 cookies JSON")
        return

    articles = find_articles()
    commented_ids = {a["id"] for a in state["commented"]}
    candidates = [a for a in articles if a["id"] not in commented_ids]
    if not candidates:
        log("无可评论的候选文章")
        return

    log(f"候选 {len(candidates)} 篇，目标 {target_count} 篇，已评论 {state['count']} 篇")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-dev-shm-usage"])
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US")
        await context.add_cookies(cookies)
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = { runtime: {} };
        """)
        page = await context.new_page()

        for article in candidates:
            if state["count"] >= target_count:
                break
            try:
                await page.goto(article["url"], wait_until="networkidle", timeout=30000)
                read_time = random.randint(READ_TIME_MIN, READ_TIME_MAX)
                log(f"📖 阅读: {article['title'][:50]}（{read_time}s）")
                for _ in range(random.randint(2, 4)):
                    await page.mouse.wheel(0, random.randint(200, 600))
                    await asyncio.sleep(random.uniform(3, 8))
                await asyncio.sleep(read_time)

                comment_box = await page.query_selector("textarea[id*='comment'], textarea[placeholder*='comment'], div[contenteditable='true']")
                if not comment_box:
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(2)
                    comment_box = await page.query_selector("textarea[id*='comment'], textarea[placeholder*='comment'], div[contenteditable='true']")
                if not comment_box:
                    log(f"⚠️ 未找到评论框: {article['title'][:40]}")
                    continue

                comment_text = pick_comment(article)
                await comment_box.click()
                await asyncio.sleep(random.uniform(1, 3))
                for char in comment_text:
                    await page.keyboard.type(char, delay=random.randint(30, 80))
                    if random.random() < 0.05:
                        await asyncio.sleep(random.uniform(0.5, 2))
                await asyncio.sleep(random.uniform(2, 5))

                submit = await page.query_selector("button[type='submit'], button:has-text('Submit'), button:has-text('Post')")
                if submit:
                    await submit.click()
                    await asyncio.sleep(3)
                    content = await page.content()
                    if comment_text[:30] in content:
                        state["commented"].append({"id": article["id"], "url": article["url"],
                                                    "title": article["title"], "at": datetime.now().isoformat()})
                        state["count"] += 1
                        save_state(state)
                        log(f"✅ 评论成功 [{state['count']}/{target_count}]: {article['title'][:40]}")
                    else:
                        log(f"⚠️ 评论可能失败: {article['title'][:40]}")
                else:
                    log(f"⚠️ 未找到提交按钮: {article['title'][:40]}")

                if state["count"] < target_count:
                    delay = random.randint(DELAY_MIN, DELAY_MAX)
                    log(f"⏳ 等待 {delay}s 后评论下一篇...")
                    await asyncio.sleep(delay)
            except Exception as e:
                log(f"⚠️ 评论失败: {article['title'][:40]} | {type(e).__name__}: {str(e)[:100]}")

        await browser.close()
    log(f"今日评论完成: {state['count']}/{target_count} 篇")


if __name__ == "__main__":
    asyncio.run(run())
