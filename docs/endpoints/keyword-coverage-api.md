# FoxData Keyword Coverage API — iOS & Google Play Keyword Research

> FoxData API endpoint: `app/coverage-keywords` · Device: IPHONE / IPAD · Store: iOS App Store / Google Play

## What is the FoxData Keyword Coverage API?

The FoxData Keyword Coverage API returns the list of keywords an app ranks for in the app store — the core ASO asset. Compare keyword coverage across competitors to find gaps and opportunities (e.g., Temu 16,843 keywords vs Shopee 7,403 in Thailand).

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/coverage-keywords",
    json={"appId": "959841453", "region": "TH", "device": "IPHONE"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for kw in r.json()["data"]["result"][:20]:
    print(kw["keyword"])
```

## Real data sample (Shopee TH)

The coverage list includes competitor brands (shein, lotus's), adjacent categories (tiktok, spotify), misspellings (shoppee, soppee) and utility terms — each one a search entry point.

## FAQ

### What is keyword coverage?

The number of search terms an app ranks for in the store. More coverage = more search appearances.

### How do I find keyword gaps?

Set-difference your coverage vs competitors, then prioritize by search index (see the search-index endpoint).

### How often should I pull coverage?

Monthly for trend tracking; the list shifts with metadata changes and ASA campaigns.
