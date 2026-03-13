"""
models.py — Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field



class KaratPrices(BaseModel):
    price_18k: float = Field(..., alias="18k", description="18k gold price in OMR per gram")
    price_21k: float = Field(..., alias="21k", description="21k gold price in OMR per gram")
    price_22k: float = Field(..., alias="22k", description="22k gold price in OMR per gram")
    price_24k: float = Field(..., alias="24k", description="24k gold price in OMR per gram")

    class Config:
        populate_by_name = True


class GoldPriceResponse(BaseModel):
    source: str = Field(..., description="Data source")
    currency: str = Field(default="OMR", description="Currency")
    unit: str = Field(default="gram", description="Unit of measurement")
    market: str = Field(default="Oman Gold Market")
    timestamp: str = Field(..., description="Time data was fetched (UTC)")
    prices: dict = Field(..., description="Gold prices by karat")


class HistoryRecord(BaseModel):
    timestamp: str
    source: str
    prices: dict


class HistoryResponse(BaseModel):
    count: int
    history: list[HistoryRecord]


class ConvertResponse(BaseModel):
    karat: str = Field(..., description="Selected karat")
    grams: float = Field(..., description="Weight in grams")
    price_per_gram_omr: float = Field(..., description="Price per gram in OMR")
    total_omr: float = Field(..., description="Total in Omani Rial")
    converted_to: str = Field(..., description="Target currency")
    total_converted: float = Field(..., description="Total in target currency")
    exchange_rate: float = Field(..., description="Exchange rate used")
    timestamp: str