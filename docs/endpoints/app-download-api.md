# FoxData App Download API — Get Download Estimates for iOS & Google Play

> FoxData API endpoint: `app/download-ranking` · Region: per-country · Store: iOS App Store / Google Play

## What is the FoxData App Download API?

The FoxData App Download API returns per-country download estimates for apps on the iOS App Store and Google Play. Call it with an app ID and region, get back download rankings and daily download estimates — the foundation for market sizing, UA budgeting and competitor tracking.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/download-ranking",
    json={"region": "TH", "category": "-1", "date": "2026-08-20"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for app in r.json()["data"]["result"][:5]:
    print(app["title"], app.get("trend"))
```

## Real data example (2026-08-20, Thailand)

| Rank | App | Weekly downloads |
|---|---|---|
| 1 | X | 21,175 |
| 2 | Earthquake alerts | 3,078 |
| 3 | TradingView | 2,750 |

## FAQ

### How accurate are FoxData download estimates?

Modeled from store rankings, review velocity and SDK signals — use for trends and relative comparison.

### Can I get daily download trends?

Yes — the endpoint returns trend arrays per app per day.

### Which regions are covered?

200+ countries, including SEA (TH/VN/ID), US, JP, KR and EU markets.
