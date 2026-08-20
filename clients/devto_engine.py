#!/usr/bin/env python3
"""Dev.to AI 运营引擎：全自动监控 → 分析 → 救活 → 互链注入 → 策略迭代。

用法：
    python3 clients/devto_engine.py monitor   # 拉数据存历史
    python3 clients/devto_engine.py analyze   # 表现分析+建议
    python3 clients/devto_engine.py revive    # 低曝光自动救活
    python3 clients/devto_engine.py inject    # 草稿注入互链+引导
    python3 clients/devto_engine.py report    # 策略轮换
    python3 auto.py devto-ops                 # 一键全链路
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
from clients.devto_client import parse_frontmatter  # noqa: E402

CREDS_FILE = BASE_DIR / "config" / "devto_creds.json"
STATS_FILE = BASE_DIR / "state" / "devto_stats.json"
STRATEGY_FILE = BASE_DIR / "config" / "devto_strategy.json"
PUBLISHED_FILE = BASE_DIR / "state" / "published.json"
ARTICLES_DIR = BASE_DIR / "content" / "articles"

DEFAULT_STRATEGY = {
    "best_hours_utc": [13, 14, 15, 16, 17, 18],  # 数据研究：UTC 下午互动最佳
    "tag_pool": {
        "推荐": ["api", "data", "aso", "mobile"],
        "流量池": ["webdev", "productivity", "showdev", "discuss"],
    },
    "title_templates": [
        "数据钩子：{insight}，但{contrast}",
        "数字场景：{minutes} 分钟搭一个{thing}（{n} 个 API 端点）",
        "反直觉：排名第 {rank} 的 App，正在{action}",
        "决策指南：{market_a} or {market_b}？{data_source}说",
        "教程：用 {api} 做{task}（{steps} 步，含代码）",
    ],
    "weekly_target": 2,
    "low_engagement_threshold": {"hours": 24, "views": 100, "rate": 3.0},
    "revive": {
        "enabled": True,
        "max_per_article": 1,      # 每篇文章最多救活 1 次（防频繁改标题）
        "hours": 24,               # 发布 24h 后才考虑救活
        "views_below": 100,        # views 低于该值触发
    },
}


def load_creds():
    return json.loads(CREDS_FILE.read_text())["api_key"]


def load_stats():
    if STATS_FILE.exists():
        return json.loads(STATS_FILE.read_text())
    return {"history": [], "latest": {}}


def save_stats(stats):
    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2))


def load_strategy():
    if STRATEGY_FILE.exists():
        merged = DEFAULT_STRATEGY.copy()
        merged.update(json.loads(STRATEGY_FILE.read_text()))
        return merged
    return DEFAULT_STRATEGY


def save_strategy(s):
    STRATEGY_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2))


def fetch_articles():
    key = load_creds()
    r = requests.get(
        "https://dev.to/api/articles/me",
        params={"per_page": 100, "state": "all"},
        headers={"Accept": "application/vnd.forem.api-v1+json", "api-key": key},
        timeout=30,
    )
    return r.json()


def monitor():
    """拉取文章数据，追加历史。"""
    stats = load_stats()
    arts = fetch_articles()
    snapshot = []
    for a in arts:
        snapshot.append({
            "id": a["id"], "title": a["title"], "url": a["url"],
            "tags": a.get("tag_list", ""),
            "views": a.get("page_views_count") or 0,
            "reactions": a.get("positive_reactions_count") or 0,
            "comments": a.get("comments_count") or 0,
            "published_at": a.get("published_at"),
            "checked_at": datetime.now().isoformat(),
        })
    stats["history"].append({"time": datetime.now().isoformat(), "snapshot": snapshot})
    stats["history"] = stats["history"][-30:]  # 保留 30 次
    stats["latest"] = snapshot
    save_stats(stats)
    print(f"[monitor] 已记录 {len(snapshot)} 篇文章数据（历史 {len(stats['history'])} 次快照）")
    for s in snapshot:
        rate = s["reactions"] / s["views"] * 100 if s["views"] else 0
        print(f"  👁{s['views']:>4} ❤{s['reactions']:>3} 💬{s['comments']:>2} | {rate:>4.1f}% | {s['title'][:46]}")


def analyze():
    """表现分析：低互动检测 + 归因 + 建议。"""
    stats = load_stats()
    arts = stats.get("latest", [])
    if not arts:
        print("[analyze] 暂无数据，先运行 monitor")
        return
    strat = load_strategy()
    th = strat["low_engagement_threshold"]
    now = datetime.now().astimezone()

    print("=" * 60)
    print("Dev.to 运营分析")
    print("=" * 60)
    alerts = []
    for s in arts:
        rate = s["reactions"] / s["views"] * 100 if s["views"] else 0
        pub = s.get("published_at") or ""
        if pub:
            age_h = (now - datetime.fromisoformat(pub.replace("Z", "+00:00"))).total_seconds() / 3600
            if age_h > th["hours"] and s["views"] < th["views"]:
                alerts.append(s)
                print(f"  ⚠️ 低曝光: {s['title'][:50]}（{age_h:.0f}h，{s['views']} views）")
    if not alerts:
        print("  ✅ 无低互动告警")

    # 归因：标签维度（简单启发式）
    tag_perf = {}
    for s in arts:
        tags = s.get("tags") or ""
        if isinstance(tags, list):
            tags = ",".join(tags)
        for t in tags.split(","):
            t = t.strip()
            if not t:
                continue
            d = tag_perf.setdefault(t, {"views": 0, "reactions": 0, "n": 0})
            d["views"] += s["views"]; d["reactions"] += s["reactions"]; d["n"] += 1
    if tag_perf:
        print("  标签表现：")
        for t, d in sorted(tag_perf.items(), key=lambda x: -x[1]["reactions"] / max(x[1]["views"], 1)):
            print(f"    #{t}: {d['n']}篇 | 互动率 {d['reactions']/max(d['views'],1)*100:.1f}%")

    # 建议输出（供内容工厂使用）
    print("-" * 60)
    print("策略建议：")
    print(f"  - 推荐发布时间: UTC {strat['best_hours_utc']}（北京 {[(h+8)%24 for h in strat['best_hours_utc']]} 点）")
    print(f"  - 推荐标签: {strat['tag_pool']['推荐']}")
    print("  - 标题模板（下次文章选用）:")
    for i, t in enumerate(strat["title_templates"][:3], 1):
        print(f"    {i}. {t}")
    if alerts:
        print("  - 建议: 为低曝光文章更新标题/首段，或调整标签（API 更新，5 分钟生效于 SEO）")
    print("=" * 60)
    return alerts


def load_data_insight():
    """从数据快照生成标题用数据点（无 LLM 的启发式）。"""
    snap_file = BASE_DIR / "data" / "raw_latest.json"
    if not snap_file.exists():
        return None
    try:
        snap = json.loads(snap_file.read_text())
    except Exception:
        return None
    ki = snap.get("keyword_index")
    if ki:
        top = max(ki, key=lambda k: abs(ki[k].get("VN", 0) - ki[k].get("TH", 0)))
        vn, th = ki[top].get("VN", 0), ki[top].get("TH", 0)
        winner = "Vietnam" if vn > th else "Thailand"
        return f"'{top}' search demand: {winner} {abs(vn - th)} pts higher"
    rank = snap.get("th_shopping_rank")
    if rank and len(rank) >= 4:
        _, _, k1 = rank[0]
        _, _, k2 = rank[2]
        return f"#3 Temu covers {k2:,} keywords vs #1 Shopee's {k1:,}"
    return "App Store data reveals the shift"


def revive():
    """低曝光自动救活：为 24h+ 且 views 低于阈值的文章生成新标题并更新。"""
    strat = load_strategy()
    cfg = strat.get("revive", {})
    if not cfg.get("enabled", True):
        print("[revive] 已禁用")
        return
    stats = load_stats()
    arts = stats.get("latest", [])
    if not arts:
        print("[revive] 无数据")
        return

    revived_file = BASE_DIR / "state" / "devto_revived.json"
    revived = json.loads(revived_file.read_text()) if revived_file.exists() else {}
    now = datetime.now().astimezone()
    insight = load_data_insight()

    for s in arts:
        a_id = str(s["id"])
        title = s["title"]
        views = s["views"]
        pub = s.get("published_at") or ""
        if not pub:
            continue
        try:
            age_h = (now - datetime.fromisoformat(pub.replace("Z", "+00:00"))).total_seconds() / 3600
        except ValueError:
            continue
        if age_h < cfg.get("hours", 24) or views >= cfg.get("views_below", 100):
            continue
        if revived.get(a_id, {}).get("count", 0) >= cfg.get("max_per_article", 1):
            continue

        core = title.split("—")[0].split(":")[0].strip()
        if len(core) > 42:
            core = core[:42].rstrip() + "…"
        candidate = f"{insight} — {core}" if insight else f"App Store data: {core}"
        if len(candidate) > 100:
            candidate = candidate[:97] + "…"
        if candidate == title:
            continue

        try:
            from clients.devto_client import update_article
            res = update_article(a_id, title=candidate)
            revived[a_id] = {"count": revived.get(a_id, {}).get("count", 0) + 1,
                             "old": title, "new": candidate, "at": now.isoformat()}
            revived_file.parent.mkdir(parents=True, exist_ok=True)
            revived_file.write_text(json.dumps(revived, ensure_ascii=False, indent=2))
            print(f"[revive] 🔄 已救活 [{a_id}]: {title[:40]} → {candidate[:60]}")
            print(f"         {res.get('url', '')}")
        except Exception as e:
            print(f"[revive] 更新失败 [{a_id}]: {e}")
    print("[revive] 完成")


def inject():
    """给未发布草稿注入「系列互链 + Discussion 引导」。"""
    pub = json.loads(PUBLISHED_FILE.read_text()) if PUBLISHED_FILE.exists() else {}
    devto_pub = [d for d in pub.get("devto", []) if d.get("url")]
    if not devto_pub:
        print("[inject] 暂无已发布文章，跳过互链注入")
        return

    links = "\n".join(f"- [{Path(d['draft']).stem.replace('-', ' ').title()}]({d['url']})" for d in devto_pub)
    for f in sorted(ARTICLES_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        changed = False
        if "## More from this series" not in text:
            block = f"\n## More from this series\n\n{links}\n"
            text = text.rstrip() + "\n" + block
            changed = True
        if "## Discussion" not in text:
            text = text.rstrip() + """
