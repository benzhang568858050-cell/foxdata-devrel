# FoxData Search Index API — App Store Search Demand by Keyword & Region

> FoxData API endpoint: `app/search-index-ranking` · Regions: multi-country · Store: iOS App Store / Google Play

## What is the FoxData Search Index API?

The FoxData Search Index API returns the relative popularity of keywords in the app store per region (0-100 scale). Compare search demand across countries and categories — the leading indicator for market entry and content strategy.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/search-index-ranking",
    json={"regions": ["ID", "VN", "TH"], "keywords": ["game", "shopping", "video"], "store": "AS"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
print(r.json()["data"]["result"])
```

## Real data (2026-08-20)

| Keyword | Indonesia | Vietnam | Thailand |
|---|---|---|---|
| game | 76 | **79** | 72 |
| video | **70** | 53 | 49 |
| shopping | **56** | 47 | 45 |

Indonesia leads commerce/content demand; Vietnam leads gaming — data-backed market entry decisions.

## FAQ

### What is a search index?

A normalized 0-100 measure of how often users search a keyword in the store within a region.

### How does search demand lead downloads?

Search index trends lead download charts by 2-4 weeks — rising demand without rising downloads signals a supply gap.

### Can I scan 200+ countries?

Yes — one call per region; loop through target markets for a global demand map.
