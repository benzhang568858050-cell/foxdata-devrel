<div align="center">

# 📨 FoxData API · DevRel Content Hub

**Automated developer content operations powered by [FoxData API](https://foxdata.com/app-data-api) — app market data → AI content → Dev.to publishing → growth ops.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![Automation](https://img.shields.io/badge/automation-GitHub%20Actions-orange.svg)](.github/workflows/publish.yml)
[![Platform](https://img.shields.io/badge/platform-Dev.to%20%7C%20X%20%7C%20Product%20Hunt-blueviolet.svg)](https://dev.to)

*Self-hosted, free, one command: `python3 auto.py`*

</div>

## 🚀 What is this?

An open-source automation system that turns **app store market data** ([FoxData API](https://docs.foxdata.com/)) into published developer content — automatically. Built for teams promoting **mobile app data APIs / ASO tools** to the developer community.

**Key features:**

- 🤖 **AI content pipeline** — real market data → data-driven articles & posts (SEO-friendly titles, series interlinking, discussion prompts)
- 📝 **Dev.to automation** — publish long-form articles via the official Forem API (V1), with dedup & interval protection
- 📈 **AI ops engine** — hourly monitoring, engagement analysis, low-exposure auto-revive (title optimization), tag rotation strategy
- 🔁 **Multi-platform ready** — X (Twitter), Product Hunt, Bluesky, Threads clients included
- ⏰ **Free scheduling** — GitHub Actions cron, no server needed
- 🗂 **Content hub** — the repo itself is the content CMS (articles, drafts, data snapshots)

## ⚡ Quick Start

```bash
git clone https://github.com/benzhang568858050-cell/foxdata-devrel
cd foxdata-devrel

# 1. Configure credentials (config/ dir, git-ignored)
#    config/devto_creds.json: {"api_key": "..."}  → dev.to Settings → API Keys

# 2. One-command automation: fetch data → plan → publish
python3 auto.py

# 3. AI ops engine: monitor → analyze → revive → interlink → strategy
python3 auto.py devto-ops
```

Requires: Python 3.10+, `pip install requests twikit` (project-local `.deps/` supported).

## 📁 Project Structure

```
├── clients/
│   ├── devto_client.py    # Dev.to publishing (Forem API V1, frontmatter-safe)
│   ├── devto_engine.py    # AI ops: monitor/analyze/revive/inject/report
│   ├── devto_stats.py     # Engagement weekly report
│   ├── foxdata_client.py  # FoxData Open API (x-openapi-key, pagination, retry)
│   ├── x_client.py        # X/Twitter (twikit, cookie-based)
│   └── ph_client.py       # Product Hunt (GraphQL)
├── content/articles/      # Long-form articles (Markdown + frontmatter)
├── posts/drafts/          # Short posts
├── data/                  # Market data snapshots
├── auto.py                # One-command entry
└── .github/workflows/     # Hourly auto-publish pipeline
```

## 📊 Publish Status

- **Dev.to**: 2 篇文章已发布
- **X**: 0 条短帖
- **Product Hunt**: 0 条更新
- **文章库**: 3 篇 | **短帖池**: 2 条
- 数据快照: `data/raw_latest.json`

_自动更新: 2026-08-20_

## 📚 Documentation & Links

- [FoxData Open API docs](https://docs.foxdata.com/) — authentication (`x-openapi-key`), endpoints, error codes
- [FoxData App Data API](https://foxdata.com/app-data-api) — subscription plans
- [Dev.to API (Forem V1)](https://docs.forem.com/api/) — the publishing channel

### 📖 Ops playbooks (in this repo)

- [Dev.to Growth Playbook](docs/devto-growth-playbook.md) — engagement & exposure strategy
- [Developer Forums Distribution Matrix](docs/developer-forums-distribution-matrix.md) — where to share content
- [Content Strategy Guide](docs/foxdata-content-guide.md) — content mix & cadence
- [Open Source Tools Research](docs/devto-open-source-tools-research.md) — what to reuse vs build

### 🛠 Installable skills

- [devto-operations](skills/devto-operations/SKILL.md) — `npx skills add benzhang568858050-cell/foxdata-devrel`
- [foxdata-auto-publish](skills/foxdata-auto-publish/SKILL.md) — same package, two skills

## 🧠 Content Strategy

Data-driven developer content, weekly cadence:
- 40% market insights · 20% keyword intelligence · 15% API tutorials · 10% ranking reports · 10% competitor teardowns · 5% product updates
- Best publish window: UTC 13:00–18:00 (data-backed)
- Series interlinking + discussion prompts on every article

## 🤝 License

[MIT](LICENSE) — free to use, fork, and learn from.

---

*Maintained by devrel-bot · auto-updated hourly*
