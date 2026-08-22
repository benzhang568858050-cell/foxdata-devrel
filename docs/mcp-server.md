# FoxData MCP Server — App Data MCP / ASO MCP / App Market MCP for AI Assistants

> Model Context Protocol (MCP) server for the FoxData App Store Data API (iOS + Google Play). An app data MCP, ASO MCP and app market MCP in one server.

## What is the FoxData MCP Server?

The FoxData MCP Server connects AI assistants (Claude, ChatGPT, Cursor, Codex, and any MCP-compatible agent) directly to the FoxData App Store Data API — **currently deployed for enterprise/internal use** (public release planned). Instead of writing Python/curl calls, you ask in natural language:

> "What are the top 10 shopping apps in Thailand by downloads?"
> "Compare keyword coverage of Shopee vs Temu in TH"
> "What is Shopee's ASA keyword strategy?"

The assistant calls the FoxData MCP tools and returns real store data.

## Configuration

Add to your MCP client config (e.g., `~/.claude.json` / Claude Desktop / Cursor):

```json
{
  "mcpServers": {
    "foxdata": {
      "command": "npx",
      "args": ["-y", "foxdata-mcp"],
      "env": { "FOXDATA_API_KEY": "your-api-key" }
    }
  }
}
```

> Enterprise/internal deployment access: contact hai.zhou@xiaoxitech.com for setup instructions. Public release planned.

## Available tools

| Tool | What it returns |
|---|---|
| `search_app` | Search apps by keyword in a region/store |
| `get_app_info` | Full app metadata: description, developer, version, rating, screenshots |
| `get_app_rank` | Ranking history (FREE/GROSSING) per category |
| `get_download_ranking` | Top apps by download estimates per country |
| `get_revenue_ranking` | Top apps by revenue estimates per country |
| `get_search_index_ranking` | Keyword search demand per region (0-100) |
| `get_app_coverage_keywords` | Keywords an app ranks for |
| `get_app_competitors` | Competitor lists for an app |
| `get_app_rate` | Ratings, star distribution, review velocity |
| `get_app_version_info` | Version history and release cadence |
| `get_app_asa_keywords` | Apple Search Ads bid keywords |
| `get_app_reviews` | App reviews |
| `get_app_developer_apps` | All apps by the same developer |
| `get_global_rank` | Global ranking data |
| `get_realtime_rank_info` | Real-time rank information |
| `get_active_customers_ranking` | DAU/WAU/MAU active user data |

## Example interactions

**Market scan**
```
You: Which SEA country leads gaming app demand?
FoxData MCP: search-index-ranking → game: Vietnam 79, Indonesia 76, Thailand 72
```

**Competitor teardown**
```
You: Who are Shopee Thailand's competitors?
FoxData MCP: get_app_competitors → SHEIN, Temu, Lazada + Lotus's, Big C, Makro...
```

**ASO intelligence**
```
You: What keywords does Shopee bid on in Apple Search Ads?
FoxData MCP: get_app_asa_keywords → shoppee (corr 81), shein (55), 7-Eleven (65)...
```

## Why MCP?

- **Zero code**: natural language access to store data
- **Agent-native**: AI workflows can combine FoxData data with analysis, writing, dashboards
- **Consistent with the API**: same data, same coverage (200+ countries, iOS + Google Play)

## Contact

- **MCP / trial access**: hai.zhou@xiaoxitech.com (or WeChat: `wish_568858050`)
- API docs: https://docs.foxdata.com/
- Product: https://foxdata.com/en/app-data-api/
