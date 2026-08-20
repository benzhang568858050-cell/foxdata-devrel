---
title: "Shopee's Real Competitors Aren't SHEIN or Temu — The Data Says Lotus's and Big C"
tags: api, aso, data, ecommerce
series: FoxData API in Practice
scheduled: 2026-08-21
published: false
---

# Shopee's Real Competitors Aren't SHEIN or Temu — The Data Says Lotus's and Big C

> Data: FoxData API snapshot, 2026-08-20. Competitor lists from the FoxData API `competitor` endpoint.

Conventional wisdom says Shopee's battlefield is SHEIN, Temu and Lazada. But the FoxData API's competitor data tells a different story.

Here's what Shopee Thailand's competitor list actually looks like:

**Online-first players:** SHEIN, Temu, Lazada, AliExpress

**Offline giants (the surprise):** Lotus's, Big C PLUS, Makro PRO, Central App, Watsons TH, Kaidee, Konvy

Half of Shopee's detected competitors are **physical retail chains that went digital**. That's not a coincidence — it's a structural shift.

## What the data actually means

### 1. E-commerce has become omni-channel retail warfare

Lotus's (hypermarket chain) and Big C (supermarket chain) both run aggressive app-first strategies in Thailand: same-day delivery, membership pricing, store-pickup. Their apps sit permanently in the shopping category top ranks:

| App | Shopping rank (Aug 2026) | Type |
|---|---|---|
| Shopee | 1 | Pure e-commerce |
| SHEIN | 2 | Cross-border fashion |
| Temu | 3 | Cross-border marketplace |
| Lazada | 4 | Pure e-commerce |
| Lotus's | Top 20 (rising) | Retail chain app |
| Big C PLUS | Top 20 (rising) | Retail chain app |

**If you only watch the top 4, you miss the entire second wave** — the retailers who already own the customer relationship offline and are now attacking the same shopping journey online.

### 2. For competitor monitoring, category charts lie

A pure "shopping category" ranking hides retail-chain competitors because they're often classified differently or rank lower. The `competitor` endpoint — which uses app-store similarity signals — surfaces them automatically.

This is the case for monitoring tools: **rankings show the scoreboard; competitor lists show who's actually on the field.**

### 3. The practical takeaway for app marketers

- If you compete with Shopee in Thailand, your threat model is wrong if it only includes marketplaces. **Monitor Lotus's, Big C and Makro the same way you monitor Temu.**
- These chains have offline distribution advantages — expect them to invest heavily in app retention mechanics (membership, delivery speed), not just acquisition.
- For other SEA markets, run the same analysis: the `competitor` endpoint is one POST away.

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/competitor",
    json={"appId": "959841453", "region": "TH"},   # Shopee TH
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for c in r.json()["data"]["result"][:10]:
    print(c["title"])
```

## Discussion

Are you tracking offline-to-online retail apps in your market? What did the data show that surprised you? Share in the comments — I'll pull deeper data for the most-requested markets.

---

*Sample data from FoxData API snapshot, 2026-08-20. Get API access at foxdata.com/app-data-api.*

*Built with the open-source [foxdata-devrel automation hub](https://github.com/benzhang568858050-cell/foxdata-devrel) ⚡ — data → content → publishing, fully automated.*

## More from this series

- [Sea App Market Watch](https://dev.to/_a29a85391c475e16a6bed4/building-a-southeast-asia-app-market-watch-with-the-foxdata-api-420i)
- [Vn Vs Th Market](https://dev.to/_a29a85391c475e16a6bed4/vietnam-vs-thailand-where-should-your-app-marketing-budget-go-in-2026-1e6d)
