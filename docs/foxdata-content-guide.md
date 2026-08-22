# FoxData API 内容方向 · 海外平台运营指南

> 目标：围绕 FoxData App Data API（应用商店数据 API）持续产出专业内容，触达 ASO 从业者、移动增长营销、独立开发者与出海团队，实现品牌认知 → 试用转化。
> 配套系统：`bs-automation`（Bluesky/Threads 免费直发）+ `x-automation`（X 直发）

---

## 一、平台匹配分析（谁最适合 FoxData API 内容）

### 主推平台（内容与人群高度匹配）

| 平台 | 匹配度 | 理由 | 发布通道 | 建议频率 |
|---|---|---|---|---|
| **X (Twitter)** | ⭐⭐⭐⭐⭐ | ASO/移动增长圈层成熟（#ASO #AppMarketing #MobileGrowth），数据型帖子天然受宠，短平快洞察的完美载体 | 现有 `x-automation` | 每天 1-2 条 |
| **LinkedIn** | ⭐⭐⭐⭐⭐ | API 产品决策者（增长负责人/CMO/出海中高层）聚集地，B2B 转化率最高；适合长文干货 + CTA | Postiz 或官方 API（待接入） | 每周 1-2 条 |
| **Bluesky** | ⭐⭐⭐⭐ | 开发者/技术人群密度高、内容生态早期红利、官方 API 免费零门槛 | `bs-automation`（已就绪） | 每天 0-1 条 |

### 辅助平台（补充曝光）

| 平台 | 匹配度 | 定位 | 说明 |
|---|---|---|---|
| **Threads** | ⭐⭐⭐ | 品牌存在感 + 简单数据梗图 | 大众流量，硬核 API 内容效果一般；`bs-automation` 已支持 |
| **Reddit** | ⭐⭐⭐ | r/ASO、r/AppStoreOptimization、r/marketing、r/SideProject 发数据洞察帖 | 注意 subreddit 推广规则：发"数据发现"而非广告，评论区自然引流 |
| **Product Hunt** | ⭐⭐ | API 上新/大版本更新时发布 | 低频节点型投放 |
| **技术社区** | ⭐⭐ | 技术向教程（"用 Python 调 FoxData API 做面板"） | 可选 |

### 内容语气建议
- 英文为主（受众全球化），**避免中文直译腔**
- 账号人格：数据驱动的移动市场观察者（"data-first, opinion-second"），比纯厂商号可信度高 3 倍

---

## 二、内容类型模板（6 种可复用）

### T1 数据洞察帖（占比 40%）——主力内容
```
[市场] [时间] [现象/排名变化] + [1 个反直觉发现] + 数据来源
示例：泰国购物榜 Shopee #1 / SHEIN #2 / Temu #3，但 Temu 关键词覆盖 16.8K > Shopee 7.4K
```

### T2 关键词情报帖（占比 20%）
```
[国家 A vs 国家 B] 搜索指数对比 + 业务建议（预算重分配/新市场判断）
示例：'game' 指数 VN 76 vs TH 70 → 越南搜索需求更强
```

### T3 API 干货帖（占比 15%）——转化主力
```
"用 FoxData API 做 X 的 N 个端点/步骤"（不硬广，教方法，文末自然带链接）
```

### T4 榜单周报（占比 10%）——周期性栏目
```
每周一固定栏目：#SEAAppWatch —— 东南亚 3 国下载/收入榜 Top10 变化
```

### T5 竞品拆解（占比 10%）
```
某 App 的排名曲线 + 发版节奏 + 关键词策略复盘（get_app_rank + get_app_version_info + get_app_coverage_keywords）
```

### T6 产品更新（占比 5%）
```
FoxData API 新功能/数据范围更新（官方信息，需人工确认后发布）
```

---

## 三、数据源 → 内容映射（foxdata-aichat 可用接口）

| foxdata-aichat 接口 | 稳定性 | 可产出内容 |
|---|---|---|
| `search_app`（关键词搜应用） | ✅ 稳定 | T1/T2 素材（排名、关键词覆盖量、评分） |
| `get_search_index_ranking`（关键词指数） | ✅ 稳定 | T2 关键词情报（多国家对比） |
| `get_download_ranking`（下载榜） | ✅ 稳定 | T4 榜单周报（含每日趋势） |
| `get_app_competitors`（竞品列表） | ✅ 稳定 | T5 竞品拆解 |
| `get_app_info` / `get_app_reviews` | ✅ 稳定 | T1/T5 细节补充 |
| `get_app_rank` / `get_app_revenue_info` / `get_app_asa_keywords` 等 | ⚠️ 部分可能 500 | 用到时先试，失败降级 |

**内容生产链路（人工/智能体协作）**：
```
调用 foxdata-aichat 拉数据 → 提炼 1 个反直觉洞察 → 生成多平台文案
（Bluesky ≤300 / Threads ≤500 / X ≤270 权重）→ 写入草稿目录 → create_plan + daily_post 自动发布
```

---

## 四、低频内容日历（每周 7-9 条）

| 周一 | 周二 | 周三 | 周四 | 周五 | 周末 |
|---|---|---|---|---|---|
| T4 榜单周报（X + Bluesky） | T2 关键词情报（X） | T3 API 干货（Bluesky + Threads） | T1 数据洞察（X + Bluesky） | T5 竞品拆解（LinkedIn 长文） | 互动/观点（X） |

- X：每天 1 条（`x-automation` 自动）
- Bluesky：每天 0-1 条（`bs-automation` 自动）
- Threads：每周 2-3 条（`bs-automation` 自动）
- LinkedIn：每周 1 条（接入 Postiz 后自动）

---

## 五、注意事项

1. **数据准确性**：所有数字以 foxdata-aichat 实拉为准，发布前标注数据时间（如 "Aug 2026"）；禁止编造数字
2. **合规**：不宣称"官方数据"，用"FoxData API 数据"表述；尊重平台 AI 内容披露政策
3. **推广节奏**：T1/T2 类纯价值内容与 T3/T6 类带链接内容保持 4:1 以上，避免账号被打为营销号
4. **防重复**：同一洞察 7 天内不在多平台重复同文案（内容哈希防重已内置）
5. **数据快照**：每次拉取的原始数据存 `data/raw_YYYYMMDD.json`，便于回溯与周报复用
