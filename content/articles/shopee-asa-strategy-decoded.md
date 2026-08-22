---
title: "Shopee's ASA Strategy: Bidding on Shein, 7-Eleven and Starbucks — Apple Search Ads Decoded"
tags: api, asa, aso, data
series: FoxData API in Practice
scheduled: 2026-08-24
published: false
cover_image: https://raw.githubusercontent.com/benzhang568858050-cell/App-data-IOS-GP-/main/assets/covers/shopee-asa-strategy-decoded.png
---

# Shopee's ASA Strategy: Bidding on Shein, 7-Eleven and Starbucks — Apple Search Ads Decoded

> Last updated: 2026-08-22 · Data: FoxData API ASA keywords endpoint, 2026-08-20

## What is Shopee bidding on in Apple Search Ads?

Shopee Thailand's ASA keyword portfolio reveals a **cross-category competitive bidding strategy**: they bid on competitor brands (Shein, 7-Eleven, Watson, Starbucks), adjacent categories (TikTok Shop, Uber Eats), and their own misspellings (shoppee, soppee). This is a deliberate omni-channel user acquisition play.

## The ASA keyword data

| Keyword | Correlation | Strategy |
|---|---|---|
| shop | 96 | Generic category dominance |
| shoppee | 81 | Own misspelling defense |
| shopping | 78 | Core intent capture |
| 7 eleven / 7-11 | 65-66 | Offline retail intercept |
| watson | 65 | Health/beauty cross-category |
| starbucks thailand | 60 | Lifestyle adjacency |
| shein | 55 | Direct competitor intercept |
| true money | 51 | Fintech wallet intercept |
| scb easy | 49 | Banking app intercept |

Source: FoxData API `app-asa-keywords` endpoint, 2026-08-20. Correlation = bid strength (0-100).

## Dimension 1 — Competitor brand bidding: the intercept play

Shopee bids on "shein" (corr 55) — when a user searches "shein" on the App Store, Shopee's ad appears. This is classic **competitive intercept ASA**. The mid-strength correlation suggests Shopee isn't outbidding SHEIN on its own brand — they're maintaining presence at a lower CPA.

## Dimension 2 — Cross-category bidding: the omni-channel thesis

The most revealing signals are non-shopping keywords: 7-Eleven (corr 65), Watson (65), Starbucks (60), TikTok Shop, Uber Eats. This is a **category expansion strategy** — Shopee competes for the **mobile transaction habit** across categories, not just shopping searches.

## Dimension 3 — Misspelling defense: the invisible moat

| Misspelling | Correlation |
|---|---|
| shoppee | 81 |
| soppee | 51 |
| shoopee | 47 |
| shpee | 40 |

Shopee bids aggressively on its own misspellings (shoppee corr 81 — their highest non-generic correlation). **Misspelling keywords have 2-3x higher conversion rates** because the user's intent is unambiguous.

## What this means for three roles

**For UA teams**: competitor brand bidding is cheaper than generic shopping terms. Start with corr 40-60 keywords.

**For ASO managers**: misspelling defense is non-negotiable. Audit your brand's misspellings and bid on all of them.

**For product strategists**: cross-category ASA reveals where your users overlap with adjacent apps. Use this to inform partnership decisions.

## How to reproduce this analysis

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

## FAQ

### What is Apple Search Ads (ASA)?

Apple Search Ads lets developers bid on keywords to show ads in App Store search results. The FoxData ASA endpoint reveals which keywords an app bids on and bid strength (correlation 0-100).

### How does competitor brand bidding work in ASA?

You bid on a competitor's brand name. When users search for that competitor, your ad appears. It's legal and common — the key is bidding at a correlation that captures intent without overpaying.

### Should I bid on my own misspellings?

Yes — misspelling keywords have 2-3x higher conversion rates than generic terms because intent is unambiguous. Not bidding lets competitors intercept your high-intent users.

### How much does ASA cost?

ASA uses a CPC auction model. Competitor brand terms are typically cheaper than generic category terms. FoxData's correlation score helps estimate relative bid strength.

### Can I see which keywords my competitors bid on?

Yes — the FoxData ASA keywords endpoint returns bid keywords and correlation scores for any app in supported regions.

## Discussion

Are you bidding on competitor brands in Apple Search Ads? What's your experience with misspelling defense? Share your ASA strategy below.

Questions or collaboration? Reach me at [benzhang568858050@gmail.com](mailto:benzhang568858050@gmail.com).

---

*Sources: FoxData API ASA keywords endpoint, 2026-08-20. Get API access at [foxdata.com/en/app-data-api](https://foxdata.com/en/app-data-api/).*


> ⭐ **Enjoy this data? [Star the project on GitHub](https://github.com/benzhang568858050-cell/App-data-IOS-GP-) — it builds this content automatically.**

## More from this series

- [Sea App Market Watch](https://dev.to/_a29a85391c475e16a6bed4/building-a-southeast-asia-app-market-watch-with-the-foxdata-api-420i)
- [Vn Vs Th Market](https://dev.to/_a29a85391c475e16a6bed4/vietnam-vs-thailand-where-should-your-app-marketing-budget-go-in-2026-1e6d)
- [Api Vs Scraper](https://dev.to/_a29a85391c475e16a6bed4/app-data-api-vs-building-your-own-scraper-which-is-cheaper-in-2026-4pe7)
- [Shopee Real Competitors](https://dev.to/_a29a85391c475e16a6bed4/shopees-real-competitors-arent-shein-or-temu-the-data-says-lotuss-and-big-c-2696)
