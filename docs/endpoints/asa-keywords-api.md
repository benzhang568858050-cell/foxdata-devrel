# FoxData ASA Keywords API — Apple Search Ads Bid Keywords for Any App

> FoxData API endpoint: `app/asa-keywords` · Region: per-country · Store: iOS App Store

## What is the FoxData ASA Keywords API?

The FoxData ASA Keywords API reveals which keywords an app is bidding on in Apple Search Ads, with correlation scores (0-100) reflecting bid strength. Reverse-engineer competitor acquisition strategy: target segments, brand intercepts, and category expansion plays.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/asa-keywords",
    json={"appId": "959841453", "region": "TH"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for kw in r.json()["data"]["result"]:
    if kw.get("corr", 0) > 40:
        print(kw["keyword"], kw["corr"])
```

## Real data (Shopee TH, 2026-08-20)

| Keyword | Correlation | Strategy |
|---|---|---|
| shop | 96 | Category dominance |
| shoppee | 81 | Misspelling defense |
| 7 eleven | 65 | Offline retail intercept |
| starbucks thailand | 60 | Lifestyle adjacency |
| shein | 55 | Competitor intercept |

## FAQ

### What does the correlation score mean?

Correlation (0-100) reflects bid strength: >60 aggressive, 40-60 presence-bidding, <40 experimental.

### Why bid on own misspellings?

Misspelling keywords convert 2-3x better — the user's intent is unambiguous.

### How often should I pull ASA portfolios?

Weekly — bid portfolios shift with campaigns and seasons.
