"""Find a make, list its used cars that show a price, then open one listing.

    python quickstart.py toyota
"""

import sys

from client import asking_price, get

wanted = (sys.argv[1] if len(sys.argv) > 1 else "toyota").lower()

# 1. Make ids. condition=used lists the makes that have used cars for sale right now.
makes = get("/makes", condition="used", country="sa")["items"]
make = next((m for m in makes if m["name"].lower() == wanted), None)
if not make:
    raise SystemExit(f"No used-car make called {wanted!r}. Try one of: {[m['name'] for m in makes[:10]]}")
print(f"{make['name']}: make_id {make['id']}")

# 2. Newest used listings for that make. with_price_only drops "Contact Seller" rows.
results = get(
    "/used-cars",
    country="sa",
    make_id=make["id"],
    with_price_only="true",
    sort="newest",
    page_size=10,
)
page = results["pagination"]
print(f"{page['total_items']} listings with a price, page 1 of {page['total_pages']}\n")
for row in results["items"]:
    price = asking_price(row)
    price_text = f"SAR {price:,}" if price else "Contact Seller"
    seller = "dealer" if row.get("is_dealer") else "private"
    print(f"{price_text:>14}  {row['year']}  {row['mileage']:<18} {row['city']:<10} {seller:<8} {row['title']}  (id {row['id']})")

# 3. One listing in full: the numeric price and the labelled spec sheet.
if results["items"]:
    car = get("/used-car-details", vehicle_id=results["items"][0]["id"], country="sa")
    print(f"\n{car['header']['title']}, status {car['header']['status']}")
    print(f"Price: {car['price']['price']:,} {car['price'].get('currency', '')} ({car['price'].get('vat_text', '')})")
    for spec in car.get("overview") or []:
        print(f"  {spec['title']}: {spec['text']}")
