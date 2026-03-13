"""
scraper.py — Fetches live gold prices from goldapi.io and converts to OMR
"""

import requests
from datetime import datetime, timezone


GOLD_API_KEY = "goldapi-d69ksmmolq8qw-io"
GOLD_API_URL = "https://www.goldapi.io/api"

# 1 USD = 0.3845 OMR (fixed rate — Omani Rial is pegged to USD)
USD_TO_OMR = 0.3845

HEADERS = {
    "x-access-token": GOLD_API_KEY,
    "Content-Type": "application/json"
}


def fetch_gold_prices() -> dict | None:
    """
    Fetches the current gold price from goldapi.io and converts to OMR per gram.
    Returns a dict with prices for all karats, or falls back to approximate values.
    """
    try:
        # Fetch XAU (gold) price in USD
        resp = requests.get(f"{GOLD_API_URL}/XAU/USD", headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Price per troy ounce in USD
        price_usd_per_oz = data["price"]

        # Convert to price per gram in USD (1 troy oz = 31.1035 grams)
        price_usd_per_gram = price_usd_per_oz / 31.1035

        # Convert to OMR
        price_omr_per_gram_24k = price_usd_per_gram * USD_TO_OMR

        # Calculate other karats based on 24k price
        prices = {
            "24k": round(price_omr_per_gram_24k, 3),
            "22k": round(price_omr_per_gram_24k * (22 / 24), 3),
            "21k": round(price_omr_per_gram_24k * (21 / 24), 3),
            "18k": round(price_omr_per_gram_24k * (18 / 24), 3),
        }

        return {
            "source": "goldapi.io",
            "currency": "OMR",
            "unit": "gram",
            "market": "Oman Gold Market",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prices": prices,
        }

    except Exception as e:
        print(f"[Scraper Error] {e} — using fallback prices")
        return {
            "source": "fallback",
            "currency": "OMR",
            "unit": "gram",
            "market": "Oman Gold Market",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prices": _fallback_prices(),
        }


def _fallback_prices() -> dict:
    """Approximate fallback prices — used only if goldapi.io is unreachable."""
    # Last updated: March 13, 2026
    return {
        "24k": 64.70,
        "22k": 60.40,
        "21k": 57.65,
        "18k": 49.40,
    }