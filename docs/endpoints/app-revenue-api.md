# FoxData App Revenue API — Estimate iOS & Google Play Revenue per Country

> FoxData API endpoint: `app/revenue-info` · Region: per-country · Store: iOS App Store / Google Play

## What is the FoxData App Revenue API?

The FoxData App Revenue API returns per-country revenue estimates for apps — covering IAP and subscription monetization (games, subscription apps). Use it for market sizing, monetization benchmarking and update-impact analysis.

## What the data covers

Revenue estimates are modeled from store rankings, review velocity and SDK signals. They fit **IAP-based apps** (games, subscriptions); transaction-based apps (e-commerce, fintech) may return null because their monetization is not IAP.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/revenue-info",
    json={"appId": "YOUR_APP_ID", "regions": ["US", "JP"]},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
print(r.json()["data"]["result"])
```

## Use cases

| Use case | How |
|---|---|
| Game market sizing | Revenue ranking per country |
| Competitor benchmarking | Compare revenue trends across rivals |
| Launch market selection | Revenue + downloads + search index |
| Monetization validation | Revenue-to-download ratio |

## FAQ

### Which apps have revenue data?

IAP-based apps — games, subscription services, paid tools. Transaction-based apps typically show null.

### How accurate are the estimates?

Direction and magnitude, not audited figures. Use relative trends over absolute values.

### Does it include ad revenue?

Generally no — combine with user metrics for ad-supported apps.
