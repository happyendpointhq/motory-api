// Motory API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs toyota

const HOST = 'motory-com.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Motory API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const wanted = (process.argv[2] ?? 'toyota').toLowerCase();
const { items: makes } = await get('/makes', { condition: 'used', country: 'sa' });
const make = makes.find((m) => m.name.toLowerCase() === wanted);
if (!make) throw new Error(`No used-car make called ${wanted}`);

const { items, pagination } = await get('/used-cars', {
  country: 'sa',
  make_id: make.id,
  with_price_only: 'true',
  sort: 'newest',
  page_size: 10,
});
console.log(`${make.name}: ${pagination.total_items} used listings with a price`);
for (const row of items) {
  const { price_value: price, price_currency: currency } = row.price_object;
  console.log(`${`${currency} ${price}`.padStart(14)}  ${row.year}  ${row.mileage.padEnd(18)} ${row.title}`);
}
