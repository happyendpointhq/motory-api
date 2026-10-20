# Motory API and Scraper

The Motory API returns car marketplace data from Motory (motory.com) in Saudi Arabia and
Jordan as JSON: used cars for sale with price, year, mileage, city and seller type, full
listing specs, the new car catalogue with prices by grade, dealers, car offers and finance
providers, plus a Saudi automotive business directory, car news and fuel prices. Motory has
no public developer API, so this REST API is the way to use its listings in your own code
without maintaining a Motory scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/motory-api?utm_source=github&utm_medium=readme&utm_campaign=motory-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/motory-com
- Product page: https://happyendpoint.com/library/motory-api?utm_source=github&utm_medium=readme&utm_campaign=motory-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://motory-com.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 46, all `GET` |
| Markets | Saudi Arabia (`country=sa`, prices in SAR) and Jordan (`country=jo`, prices in JOD) |
| Languages | English and Arabic (`lang=en` or `lang=ar`) |
| Page size | Up to 50 rows per page |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Used cars**
- Search used cars for sale with 21 filters: make, model, city, year, price, body type, fuel, transmission, mileage band, colour, origin, electric range, financing, priced listings only, seller type, dealer, price collection and keyword
- Seven sort orders: featured, newest, oldest, mileage and price in both directions
- Full listings: labelled specs, VIN and grade, gallery, numeric price with VAT note, financing company, inspection reports and related cars
- Paste a motory.com search or listing URL and get the same data back

**New cars**
- The new car catalogue with prices by model year and grade, specs and features
- A make's current line-up with starting and top prices
- Two new cars compared side by side, and the cars most often compared with one
- Selling companies and financing

**Market**
- Filter options with live result counts (cities, makes, models, price bands, mileage bands and more)
- Dealers and showrooms with stock counts, car offers and financing deals, finance providers by make
- Retail fuel prices per litre for Saudi Arabia and Jordan

**Directory and content**
- Saudi workshops, spare parts shops, car washes, tyre shops, inspection centres and showrooms, with opening hours and branches
- Car news by category, author, tag and make, and car videos

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/motory-com). Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Search filters take ids, not names. Look up the make first:

```bash
curl "https://motory-com.p.rapidapi.com/makes?condition=used&country=sa" \
  -H "x-rapidapi-host: motory-com.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://motory-com.p.rapidapi.com/used-cars?country=sa&make_id=90&with_price_only=true&sort=newest&page_size=10" \
  -H "x-rapidapi-host: motory-com.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py toyota
```

```python
from client import asking_price, get

toyota = next(m for m in get("/makes", condition="used")["items"] if m["name"] == "Toyota")
cars = get("/used-cars", make_id=toyota["id"], with_price_only="true", sort="newest")
for row in cars["items"]:
    print(asking_price(row), row["year"], row["mileage"], row["title"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs toyota
```

---

## Example response

One row from `GET /used-cars?country=sa&make_id=90&with_price_only=true&sort=newest`,
trimmed, from a live call on 20 October 2026. The full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 282101,
        "title": "Toyota Corolla XLI 2024",
        "year": 2024,
        "make_id": 90,
        "model_id": 431,
        "make": "Toyota",
        "model": "Corolla",
        "status": "active",
        "price_object": {
          "price_text": "Cash Price with VAT",
          "price_value": "57,500",
          "price_currency": "SR",
          "has_financing": true
        },
        "created_at": "20/10/2026",
        "transmission": "Automatic",
        "mileage": "146,275 km",
        "city": "Jeddah",
        "is_dealer": true,
        "dealer_type": "Dealer",
        "share_link": "https://ksa.motory.com/en/cars-for-sale/jeddah-haraj/toyota/corolla/2024/282101/"
      }
    ],
    "pagination": { "page": 1, "page_size": 10, "total_items": 132, "total_pages": 14 }
  }
}
```

---

## Endpoints

Base URL: `https://motory-com.p.rapidapi.com`

### Reference data

