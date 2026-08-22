---
title: "Ad Creative Intelligence: Reverse-Engineering Competitor Campaign Strategy from App Data"
tags: api, aso, ads, data
series: FoxData API in Practice
scheduled: 2026-08-28
published: false
---

# Ad Creative Intelligence: Reverse-Engineering Competitor Campaign Strategy from App Data

> Last updated: 2026-08-22 · Data: FoxData API ASA + search index snapshots

## What is ad creative intelligence?

Ad creative intelligence is the practice of analyzing competitors' advertising activity — which keywords they bid on, which creatives they run, and which channels they favor — to inform your own campaign strategy. FoxData's API service highlights multi-channel ad creatives as part of its data foundation: seeing competitors' creative direction before your next campaign is planned.

## The ASA-based reverse-engineering framework

Since ASA (Apple Search Ads) keyword bidding is observable via API, it is the most direct window into competitor acquisition strategy:

| ASA signal | What it reveals | FoxData endpoint |
|---|---|---|
| Bid keyword list | Target user segments | app-asa-keywords |
| Correlation score | Bid aggressiveness | app-asa-keywords |
| Competitor brand bids | Competitive intercept plays | app-asa-keywords |
| Cross-category bids | Category expansion intent | app-asa-keywords |

## Worked example: what Shopee's ASA portfolio reveals

From the 2026-08-20 snapshot, Shopee TH bids on:

- Own misspellings (shoppee corr 81) — defensive capture of typo traffic
- Competitor brands (shein corr 55) — intercepting rival searches
- Cross-category (7-Eleven corr 65, Starbucks 60) — omni-channel habit capture
- Generic (shop corr 96, shopping corr 78) — category dominance

This portfolio reveals three strategic layers: **defense** (misspellings), **offense** (competitor brands), and **expansion** (cross-category). A competitor watching only Shopee's shopping-category rank misses this entire acquisition playbook.

## Building your creative intelligence loop

```python
import requests

API = "https://api.foxdata.com/apiv1/open-api"
headers = {"x-openapi-key": "<YOUR_LICENSE>"}

r = requests.post(f"{API}/app/asa-keywords",
                  json={"appId": "959841453", "region": "TH"},
                  headers=headers)
for kw in r.json()["data"]["result"]:
    corr = kw.get("corr", 0)
    if corr > 40:
        print(f"{kw['keyword']:30s} corr={corr}")
```

Run weekly per competitor. Track: new keywords appearing, correlation shifts (budget changes), and cross-category entries (expansion signals).

## FAQ

### What is ad creative intelligence?

The analysis of competitors' ad activity — keywords, creatives, channels — to inform your own campaigns. In app marketing, ASA bidding data is the most observable signal.

### Can I see competitor ad keywords via API?

Yes — the FoxData ASA keywords endpoint returns bid keywords and correlation scores per app per region.

### What does a high correlation score mean?

Correlation (0-100) reflects bid strength. Above 60 suggests aggressive bidding; 40-60 is presence-bidding (cheaper intercept); below 40 is experimental.

### Why do competitors bid on their own misspellings?

Misspelling keywords convert 2-3x better than generic terms — the user's intent is unambiguous. Not bidding lets competitors capture your high-intent typo traffic.

### How often should I track ASA portfolios?

Weekly. Bid portfolios shift with campaigns and seasons; a monthly check misses budget shifts.

## Discussion

Have you used ASA keyword data to reverse-engineer competitor strategy? What surprised you most about their bidding patterns? Share below.

Questions or collaboration? Reach me at [benzhang568858050@gmail.com](mailto:benzhang568858050@gmail.com).

---

*Sources: FoxData API (ASA keywords, search index), 2026-08-20. Get API access at [foxdata.com/en/app-data-api](https://foxdata.com/en/app-data-api/).*


> ⭐ **Star this project on GitHub** — it builds this content automatically.

## More from this series

- [Sea App Market Watch](https://dev.to/_a29a85391c475e16a6bed4/building-a-southeast-asia-app-market-watch-with-the-foxdata-api-420i)
- [Vn Vs Th Market](https://dev.to/_a29a85391c475e16a6bed4/vietnam-vs-thailand-where-should-your-app-marketing-budget-go-in-2026-1e6d)
- [Api Vs Scraper](https://dev.to/_a29a85391c475e16a6bed4/app-data-api-vs-building-your-own-scraper-which-is-cheaper-in-2026-4pe7)
- [Shopee Real Competitors](https://dev.to/_a29a85391c475e16a6bed4/shopees-real-competitors-arent-shein-or-temu-the-data-says-lotuss-and-big-c-2696)
