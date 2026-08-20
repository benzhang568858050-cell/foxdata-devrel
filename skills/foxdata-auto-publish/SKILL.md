---
name: foxdata-auto-publish
description: FoxData 数据内容自动化发布系统操作指南。当用户提到「FoxData 内容运营」「API 数据内容自动发布」「一键发布到 X/Dev.to」「用 foxdata 数据发帖」「FoxData 自媒体自动化」「数据洞察内容」等需求时，必须使用本技能。覆盖：FoxData 官方 API 拉数、foxdata-aichat MCP 数据通道、数据快照、多平台文案生成、X/Dev.to/Product Hunt/Bluesky/Threads 发布、一键自动化（auto.py）、GitHub Actions 定时调度。
---

# FoxData 内容自动化发布系统（foxdata-auto-publish）

基于 FoxData Open API + foxdata-aichat MCP + 多平台发布客户端的**最简自动化方案**：一条命令完成「拉数据 → 内容 → 发布」。

## 系统位置

- 主系统：`/mnt/user-data/workspace/devrel-automation/`
- 轻量发布：`/mnt/user-data/workspace/bs-automation/`（Bluesky + Threads）
- 完整指南：`docs/setup-guide.md`（凭据获取）、`docs/foxdata-content-guide.md`（内容策略）

## 数据通道（数据获取需要 FoxData 付费订阅）

> ⚠️ 重要：FoxData 数据服务（Open API 与 foxdata-aichat MCP）均为**只读查询**，且需要付费订阅
> （API Solutions 计划，$59/月起，按调用次数/积分计费）。**MCP 不能发布内容**——发布走各平台官方 API（Dev.to 等免费）。

| 通道 | 配置 | 说明 |
|---|---|---|
| **FoxData 官方 Open API** | `config/foxdata_creds.json` → `{"x_openapi_key": "..."}`（Base: `https://api.foxdata.com/apiv1/open-api`，Header `x-openapi-key`） | 付费订阅后脚本完全自主拉数 |
| **foxdata-aichat MCP** | 对话内调用（MCP 工具） | 只读查询接口，消耗订阅配额/积分，拉完存 `data/raw_latest.json` 供后续使用 |

无订阅时：内容素材可用公开数据/人工整理代替，或等订阅开通后再启用自动拉数。

官方 API 要点（见 https://docs.foxdata.com/）：
- 端点示例：`POST /app/app-info`（body: appId/region/language）
- 分页：响应 `data.next` → `GET /common/next-page?taskId=&pageKey=`
- 错误码：401 缺 key / 403 key 无效 / 429 限流 / 60003 日配额 / 60005 积分不足 / 60008 无数据
- 脚本已内置重试与翻页（`clients/foxdata_client.py`）

## 一键自动化（核心用法）

```bash
cd /mnt/user-data/workspace/devrel-automation
python3 auto.py all      # 全链路：fetch(拉数据) → plan(生成计划) → publish(发布)
python3 auto.py status   # 各平台凭据与内容状态总览
python3 auto.py fetch    # 只拉数据（需 FoxData 订阅；无 key 时跳过）
```

## 内容生产流程（本技能的核心价值）

1. **拉数据**：官方 API（有 key）或对话中调用 foxdata-aichat MCP（search_app / get_search_index_ranking / get_download_ranking / get_app_competitors 为稳定接口）→ 存 `data/raw_latest.json`
2. **生成内容**（英文为主，直接写入草稿目录）：
   - X 短帖 → `posts/drafts/*.txt`（≤270 权重：中文×2 其他×1，带 1-2 个标签）
   - Dev.to 长文 → `content/articles/*.md`（frontmatter: title/tags/series/scheduled）
   - Product Hunt 更新 → `content/ph/*.json`（slug/name/tagline/description/url/scheduled）
   - Bluesky/Threads（可选）→ `bs-automation/posts/drafts/*.txt`（≤300 字符）
3. **内容配比**：数据洞察 40% / 关键词情报 20% / API 干货 15% / 榜单周报 10% / 竞品拆解 10% / 产品更新 5%
4. **发布**：`auto.py all`（有凭据的平台自动发布，其余跳过；间隔保护 60 分钟 + 内容哈希防重复 + 失败不重试）

## AI 运营引擎（自动提升曝光）

`python3 auto.py devto-ops` 一键运行（已接入 GitHub Actions 每小时自动执行）：

- **monitor**：拉取全部文章数据存历史（state/devto_stats.json）
- **analyze**：互动率、标签归因、24h 低曝光告警、发布策略建议
- **inject**：未发布草稿自动注入「系列互链 + Discussion 讨论引导」（站内导流）
- **report**：综合互动率偏低时自动轮换标签组合（策略文件 config/devto_strategy.json）

策略文件可调：best_hours_utc（发布时间窗口，默认 UTC 13-18）、tag_pool（标签池）、title_templates（标题模板，内容工厂生成文章时套用）。

注意：Dev.to 无评论/点赞/关注的写 API → 互动类动作无法全自动；曝光运营（发布节奏/互链/SEO/数据驱动选题）已全自动。

## 常用命令

```bash
python3 create_plan.py     # 生成今日计划（X 每天 0-2 条随机时间 + Dev.to 到期检测）
python3 daily_post.py      # 发布到期内容
python3 clients/github_client.py readme   # 更新仓库 README 索引
tail -20 logs/daily.log    # 查看日志
cat state/published.json   # 发布记录
```

## GitHub Actions 定时（可选，免费 cron）

1. 推仓库到 GitHub（公开仓库兼作内容门面）
2. Settings → Secrets：`X_COOKIES` / `DEVTO_API_KEY` / `PH_TOKEN`（凭据不进仓库）
3. `.github/workflows/publish.yml` 每小时自动跑 `auto.py` 并回写状态
4. `state/published.json` 保留在仓库内（跨环境防重）

## 凭据获取速查

| 平台 | 获取方式 | 配置文件 |
|---|---|---|
| FoxData API | FoxData 个人中心/销售订阅后获取 License | `config/foxdata_creds.json` |
| X | Cookie-Editor 导出登录 cookies | `config/x_cookies.json` |
| Dev.to | Settings → Extensions → API Keys | `config/devto_creds.json` |
| Product Hunt | ph 创建产品页 → v2/oauth/applications 拿 token | `config/ph_creds.json` |
| Bluesky/Threads | bsky 设置 App Password / Meta 开发者 token | `bs-automation/config/*` |

## 关键限制与错误处理

| 情况 | 处理 |
|---|---|
| 无 x_openapi_key（未订阅） | 跳过自动拉数；素材改用公开数据/人工整理，或开通 FoxData API 订阅 |
| X 权重 >270 | 压缩文案（中文×2 权重） |
| Dev.to scheduled 未到期 | 计划不包含该文章（正常） |
| 发布失败 | 自动记日志不重试；检查凭据有效性 |
| GitHub Actions 中文文件名 | 用英文文件名（中文转义问题） |
