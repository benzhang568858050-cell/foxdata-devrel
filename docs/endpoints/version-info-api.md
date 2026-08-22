# FoxData Version Info API — App Update History & Release Cadence

> FoxData API endpoint: `app/version-info` · Region: per-country · Store: iOS App Store / Google Play

## What is the FoxData Version Info API?

The FoxData Version Info API returns app version history — release dates, version codes, and changelog summaries. Analyze competitor release cadence and changelog themes to infer product strategy.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/version-info",
    json={"appId": "959841453", "region": "TH"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for v in r.json()["data"]["result"]["version"][:5]:
    print(v["code"], v["date"][:10], v["logs"][:60])
```

## Real data (Shopee TH, 90 days)

| Release window | Versions | Interval |
|---|---|---|
| 5/26 - 6/10 | 3 | ~5 days |
| 6/12 - 6/26 | 4 | ~3-4 days |
| 7/09 - 7/24 | 3 | ~5 days |
| 7/29 - 8/20 | 4 | ~4-7 days |

**14 versions in 90 days** — with search improvements in nearly every changelog.

## FAQ

### What does version cadence tell you?

Release frequency correlates with ASO freshness and re-ranking opportunities — a competitor shipping weekly is structurally faster.

### Can I correlate versions with ratings?

Yes — combine version-info with the rating endpoint: 1-star declines often align with fix releases.

### How far back does version history go?

The endpoint returns version logs for the requested window (default 30 days, up to 90+).
