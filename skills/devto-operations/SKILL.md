---
name: devto-operations
description: Dev.to 开发者社区全自动运营技能。当用户提到「Dev.to 运营」「Dev.to 自动化发布」「提升 Dev.to 文章曝光」「Dev.to AI 运营」「发布文章到 dev.to」「developer community 运营」等需求时触发。覆盖：文章 API 发布（Markdown/frontmatter，Forem API V1）、系列互链注入、Discussion 讨论引导、运营数据监控与分析、低曝光自动救活、标签/标题/发布时间策略迭代、GitHub Actions 定时全自动。English: Automate Dev.to publishing and community growth — API publishing, series interlinking, engagement monitoring, low-exposure auto-revive, and data-driven content strategy.
---

# Dev.to 全自动运营系统（devto-operations）

在 Dev.to 开发者社区发布高质量内容并自动提升曝光：**发布 → 互链 → 监控 → 救活 → 策略迭代** 的完整闭环。

## 核心事实（先读）

1. Dev.to 无强算法，曝光来自：标签页、follow 时间线、官方 promotion（人工+互动信号）、Google SEO
2. **官方 API 免费**（Forem API **V1**，请求头 `accept: application/vnd.forem.api-v1+json`）：发文章、更新文章、读数据（api-key：Settings → Extensions → API Keys；V0 已标记弃用）
3. **无评论/点赞/关注的写入 API**——互动类动作无法 API 自动化（可用浏览器自动化补充）
4. 实测经验：互动率 >3% 良好；评论是 promotion 最强信号；UTC 13-18 发布最佳（38k 帖子数据研究）
5. 更新文章用 `devto_client.update_article(id, title=..., tags=..., body_markdown=纯正文)`（顶层参数）

## 系统组件

```
devrel-automation/（主系统，配合使用）
├── clients/
│   ├── devto_client.py   # 发布/更新文章（Forem V1、frontmatter 解析、scheduled 剥离）
│   ├── devto_engine.py   # AI 运营引擎：monitor/analyze/revive/inject/report
│   └── devto_stats.py    # 运营数据周报
├── content/articles/     # 文章草稿（Markdown + frontmatter）
├── config/
│   ├── devto_creds.json  # {"api_key": "..."}
│   └── devto_strategy.json # 发布时间/标签池/标题模板
└── state/
    ├── published.json    # 发布记录（文件名去重）
    └── devto_stats.json  # 数据历史快照
```

## 文章格式（frontmatter 规范）

```markdown
---
title: "Your Title Here"          # 标题（数据钩子式，见策略）
tags: api, data, aso              # 3-4 个标签（前 2 个决定标签页曝光）
series: FoxData API in Practice   # 系列名（站内互链基础）
scheduled: 2026-08-21             # 本地调度日期（发布时自动剥离）
published: false
---
正文 Markdown（≥1 个代码示例 + 数据表格 + Discussion 引导）
```

**⚠️ 关键陷阱（实测踩坑）**：
- `scheduled` 字段会导致 Dev.to 422（YAML Date 解析错误）——发布时**必须剥离**
- 更新已发布文章：`PUT /articles/{id}`，title/tags/series 用**顶层参数**，body 只传纯正文（**严禁**把整个 frontmatter 文件塞进 body_markdown，会导致文章被重建、标题带引号）
- 去重：按**文件名**记录（内容 hash 在更新后失效，会重复发布）
- frontmatter 解析需剥离引号（`title: "..."` → title 不带引号）

## 发布流程

```bash
cd /mnt/user-data/workspace/devrel-automation
# 1) 写草稿到 content/articles/*.md
# 2) 生成计划 + 发布（到期自动发，间隔保护+去重+失败不重试）
python3 create_plan.py && python3 daily_post.py
# 或一键：
python3 auto.py all
```

## AI 运营引擎（提升曝光核心）

```bash
python3 auto.py devto-ops   # monitor → analyze → revive → inject → report
```

| 模块 | 功能 |
|---|---|
| monitor | 拉取全部文章数据，存 30 次历史快照 |
| analyze | 互动率、标签归因、24h 低曝光告警、策略建议 |
| **revive** | **低曝光自动救活**：24h+ 且 views<100 的文章，自动用「数据点 + 原标题核心」生成新标题并 `update_article` 更新（每篇最多 1 次，记录在 state/devto_revived.json） |
| inject | 未发布草稿**自动注入系列互链 + Discussion 引导**（站内导流） |
| report | 综合互动率 <3% 时自动轮换标签组合（自我进化） |

## 内容策略（提升曝光）

**标题模板**（数据钩子 > 产品介绍）：
1. `{insight}，但{contrast}` — "Temu 关键词数是 Shopee 的 2.3 倍，但只排第 3"
2. `{minutes} 分钟搭一个{thing}（{n} 个 API 端点）`
3. `排名第 {rank} 的 App，正在{action}`
4. `{market_a} or {market_b}？{data_source}说`

**标签组合**：主标签 `api, data, aso, mobile`（流量+精准）；轮换池 `webdev, productivity, showdev, discuss`
**发布时间**：UTC 13:00-18:00（北京 21:00-02:00）；周末 reader/writer 比高也可发
**频率**：每周 1-2 篇；系列化（每篇互链前文）
**讨论引导**：文末固定 `## Discussion` 抛问题（评论区是 promotion 信号）
**交叉引流**：发布后立即在 X/Bluesky/LinkedIn 发引流短帖（首小时流量影响标签页排序）

## 定时全自动（GitHub Actions）

`.github/workflows/publish.yml` 每小时执行：`auto.py all` + `auto.py devto-ops`，凭据走 GitHub Secrets（DEVTO_API_KEY），状态文件提交回仓库（跨环境防重）。

## 错误处理速查

| 错误 | 原因 | 处理 |
|---|---|---|
| 422 Title has already been used | 5 分钟重复标题 | 换标题或等待 |
| 422 Tried to load unspecified class: Date | frontmatter 含 scheduled | 发布时剥离该字段 |
| 404 image_uploads | Dev.to 图片上传 API 已失效 | 用图床/手动上传封面 |
| 低曝光告警 | 24h+ views < 100 | 自动 revive 或更新标题/首段 |

## 发布到广场（skills.sh）

```bash
# 推送到 GitHub 仓库后，任何人可安装：
npx skills add benzhang568858050-cell/foxdata-devrel
# 或托管 URL：
npx skills add https://github.com/benzhang568858050-cell/foxdata-devrel/blob/main/skills/devto-operations/SKILL.md
```
