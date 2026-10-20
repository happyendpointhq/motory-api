# Sample responses

Example `200` responses for five Motory API endpoints. Long arrays are cut to their first
few items. Seller names, phone and WhatsApp numbers, and private sellers' ids are removed.
Field names and values are otherwise unchanged.

| File | Request | Source |
|---|---|---|
| `makes.json` | `GET /makes?condition=used&country=sa` | public documentation |
| `models.json` | `GET /models?make_id=90&condition=used&country=sa` | public documentation |
| `used-cars.json` | `GET /used-cars?country=sa&make_id=90&with_price_only=true&sort=newest&page_size=10` | live response, 20 Oct 2026, three rows kept |
| `used-car-details.json` | `GET /used-car-details?vehicle_id=272443&country=sa` | public documentation |
| `used-car-filters.json` | `GET /used-car-filters?country=sa` | public documentation |

`used-cars.json` is a live response because every row in the documented example reads
"Contact Seller", so it shows none of the price, VAT and mileage formats you will meet. The
three rows kept are a dealer with an exact mileage, a private seller with a mileage band,
and a private seller in the open `200,000+ km` band.

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
