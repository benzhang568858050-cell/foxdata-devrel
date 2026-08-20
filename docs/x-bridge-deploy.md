# X 桥接脚本部署指南（方式 A）

> 在外部环境（本地电脑/服务器）部署 `x_matrix_bridge.py`，与 devrel 矩阵联动发帖+养号。

## 1. 环境要求

```bash
# Python 3.10+
python3 --version

# 安装依赖（脚本所在目录）
pip install twikit requests
```

## 2. 获取代码与凭据

```bash
# 方式一：克隆仓库（推荐，自动同步草稿池）
git clone https://github.com/benzhang568858050-cell/foxdata-devrel.git
cd foxdata-devrel

# 方式二：只复制桥接脚本（如果已有自己的 X 代码）
# 需要: clients/x_matrix_bridge.py + clients/x_client.py
```

**X 凭据**（二选一）：
- `config/x_cookies.json`：Chrome 装 Cookie-Editor → 登录 x.com → 导出全部 cookies（JSON）粘贴进来
- `config/x_creds.json`：`{"auth_info_1": "邮箱/用户名", "password": "密码", "totp_secret": "可选"}`

⚠️ 凭据文件已在 .gitignore 中，不会提交。

## 3. 定时任务配置（crontab 示例）

```bash
crontab -e
```

```cron
# 每小时检查发帖（草稿池有内容才发，自动去重+限频）
17 * * * * cd /path/to/foxdata-devrel && python3 clients/x_matrix_bridge.py publish >> logs/bridge.log 2>&1

# 每天 1 次养号（固定 IP 环境！）——建议随机时段，避免规律性
23 9 * * * cd /path/to/foxdata-devrel && python3 clients/x_matrix_bridge.py warmup >> logs/bridge.log 2>&1
```

**频率风控建议**：
| 动作 | 频率 | 保护 |
|---|---|---|
| 发帖 | 每小时检查一次，实际每天 ≤5 条 | 脚本内置每日上限 + 45 分钟间隔 |
| 养号 | 每天 1 次（点赞 8-15 + 关注 1-3） | 25-90s 随机间隔 + 每日重置 |
| 引流草稿 | 矩阵自动生成，次日发出 | 与普通草稿同池同规则 |

## 4. 与矩阵同步状态（可选但推荐）

发帖/养号状态存在本地 `state/published.json` + `state/warmup.json`。
**要与 GitHub 仓库同步**（矩阵侧才能看到你发了什么，避免重复）：

```bash
# 每次运行后推送（或加进 crontab）：
cd /path/to/foxdata-devrel
git add -A && git commit -m "sync: bridge state" && git push
# 运行前先拉取（拿到矩阵最新草稿）：
git pull --rebase
```

推荐 crontab 加两条：
```cron
# 运行前拉取最新草稿池
15 * * * * cd /path/to/foxdata-devrel && git pull --rebase -q || true

# 状态回写（publish/warmup 后 5 分钟）
*/30 * * * * cd /path/to/foxdata-devrel && git add -A && git diff --cached --quiet || (git commit -m "sync: bridge state" && git push -q)
```

## 5. 验证

```bash
python3 clients/x_matrix_bridge.py status    # 应显示草稿池与待发布数量
python3 clients/x_matrix_bridge.py publish   # 首条测试发帖
```

## 6. 注意事项

- **养号仅限固定 IP 环境**（家庭宽带/固定服务器）；不要在 GitHub Actions、频繁换 IP 的环境跑 warmup
- 与矩阵的草稿池共享：`x-promo-*.txt` 是 Dev.to 文章发布后自动生成的引流草稿，优先级最高
- 如果已有自己的 X 发帖代码（旧 x-automation），可直接用最小协议接入（见 `docs/x-matrix-integration.md` 方式 B），不必换代码
