---
name: x-automation
description: X（Twitter）账号自动化运营系统（矩阵版）。当用户提到「X自动化运营」「X账号运营」「X发帖」「X养号」「X图文」「Twitter自动化」「发推」「自动发帖到X」「X账号状态」「X运营配置」等任何与 X/Twitter 账号自动化运营相关的需求时，必须使用本技能。覆盖：自动/手动发帖、图文发布、热点话题结合、养号（点赞/关注）、发布计划、账号状态查询、配图、矩阵联动（引流草稿/统一防重/限频）、错误处理（配额/重复/超长）、外部任务桥接部署。
---

# X 账号自动化运营系统（x-automation · 矩阵版）

基于 cookies 网页端 API（twikit）实现发帖/图文/点赞/关注，无需付费 API。**已融入多平台矩阵**：与 Dev.to/GitHub 共享草稿池、发布状态与限频规则。

## 系统位置（矩阵版）

所有代码与数据：`/mnt/user-data/workspace/devrel-automation/`（持久工作区 + GitHub 备份）

| 文件 | 职责 |
|---|---|
| `clients/x_client.py` | X API 客户端：post_tweet（含图文）、upload_media、favorite_tweet、follow_user、get_trends、verify（twikit，cookies 方案） |
| `clients/x_matrix_bridge.py` | **外部任务桥接**：publish（草稿池发帖，去重+限频）/ warmup（养号）/ status |
| `clients/warmup.py` | 养号：点赞 8-15/天 + 关注 1-3/天，25-90s 随机间隔，每日限频去重 |
| `clients/collect_hotspots.py` | X 实时趋势采集 → `posts/HOTSPOTS.md`（选题源） |
| `create_plan.py` | 统一计划：X 短帖 0-2 条/天随机时间 + Dev.to 到期检测 |
| `daily_post.py` | 按计划发布；**Dev.to 发布成功自动生成 x-promo-*.txt 引流草稿** |
| `config/settings.json` | 运营配置（x.enabled / 条数 / 窗口 / 间隔） |
| `posts/drafts/` | X 草稿池（每个 .txt 一篇；x-promo-* 为矩阵引流草稿） |
| `posts/images/` | 配图库（自动随机搭配） |
| `state/published.json` | 发布记录（**全平台统一防重，按文件名**） |
| `state/warmup.json` | 养号记录（每日限频） |
| `logs/daily.log` | 发布日志 |

## 矩阵联动协议（重要）

1. **草稿池共享**：`posts/drafts/*.txt` 是矩阵统一草稿池——Dev.to 文章发布后自动生成 `x-promo-<文章名>.txt` 引流草稿（标题+链接+标签）
2. **统一防重**：`state/published.json` 的 `x` 数组按 **draft 文件名**去重；任何环境（沙箱/外部任务）发帖后必须回写
3. **限频共享**：每日 ≤5 条、间隔 ≥45 分钟；养号额度在 warmup.json（外部任务共用）
4. **GitHub 同步**：状态文件随仓库同步（每天 3 次 Actions + 外部任务可 pull/push），跨环境防重
5. **外部任务接入**：见 `docs/x-matrix-integration.md`（最小协议）与 `docs/x-bridge-deploy.md`（桥接脚本部署）

## 常用操作

### 1. 验证登录态

```bash
cd /mnt/user-data/workspace/devrel-automation && python3 -c "from clients.x_client import verify; verify()"
```
输出 `X 登录 OK：user_id=...` 即正常。失败时请用户用 Chrome 的 Cookie-Editor 重新导出 cookies，覆盖 `config/x_cookies.json`。

### 2. 立即发布一条帖子

1. 用 write_file 写草稿到 `posts/drafts/任意名.txt`（≤270 权重：中文×2 其他×1，即中文约 135 字上限）
2. 生成计划：`python3 create_plan.py`（随机 0-2 条，24h 窗口；如需立即发，把计划 json 中该条 `time` 改为过去时间）
3. 发布：`python3 daily_post.py`

