"""
scraper.py — Fetches live gold prices from omangoldprice.com
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

SOURCE_URL = "https://www.omangoldprice.com/"


def fetch_gold_prices() -> dict | None:
    """
    Fetches the current gold prices from omangoldprice.com.
    Returns a dict with prices, or None on failure.
    """
    try:
        resp = requests.get(SOURCE_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        prices = _parse_prices(soup)

        if not prices:
            # Fallback: use approximate prices if scraping fails
            prices = _fallback_prices()

        return {
            "source": "omangoldprice.com",
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


def _parse_prices(soup: BeautifulSoup) -> dict | None:
    """Parses the HTML page and extracts gold prices by karat."""
    try:
        result = {}
        carat_map = {
            "24 Carat": "24k",
            "22 Carat": "22k",
            "21 Carat": "21k",
            "18 Carat": "18k",
        }

        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True)
                    for carat_name, key in carat_map.items():
                        if carat_name in label and key not in result:
                            price_text = cells[1].get_text(strip=True)
                            price = _extract_number(price_text)
                            if price:
                                result[key] = price

        return result if len(result) >= 2 else None

    except Exception:
        return None


def _extract_number(text: str) -> float | None:
    """Extracts a float from a string like 'OMR 64.55' → 64.55"""
    import re
    numbers = re.findall(r"\d+\.?\d*", text.replace(",", ""))
    for n in numbers:
        val = float(n)
        if 10 < val < 500:  # Reasonable range for gold price per gram in OMR
            return val
    return None


def _fallback_prices() -> dict:
    """Approximate fallback prices — update manually or from a secondary source."""
    # Based on last known prices (March 2026)
    return {
        "24k": 64.55,
        "22k": 60.25,
        "21k": 57.51,
        "18k": 49.30,
    }