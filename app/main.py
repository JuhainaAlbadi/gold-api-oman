from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import secrets

from app.database import init_db
from app.scraper import fetch_gold_prices
from app.models import GoldPriceResponse, HistoryResponse, ConvertResponse
from app import database as db

# App Setup
app = FastAPI(
    title="Gold API - Oman Market 🇴🇲",
    description=(
        "A REST API that provides live gold prices for the Oman market in Omani Rial (OMR).\n\n"
        "**Features:**\n"
        "- Live prices for karats: 18k, 21k, 22k, 24k\n"
        "- Currency conversion (OMR, USD, EUR, SAR, AED, INR)\n"
        "- Historical price records\n"
        "- Price change comparison\n"
        "- API Key authentication\n\n"
        "**How to use:** Visit `/docs` to explore and test all endpoints interactively."
    ),
    version="1.0.0",
    contact={"name": "Majan Programmer Club Challenge"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Auth
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, store this in a .env file — never hardcode secrets
VALID_API_KEY = "goldapi-d69ksmmolq8qw-io"


async def verify_api_key(api_key: str = Security(api_key_header)):
    # Allow requests with no key in development/docs mode
    if api_key is None or api_key == "":
        return "docs-mode"
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key. Add X-API-Key to your request headers.")
    return api_key


# Startup
@app.on_event("startup")
async def startup():
    init_db()


# Endpoints
@app.get("/", tags=["Info"])
def root():
    """Entry point — general info about the API."""
    return {
        "api": "Gold API - Oman Market",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "current_prices": "/gold/prices",
            "price_history": "/gold/history",
            "currency_convert": "/gold/convert",
            "price_compare": "/gold/compare",
        },
        "usage": "Include X-API-Key: goldapi-d69ksmmolq8qw-io in your headers"
    }


@app.get(
    "/gold/prices",
    response_model=GoldPriceResponse,
    tags=["Gold Prices"],
    summary="Current gold prices in the Oman market",
    dependencies=[Depends(verify_api_key)],
)
async def get_gold_prices():
    """
    Returns the current gold prices in the Oman market in Omani Rial (OMR).

    Available karats: **18K, 21K, 22K, 24K**

    Data is fetched from a reliable source and saved locally to the database.
    """
    prices = fetch_gold_prices()
    if not prices:
        raise HTTPException(status_code=503, detail="Failed to fetch prices. Please try again later.")

    db.save_prices(prices)
    return prices


@app.get(
    "/gold/history",
    response_model=HistoryResponse,
    tags=["Gold Prices"],
    summary="Historical gold price records",
    dependencies=[Depends(verify_api_key)],
)
def get_history(limit: int = 10):
    """
    Returns the last **{limit}** gold price records saved in the local database.

    - **limit**: Number of records to return (default: 10, max: 100)
    """
    if limit > 100:
        limit = 100
    records = db.get_history(limit)
    return {"count": len(records), "history": records}


@app.get(
    "/gold/convert",
    response_model=ConvertResponse,
    tags=["Currency Conversion"],
    summary="Convert gold price between currencies",
    dependencies=[Depends(verify_api_key)],
)
async def convert_currency(
    karat: str = "24k",
    grams: float = 1.0,
    to: str = "USD"
):
    """
    Converts a gold price from Omani Rial (OMR) to another currency.

    - **karat**: Gold karat (18k, 21k, 22k, 24k)
    - **grams**: Weight in grams
    - **to**: Target currency (USD, EUR, SAR, AED, INR)
    """
    # Approximate exchange rates — in production, fetch from a live currency API
    exchange_rates = {
        "USD": 2.5974,
        "EUR": 2.3891,
        "SAR": 9.7408,
        "AED": 9.5409,
        "INR": 217.39,
        "OMR": 1.0,
    }

    to_upper = to.upper()
    if to_upper not in exchange_rates:
        raise HTTPException(
            status_code=400,
            detail=f"Currency '{to}' is not supported. Available currencies: {list(exchange_rates.keys())}"
        )

    prices = fetch_gold_prices()
    if not prices:
        raise HTTPException(status_code=503, detail="Failed to fetch prices. Please try again later.")

    karat_map = {
        "18k": prices["prices"]["18k"],
        "21k": prices["prices"]["21k"],
        "22k": prices["prices"]["22k"],
        "24k": prices["prices"]["24k"],
    }

    karat_lower = karat.lower()
    if karat_lower not in karat_map:
        raise HTTPException(status_code=400, detail=f"Invalid karat '{karat}'. Valid options: 18k, 21k, 22k, 24k")

    price_per_gram_omr = karat_map[karat_lower]
    total_omr = price_per_gram_omr * grams
    total_converted = round(total_omr * exchange_rates[to_upper], 4)

    return {
        "karat": karat_lower,
        "grams": grams,
        "price_per_gram_omr": price_per_gram_omr,
        "total_omr": round(total_omr, 4),
        "converted_to": to_upper,
        "total_converted": total_converted,
        "exchange_rate": exchange_rates[to_upper],
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get(
    "/gold/compare",
    tags=["Gold Prices"],
    summary="Compare current gold prices with previous record",
    dependencies=[Depends(verify_api_key)],
)
def compare_prices():
    """
    Compares the latest gold prices with the previous record in the database.
    Shows price change in amount and percentage for each karat.
    """
    records = db.get_history(2)

    if len(records) < 2:
        raise HTTPException(
            status_code=404,
            detail="Not enough data to compare. Call /gold/prices at least twice."
        )

    current = records[0]["prices"]
    previous = records[1]["prices"]

    comparison = {}
    for karat in ["18k", "21k", "22k", "24k"]:
        current_price = current.get(karat)
        previous_price = previous.get(karat)

        if current_price and previous_price:
            change_amount = round(current_price - previous_price, 4)
            change_percent = round((change_amount / previous_price) * 100, 2)
            trend = "↑ up" if change_amount > 0 else "↓ down" if change_amount < 0 else "→ stable"

            comparison[karat] = {
                "current": current_price,
                "previous": previous_price,
                "change_amount": change_amount,
                "change_percent": f"{change_percent}%",
                "trend": trend,
            }

    return {
        "current_timestamp": records[0]["timestamp"],
        "previous_timestamp": records[1]["timestamp"],
        "currency": "OMR",
        "comparison": comparison,
    }