### 3. 图文发布

- `create_plan.py` 自动以 60% 概率从 `posts/images/` 配图池随机配图（≤5MB，建议 16:9 或 1:1）
- 手动指定：编辑计划 json 的 `images` 字段为图片路径列表
- 技术链路：twikit upload_media（wait_for_completion）→ create_tweet(media_ids)

### 4. 结合热点

- `python3 clients/collect_hotspots.py` 刷新热点（X 实时趋势 → `posts/HOTSPOTS.md`）
- 生成内容前先读 `posts/HOTSPOTS.md`，用 ipipgo-search 搜索当日 AI/科技热点补充，把 1-2 个热点融入帖子开头或论据
- `create_plan.py` 自动在帖尾注入标签（权重检查防超限）

### 5. 养号（点赞 + 关注）

```bash
python3 clients/warmup.py   # 或外部环境用桥接: python3 clients/x_matrix_bridge.py warmup
```
每天点赞 8-15 次、关注 1-3 人，间隔 25-90 秒随机，自动去重与每日限频。
**注意：养号仅在固定 IP 环境运行**（家庭网络/固定服务器），勿放 GitHub Actions 或动态 IP 环境。

### 6. 查看运营状态

```bash
python3 clients/x_matrix_bridge.py status   # 已发布数/草稿池/待发布
cat state/published.json                    # 全平台发布记录
cat state/warmup.json                       # 养号记录
tail -20 logs/daily.log                     # 发布日志
```

### 7. 外部任务桥接（方式 A）

在外部环境（本地电脑/服务器）部署后定时执行：
```bash
python3 clients/x_matrix_bridge.py publish   # 每小时检查发帖（去重+限频）
python3 clients/x_matrix_bridge.py warmup    # 每天 1 次养号（固定 IP）
```
部署细节见 `docs/x-bridge-deploy.md`。

## 关键限制与错误处理

| 错误码 | 含义 | 处理 |
|---|---|---|
| 344 | 每日发帖配额用尽（低活跃账号约 7-10 条/天，UTC 重置） | 当天停止发帖，次日自动恢复；已记录 failed 不重试 |
| 187 | 重复内容（相同文本） | 草稿已按文件名归档防重；需换文案 |
| 186 | 超 280 权重 | 压缩文本（中文×2，控制 ≤270） |
| 226 | 快速连发触发风控 | 间隔 ≥45 分钟（post_gap_min 已内置） |
| 401 | 登录失效 | 重新导出 cookies 覆盖 config/x_cookies.json |

要点：
- 中文每字权重 2、英文 1；280 上限，安全线 270
- daily_post 输出「本轮跳过发布」是 45 分钟间隔保护，正常
- 不删除 `state/published.json` 记录（防重复发布）
- cookies 等同账号钥匙：不写入任何对外汇报，有效期约 1 年
- **矩阵铁律**：发帖前查 published.json（文件名去重）；发完回写状态；勿超每日 5 条

## 配置调整

`config/settings.json`：
- `x.enabled`：X 通道开关（默认 true）
- `x.min_per_day` / `x.max_per_day`：每日帖子数（默认 0-2）
- `window_hours`：随机发布窗口（默认 24 小时）
- `post_gap_min`：相邻帖子最小间隔（默认 60 分钟）
- `image_prob`：配图概率（默认 0.6）

## 配图库扩充

向 `posts/images/` 添加任意 png/jpg 即自动进入配图池（可用 image-generation 生成统一风格的出海主题插画）。

## 文档索引

- `docs/matrix-architecture.md` —— 多平台矩阵架构
- `docs/x-matrix-integration.md` —— 外部任务联动协议（方式 A/B/C）
- `docs/x-bridge-deploy.md` —— 桥接脚本部署指南（cron/风控/状态同步）
