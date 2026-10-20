"""Export a Motory used-car search to CSV, with numeric price and mileage columns.

    python used_cars_to_csv.py --make-id 90 --model-id 406 --out fortuner.csv
    python used_cars_to_csv.py --make-id 90 --country jo --out toyota-jordan.csv

Pages at 50 rows (the maximum) until pagination.total_pages. Ids are per market: take
make_id and model_id from /makes and /models called with the same --country.
"""

import argparse
import csv

from client import asking_price, get, mileage_range

COLUMNS = [
    "id", "title", "make", "model", "year", "city", "price", "currency", "mileage_text",
    "mileage_low_km", "mileage_high_km", "transmission", "seller_type", "has_financing",
    "created_at", "share_link",
]


def to_row(item):
    low, high = mileage_range(item)
    return {
        "id": item["id"],
        "title": item.get("title"),
        "make": item.get("make"),
        "model": item.get("model"),
        "year": item.get("year"),
        "city": item.get("city"),
        "price": asking_price(item),
        "currency": (item.get("price_object") or {}).get("price_currency"),
        "mileage_text": item.get("mileage"),
        "mileage_low_km": low,
        "mileage_high_km": high,
        "transmission": item.get("transmission"),
        "seller_type": "dealer" if item.get("is_dealer") else "individual",
        "has_financing": item.get("has_financing"),
        "created_at": item.get("created_at"),
        "share_link": item.get("share_link"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", default="sa", choices=["sa", "jo"])
    parser.add_argument("--make-id", type=int)
    parser.add_argument("--model-id", type=int)
    parser.add_argument("--city-id", help="from /used-car-filters; comma-separated for several")
    parser.add_argument("--min-year", type=int)
    parser.add_argument("--seller-type", choices=["dealer", "individual"])
    parser.add_argument("--all", action="store_true", help='include "Contact Seller" listings')
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--out", default="used-cars.csv")
    args = parser.parse_args()

    written = 0
    with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for page in range(1, args.max_pages + 1):
            data = get(
                "/used-cars",
                country=args.country,
                make_id=args.make_id,
                model_id=args.model_id,
                city_id=args.city_id,
                min_year=args.min_year,
                seller_type=args.seller_type,
                with_price_only=None if args.all else "true",
                sort="newest",
                page=page,
                page_size=50,
            )
            for item in data["items"]:
                writer.writerow(to_row(item))
                written += 1
            pages = data["pagination"]["total_pages"]
            print(f"page {page} of {pages}: {written} of {data['pagination']['total_items']} listings")
            if page >= pages:
                break
    print(f"Wrote {written} rows to {args.out}")


if __name__ == "__main__":
    main()
