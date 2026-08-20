# X 自动发帖养号任务 · 矩阵联动接入指南

> 目标：让外部的 X 自动发帖/养号任务与 devrel 矩阵联动，共享草稿池、发布状态和限频规则。
> 联动不依赖特定环境：所有共享数据在 **GitHub 仓库**（benzhang568858050-cell/foxdata-devrel）和本地目录中。

## 一、共享资产（联动接口）

| 资产 | 路径 | 说明 |
|---|---|---|
| **X 草稿池** | `posts/drafts/*.txt` | 矩阵生产的短帖（含 `x-promo-*.txt` 引流草稿：Dev.to 文章发布后自动生成） |
| **发布状态** | `state/published.json` | 全平台发布记录，`x` 数组按 **draft 文件名**去重 |
| **养号状态** | `state/warmup.json` | 每日点赞/关注计数与已处理列表（限频依据） |
| **X 客户端** | `clients/x_client.py` | twikit 封装：`post_tweet(text, image_paths)` / `verify()` |
| **养号模块** | `clients/warmup.py` | 点赞 8-15/天 + 关注 1-3/天，间隔 25-90s |
| **计划文件** | `plans/plan_*.json` | 已排期的发布计划（时间、草稿、配图） |

## 二、联动规则（必须遵守）

1. **发帖前查重**：检查 `state/published.json` 的 `x` 数组——`draft` 文件名已存在则跳过
2. **每日限频**：X 每日发帖 ≤5 条（矩阵计划已控制在 0-2 条）；养号额度见 warmup.json
3. **间隔保护**：相邻发帖间隔 ≥45 分钟（`post_gap_min`）
4. **回写状态**：发帖成功后立即追加到 `published.json` 的 `x` 数组（`draft`/`published_at`/`url`），并同步到 GitHub
5. **权重限制**：文案 ≤270 权重（中文×2 其他×1）
6. **养号身份**：养号只在固定 IP 环境运行（**不要**放 GitHub Actions 或频繁切换 IP 的环境）

## 三、快速接入（外部任务三选一）

### A. 直接调用桥接脚本（推荐）

```bash
# 在任务环境（有代码的机器）：
python3 clients/x_matrix_bridge.py publish   # 读草稿池 → 发 1 条未发布的 → 回写状态
python3 clients/x_matrix_bridge.py warmup    # 执行养号（限频保护）
python3 clients/x_matrix_bridge.py status    # 查看联动状态
```

### B. 自己实现（最小协议）

```python
# 1) 拉最新状态（本地或 GitHub raw）
# 2) 挑草稿：posts/drafts/ 中文件名不在 published.json.x 里的
# 3) 发帖（任选实现：twikit / 自有 cookies 方案）
# 4) 回写：
#    published.json.x.append({"draft": 文件名, "published_at": now, "url": ...})
# 5) 推回 GitHub（git pull --rebase && git push）
```

### C. 在 DeerFlow 平台另一个线程中联动

告诉那个对话线程：
> "读取 GitHub 仓库 benzhang568858050-cell/foxdata-devrel 的 posts/drafts/ 作为 X 草稿池，
> 按 state/published.json 的 x 数组去重，发帖后用 x_matrix_bridge.py 或按最小协议回写状态。"

## 四、引流联动流程（自动发生）

```
Dev.to 文章发布成功（矩阵 daily_post）
  → 自动生成 x-promo-<文章名>.txt（X 引流草稿，≤270 权重）
  → 进入 posts/drafts/ 草稿池
  → 你的 X 任务下次运行时自然发到 X（去重+限频保护）
  → 回写状态 → 全矩阵防重
```

## 五、状态文件格式

```json
{
  "x": [
    {"draft": "th-keyword-war.txt", "published_at": "2026-08-21T08:00:00", "url": "https://x.com/i/status/xxx"}
  ],
  "devto": [...],
  "ph": []
}
```