## Discussion

What do you think? Drop a comment — I read every one and answer within a day.
"""
            changed = True
        if changed:
            f.write_text(text, encoding="utf-8")
            print(f"[inject] ✅ {f.name} 已注入互链+引导")
        else:
            print(f"[inject] - {f.name} 已完备")


def report():
    """汇总报告（自动生成策略文件更新）。"""
    strat = load_strategy()
    stats = load_stats()
    arts = stats.get("latest", [])
    if arts:
        total_r = sum(s["reactions"] for s in arts)
        total_v = sum(s["views"] for s in arts)
        rate = total_r / total_v * 100 if total_v else 0
        if rate < 3 and total_v > 0:
            strat["tag_pool"]["推荐"] = strat["tag_pool"]["流量池"][:2] + strat["tag_pool"]["推荐"][:2]
            save_strategy(strat)
            print(f"[report] 综合互动率 {rate:.1f}% 偏低 → 已轮换标签组合: {strat['tag_pool']['推荐']}")
        else:
            print(f"[report] 综合互动率 {rate:.1f}% 正常，维持当前策略")
    print("[report] 完成")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "monitor":
        monitor()
    elif cmd == "analyze":
        analyze()
    elif cmd == "revive":
        revive()
    elif cmd == "inject":
        inject()
    elif cmd == "report":
        report()
    else:
        print(__doc__)
