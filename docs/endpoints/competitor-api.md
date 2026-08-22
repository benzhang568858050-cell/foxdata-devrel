# FoxData Competitor API — Discover Competitors for Any iOS & Google Play App

> FoxData API endpoint: `app/competitor` · Region: per-country · Store: iOS App Store / Google Play

## What is the FoxData Competitor API?

The FoxData Competitor API returns the competitive set for any app — detected via app-store similarity signals. It surfaces both obvious rivals and surprising ones (Shopee TH → online marketplaces AND offline retail chains like Lotus's, Big C, Makro).

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/competitor",
    json={"appId": "959841453", "region": "TH"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for c in r.json()["data"]["result"][:10]:
    print(c["title"])
```

## Real data (Shopee TH, 2026-08-20)

| Type | Competitors |
|---|---|
| Online | SHEIN, Temu, Lazada, AliExpress |
| Offline-to-online | Lotus's, Big C PLUS, Makro PRO, Central App, Watsons TH |

Half the competitor set is physical retail that went digital — rankings alone miss this second wave.

## FAQ

### How are competitors detected?

Store similarity signals — keyword overlap, category co-occurrence, user-install patterns.

### Why does an offline retailer appear as a competitor?

Retail chains with aggressive app-first strategies compete for the same shopping journey — the API surfaces them automatically.

### How often does the competitor set change?

Pull monthly; the set shifts with app positioning and category dynamics.
