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
