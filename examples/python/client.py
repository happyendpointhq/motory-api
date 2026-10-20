"""Minimal client for the Motory API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
import re

import requests

HOST = "motory-com.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def asking_price(row):
    """Price of a search row as a number, or None when it reads "Contact Seller"."""
    value = (row.get("price_object") or {}).get("price_value") or ""
    digits = re.sub(r"[^\d]", "", str(value))
    return int(digits) if digits else None


def mileage_range(row):
    """(low_km, high_km) from the mileage text: a band ("10,000-19,999 km"),
    an open band ("200,000+ km", high is None) or an exact figure ("92,319 km")."""
    text = (row.get("mileage") or "").replace(",", "").replace("km", "").strip()
    if not text:
        return None, None
    if text.endswith("+"):
        return int(text[:-1]), None
    low, _, high = text.partition("-")
    return int(low), int(high or low)
