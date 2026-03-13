"""
scraper.py — Fetches live gold prices from gold-price-daily.com (Oman) in OMR
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone


SOURCE_URL = "https://gold-price-daily.com/gold-om/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_gold_prices() -> dict | None:
    """
    Fetches live gold prices from gold-price-daily.com for Oman in OMR.
    Falls back to approximate values if scraping fails.
    """
    try:
        resp = requests.get(SOURCE_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        prices = _parse_prices(soup)

        if not prices:
            raise ValueError("Failed to parse prices from page")

        return {
            "source": "gold-price-daily.com",
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
    """Parses the HTML table and extracts gold prices by karat."""
    try:
        result = {}
        karat_map = {
            "غرام ذهب عيار 24": "24k",
            "غرام ذهب عيار 22": "22k",
            "غرام ذهب عيار 21": "21k",
            "غرام ذهب عيار 18": "18k",
        }

        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True)
                    for arabic_name, key in karat_map.items():
                        if arabic_name in label and key not in result:
                            price_text = cells[1].get_text(strip=True)
                            price = _extract_number(price_text)
                            if price:
                                result[key] = price

        return result if len(result) >= 3 else None

    except Exception:
        return None


def _extract_number(text: str) -> float | None:
    """Extracts a float from a string like '62.75' or '62.75 ريال'."""
    import re
    numbers = re.findall(r"\d+\.?\d*", text.replace(",", ""))
    for n in numbers:
        val = float(n)
        if 10 < val < 500:  # Reasonable range for gold price per gram in OMR
            return val
    return None


def _fallback_prices() -> dict:
    """Approximate fallback prices — used only if scraping fails."""
    # Last updated: March 13, 2026 — source: gold-price-daily.com
    return {
        "24k": 62.75,
        "22k": 57.52,
        "21k": 54.91,
        "18k": 47.06,
    }