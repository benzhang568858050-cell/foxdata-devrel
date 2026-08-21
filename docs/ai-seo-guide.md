# AI-SEO 内容规范（内容工厂必读）

> 目标：让 FoxData 内容在 Google AI Overviews / ChatGPT / Perplexity / Gemini / Copilot 中被检索和引用。
> 依据：AI-SEO 方法论（Princeton GEO 研究 + Google 官方指南 + 多平台实测）。

## 核心数据（为什么这么做）

| 事实 | 数值 |
|---|---|
| Google 搜索显示 AI Overviews 的比例 | ~45% |
| AI Overviews 减少的点击 | 最多 58% |
| 优化内容的被引用率提升 | **3 倍** |
| 引用来源+数据统计的可见度提升 | +40% / +37%（Princeton GEO） |
| 关键词堆砌对 AI 可见度的影响 | **-10%（有害）** |
| 对比类内容在 AI 引用中的占比 | ~33% |

## 三大支柱（每篇内容必须满足）

### 支柱 1：结构可提取（Structure）

| 块类型 | 对应查询 | 规范 |
|---|---|---|
| **定义块** | "What is X?" | 首段 40-60 词直接回答，独立成段（AI 摘取首选） |
| **分步块** | "How to X?" | 编号列表，每步一句话 |
| **对比表** | "X vs Y" | 表格 > 散文（AI 解析表格最强） |
| **数据统计块** | "How many/How much" | 具体数字 + 来源 + **日期** |
| **FAQ 块** | 长尾问题 | H3 自然语言提问（5-8 个），每个 40-60 词独立回答 |

结构规则：
- 每个章节**开头直接给答案**，不铺垫
- H2/H3 用用户真实提问句式（"How much does X cost?" 而非 "费用说明"）
- 表格和编号列表优先于长段落

### 支柱 2：权威可引用（Authority）

- ✅ 每篇带 **Last updated 日期**（新鲜度信号，AI 权重高）
- ✅ 数据必须带**来源 + 日期**（"Source: FoxData API, 2026-08-20"）
- ✅ 引用原创数据（我们独有的 foxdata 快照 = 差异化）
- ✅ 作者署名 + 联系方式（E-E-A-T）
- ✅ 行业术语自然使用（tech terms +18%）
- ❌ 禁止关键词堆砌（-10%）

### 支柱 3：存在感（Presence）

| 渠道 | 状态 |
|---|---|
| GitHub 仓库（llms.txt + README） | ✅ 已配置 |
| Dev.to 文章（高权重域名） | ✅ 发布中 |
| Reddit/Quora 讨论 | ⏳ 可选（真实参与） |
| 第三方对比文章 | ⏳ 后续 |

## 查询扇出（Query Fan-Out）覆盖

每篇主题文章必须覆盖 5-10 个 AI 可能扇出的相关子问题。例：
- 主题"app market data API" → 扇出：best app data API / cost / how accurate / free alternatives / for indie developers / competitor analysis
- 写作时：把这 5-10 个问题作为 FAQ 或小章节

## 深度内容规范 v2（2026-08-21 起强制）

> 方针：SEO/GEO 合规 + foxdata-mcp 多维度数据 + 深度分析。**禁止浅层数据快照文**。

### 深度标准（每篇至少满足 6/8）

| # | 深度维度 | 要求 | 数据来源（foxdata-mcp） |
|---|---|---|---|
| 1 | **多维交叉** | ≥3 个数据维度交叉分析（排名×关键词×评分×版本×竞品） | get_app_rank + get_app_coverage_keywords + get_app_rate + get_app_version_info + get_app_competitors |
| 2 | **时间趋势** | 数据带 7 天+ 趋势变化，分析"变化而非静态" | get_app_rank / get_download_ranking（trend 数组） |
| 3 | **因果链** | 数据 → 原因 → 影响 → 建议（每段至少 2 层因果） | 分析层 |
| 4 | **角色建议** | 分角色落地建议（UA 团队 / ASO 经理 / 产品 / 出海决策者） | 分析层 |
| 5 | **数据可视化** | ≥1 个表格 + 可选图表 | 数据层 |
| 6 | **行业叙事** | 数据放进市场背景（品类竞争格局/区域趋势） | 分析层 |
| 7 | **SEO/GEO 结构** | 定义块 + 提问式 H2/H3 + FAQ 5-8 个 + 来源日期 | AI-SEO 三支柱 |
| 8 | **可操作代码** | ≥1 段可运行 API 示例代码 | get_app_info 等 |

### 写作深度检查清单（发布前自检）

- [ ] 是否有"因为…所以…"的因果推理，而不是罗列数字？
- [ ] 是否至少 3 个数据维度互相印证？
- [ ] 读者读完能否做出一个具体决策（预算/选址/改关键词）？
- [ ] 数据是否带来源和日期？
- [ ] FAQ 是否覆盖 AI 扇出查询？（FAQ = 以疑问词开头的 H3，如 What/How/Is/Which/Does；统计时勿把章节小标题计入）
- [ ] 是否给出可复现的 API 代码？

### 深度与 SEO/GEO 的关系

- **深度 = 引用资格**：AI 引擎引用"信息量大的原创分析"，浅层快照文不会被引用（GEO 核心）
- **深度 = 长尾覆盖**：一篇深度文自然覆盖 10+ 长尾查询（扇出），比 5 篇浅文有效
- **深度 = 差异化**：foxdata 独有数据交叉是别人抄不走的护城河

## 文章类型优先级（引用份额）

1. **对比文章**（~33%）—— 工具对比/方式对比（表格）
2. **原创数据报告**（~12%）—— 我们独有的 foxdata 快照
3. **定义/指南**（~15%）—— What is / How to（AI 最爱摘取）
4. 列表类（~10%）
5. 产品页（~10%）

## 文章模板（必填结构）

```markdown
---
title: "What Is ...? / How to ... / [数据钩子] (2026)"
tags: api, data, aso, ...
series: FoxData API in Practice
scheduled: YYYY-MM-DD
published: false
---
# 标题

> Last updated: YYYY-MM-DD · Data: FoxData API snapshot

## 定义块（40-60 词直接回答核心问题）

## 数据表（来源+日期）

## 章节（H2 用提问句式）

## FAQ（H3 自然语言问题 × 5-8）

## Discussion + 邮箱

---

*Sources: ... | Get API access at [foxdata.com/en/app-data-api](...)*
*Built with the open-source [foxdata-devrel automation hub](...)*
```

## 发布节奏与监控

- 每周 1-2 篇 AI-SEO 结构文章（与现有系列并行）
- 每月用 devto_stats 检查互动率；AI 引用情况可用 Otterly/Peec 或手动查 ChatGPT/Perplexity
- 内容更新：季度刷新旧文（改数据日期、加新数据）

## 机器可读文件（已配置）

- `llms.txt` —— AI 系统上下文（产品、链接、数据样本）
- `data/raw_latest.json` —— 机器可读数据快照
- README 结构清晰（agents 可解析）