| Endpoint | Returns |
|---|---|
| `GET /makes` | Makes with ids and logos, for used or new cars |
| `GET /models` | One make's models with ids |
| `GET /used-car-filters` | Used-car filter options with live result counts |
| `GET /new-car-filters` | New-car filter options with live result counts |
| `GET /search-suggestions` | Make, model and year suggestions with ids for typed text |
| `GET /resolve-url` | The page type and ids behind any motory.com link |
| `GET /fuel-prices` | Retail fuel prices per litre by grade |

### Used cars

| Endpoint | Returns |
|---|---|
| `GET /used-cars` | Used cars for sale, with all filters and sorts |
| `GET /used-car-details` | One listing in full: specs, VIN, price, inspection reports, related cars |
| `GET /used-cars-by-url` | The results of a pasted motory.com search URL |
| `GET /used-car-details-by-url` | One listing from its motory.com URL |

### New cars

| Endpoint | Returns |
|---|---|
| `GET /new-cars` | New cars by make, model, year, price, body, fuel and more |
| `GET /new-car-details` | One new car: grade, price, specs, features, selling companies |
| `GET /new-cars-by-url` | The results of a pasted motory.com new-car URL |
| `GET /new-car-details-by-url` | One new car from its motory.com URL |
| `GET /new-car-lineup` | A make's line-up with starting and top prices |
| `GET /compare-new-cars` | Two new cars side by side |
| `GET /compare-suggestions` | Cars most often compared with a car |

### Dealers, offers and finance

| Endpoint | Returns |
|---|---|
| `GET /dealers` | Showcased dealers with stock counts |
| `GET /dealer-details` | One dealer: showroom location, branches, stock |
| `GET /offers` | Current car offers and financing deals |
| `GET /offer-details` | One offer with its terms and the cars on offer |
| `GET /finance-providers` | Finance providers, optionally by make |

### Site search

| Endpoint | Returns |
|---|---|
| `GET /search` | Keyword search across used cars, new cars, offers, directory, news and videos |

### Business directory (Saudi Arabia)

| Endpoint | Returns |
|---|---|
| `GET /directory-search` | Workshops, parts shops, car washes and more by name, city, make, service, opening day |
| `GET /directory-business-details` | One business with contacts and opening hours |
| `GET /directory-companies` | Companies with branches |
| `GET /directory-company-details` | One company |
| `GET /directory-branches` | A company's branches |
| `GET /directory-services`, `/directory-amenities`, `/directory-cities`, `/directory-makes` | Directory filter values |

### News and videos

| Endpoint | Returns |
|---|---|
| `GET /news-categories`, `/category-news`, `/news-search`, `/news-details`, `/most-read-news` | Car news |
| `GET /author-details`, `/author-news`, `/author-tags`, `/tag-news` | News by author and tag |
| `GET /video-categories`, `/videos`, `/video-details` | Car videos with playable links |
| `GET /status` | Service health |

---

## Things to know about the data

From the documentation and a live test on 20 October 2026. These produce wrong numbers
rather than errors.

- **Dealer prices include VAT, private prices do not say so.** On live rows, dealer listings
  carry `price_text: "Cash Price with VAT"` and private listings `"Cash Price"`. Keep
  `price_text` next to the price and compare like with like.
- **`price_value` is a string, and can be "Contact Seller".** Live priced rows read
  `"57,500"`. Without `with_price_only=true` many rows read `"Contact Seller"` with an empty
  currency (every row in the documented example does). `client.asking_price()` returns a
  number or `None`. On `/used-car-details`, `price.price` is already a number, and `0`
  means no price was published.
- **The currency code is `SR`, not `SAR`.** Live rows in Saudi Arabia carry
  `price_currency: "SR"`. Jordan prices are in JOD.
- **Mileage is a band or an exact figure, depending on the seller.** In one live page of 50
  Toyota listings, all 24 exact readings (`"146,275 km"`) came from dealers, while all 23
  private sellers gave a band (`"80,000-89,999 km"`) and some used the open
  `"200,000+ km"`. `client.mileage_range()` turns either into a low and high figure. Do not
  average the band labels.
