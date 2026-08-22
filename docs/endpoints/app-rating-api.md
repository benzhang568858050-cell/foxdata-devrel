# FoxData App Rating API — Ratings & Review Velocity for iOS & Google Play Apps

> FoxData API endpoint: `app/rate` · Region: per-country · Store: iOS App Store / Google Play

## What is the FoxData App Rating API?

The FoxData App Rating API returns daily rating data — average star rating, total ratings, star distribution, and daily new-review velocity. Track product health, review trends, and the impact of version updates on user sentiment.

## Code example

```python
import requests

r = requests.post(
    "https://api.foxdata.com/apiv1/open-api/app/rate",
    json={"appId": "959841453", "region": "TH",
          "startTime": "2026-08-14", "endTime": "2026-08-20", "store": "AS"},
    headers={"x-openapi-key": "<YOUR_LICENSE>"},
)
for day in r.json()["data"]["result"]["rating"]:
    print(day["date"][:10], day["num"], day["stars"])
```

## Real data (Shopee TH, 2026-08-20)

| Metric | Value |
|---|---|
| Average rating | 4.7★ |
| Total ratings | 1,345,323 |
| 5-star share | 83% |
| Daily new reviews | ~800-1,000 |

## FAQ

### What is review velocity and why does it matter?

Daily new-review count is a product-health pulse — 1-star spikes are early warnings; velocity changes reveal issues weeks before the average moves.

### How does rating affect ASO?

Rating stability matters more than level — store algorithms penalize volatile ratings.

### Can I track competitor ratings?

Yes — run the same endpoint for any competitor app ID.
