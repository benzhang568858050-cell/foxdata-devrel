# FoxData App Ranking API — Track iOS & Google Play Rankings by Category

> FoxData API endpoint: `app/rank` · Region: per-country · Store: iOS App Store / Google Play

## What is the FoxData App Ranking API?

The FoxData App Ranking API returns app ranking positions over time — overall charts and category charts (FREE / GROSSING) per country. Track rank history, competitor moves, and the impact of version updates or campaigns.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/rank",
    json={"appId": "959841453", "region": "TH",
          "startTime": "2026-08-14", "endTime": "2026-08-20"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for chart in r.json()["data"]["result"]["ranks"]:
    print(chart["chartsType"], chart["categoryId"], chart["data"])
```

## Real data example (Shopee TH, 08-14 to 08-20)

| Date | Overall FREE | Shopping FREE |
|---|---|---|
| 08-14 | 14 | 1 |
| 08-18 | **10** | 1 |
| 08-20 | 11 | 1 |

The overall-chart climb (14 to 10) while holding category #1 signals cross-category user expansion.

## FAQ

### What chart types are available?

FREE, PAID and GROSSING rankings, both overall and per category.

### How far back does rank history go?

Daily rank data for the requested window; historical data is included.

### Can I monitor multiple countries?

Yes — one call per region; loop through your target markets for a global rank watch.