- **Watch for placeholder prices.** The same live page had a 2023 Toyota Raize at SAR 45,
  next to another 2023 Raize at SAR 46,500. Use `min_price` or drop implausible values
  before you take a median.
- **"Used" includes new cars.** Dealers list 0 km cars of the current model year in the
  used-car search (live: a 2026 Urban Cruiser at 0 km). Filter on mileage or year if you
  want genuinely used stock.
- **Price sorting only works on small searches.** `sort=price_asc` and `price_desc` order a
  search that matches at most 50 listings; a larger search returns 400 and tells you how to
  narrow it. Sort `newest` and sort prices yourself, as `used_cars_to_csv.py` does.
- **`newest` is by publish date, not `created_at`.** The live newest-first page ended with
  a listing whose `created_at` was `06/12/2025` among October 2026 rows. `created_at` is
  `DD/MM/YYYY`.
- **Ids belong to one market.** Make, model, city, dealer and vehicle ids from
  `country=sa` are unknown in `country=jo` (404 on lookups, 400 on filters). Look ids up
  again per market.
- **Filters are strict about values.** `with_price_only=false` is a 400 (omit it instead),
  `page_size` above 50 is a 400, and `keyword` matches only in the language set by `lang`.
- **Spec text carries its label.** On the live detail record, `description.grade` read
  `"- Grade: XLI"` and `vin_number` had the same `"- VIN Number: "` prefix. Strip the label
  before storing the value.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Make lookup, the newest priced used cars for that make, one listing's full spec sheet |
| [`examples/python/used_cars_to_csv.py`](examples/python/used_cars_to_csv.py) | Pages through a used-car search at 50 rows a page and writes a CSV with numeric price and mileage columns |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The quickstart in Node 18+, no dependencies |
| [`samples/`](samples/) | Example responses for five endpoints |

---

## API or your own Motory scraper

A homemade Motory scraper has to follow the site's markup in two languages and two
markets, and breaks when either changes. This API returns the same listings as documented
JSON with a stable contract, so the work you keep is the analysis, not the parser. If you
need a recurring export of Saudi car prices rather than API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=motory-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Motory
listings without code:

```json
{
  "mcpServers": {
    "motory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: motory-com.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Does Motory have an API?

Motory does not publish a public developer API for its listings. This API, built and
maintained by Happy Endpoint and independent of Motory, provides that access as REST and
JSON.

### Is there a free Motory API?

Yes. The [RapidAPI listing](https://rapidapi.com/happyendpoint/api/motory-com) has a free plan, and every endpoint can be tried on it.

### Where is the Motory API documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the
endpoint table above summarises them. Example responses are in [`samples/`](samples/).

### How do I scrape Motory car listings in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call `/used-cars` with ids from `/makes` and
`/used-car-filters`. [`used_cars_to_csv.py`](examples/python/used_cars_to_csv.py) exports a
whole search to CSV with numeric prices and mileage.

### Can I get used car prices in Saudi Arabia by make and model?

Yes. Filter `/used-cars` by `make_id` and `model_id` with `with_price_only=true`, and keep
`price_text` so dealer prices with VAT are not mixed with private prices.

### Does it cover Jordan?

Yes. Send `country=jo` for Jordan's own inventory, priced in JOD. Ids differ between the two
markets, so look them up again with `country=jo`.

### Can I get new car prices and dealer offers?

Yes. `/new-cars` and `/new-car-details` return prices by model year and grade, `/offers`
lists current deals with their terms, and `/compare-new-cars` puts two cars side by side.

### Do you cover other Saudi marketplaces?

Yes, including Aqar and Wasalt for property. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=motory-api).

---

## Related repos

- [aqar-api](https://github.com/happyendpointhq/aqar-api) - Saudi Arabia property listings, district prices and AI search
- [wasalt-api](https://github.com/happyendpointhq/wasalt-api) - Saudi listings with REGA licences, holiday rentals and Infath auctions
- [awesome-ecommerce-data-apis](https://github.com/happyendpointhq/awesome-ecommerce-data-apis) - product, pricing and marketplace data APIs
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
