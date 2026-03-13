# 🥇 Gold API — Oman Market

> A REST API that delivers real-time gold prices for the Oman market in Omani Rial (OMR). Built for the **Majan Programmer Club Challenge — 2026**.

---

## Tech Stack

- Python 3.11 + FastAPI
- SQLite
- gold-price-daily.com — Live gold price data source (updated every 15 minutes)
- API Key Authentication

---

## Features

✅ Live gold prices for karats 18k, 21k, 22k, 24k in OMR  
✅ Real-time data from gold-price-daily.com (updated every 15 min) with automatic fallback  
✅ Currency conversion (OMR → USD, EUR, SAR, AED, INR)  
✅ Historical price records stored in local SQLite database  
✅ Price change comparison between records  
✅ API Key authentication on all protected endpoints  
✅ Auto-generated Swagger UI documentation  
✅ Clean JSON responses with timestamps  

---

## Project Structure
```
gold-api-oman/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app, middleware, and all endpoints
│   ├── scraper.py      # Live data fetching from gold-price-daily.com
│   ├── database.py     # SQLite connection, schema, and queries
│   └── models.py       # Pydantic models for validation and serialization
├── gold_prices.db      # Auto-generated SQLite database (created on first run)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🗄️ Database

Uses a local **SQLite** database to store price history automatically every time `/gold/prices` is called.

Each record stores:
- Timestamp of the request
- Data source (gold-price-daily.com or fallback)
- Price per gram for all 4 karats (18k, 21k, 22k, 24k)
- Full raw JSON response

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/JuhainaAlBadi/gold-api-oman.git
cd gold-api-oman
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python -m uvicorn app.main:app --reload
```

### 4. Open interactive docs
```
http://localhost:8000/docs
```

---

## 🔑 Authentication

All endpoints (except `GET /`) support an optional API Key in the request header:
```
X-API-Key: YOUR_API_KEY
```

---

## API Documentation

After running the server, visit: `http://localhost:8000/docs`

---

## Example API Usage

**Get current gold prices:**
```bash
curl http://localhost:8000/gold/prices
```

**Get price history (last 5 records):**
```bash
curl "http://localhost:8000/gold/history?limit=5"
```

**Convert 10 grams of 21k gold to USD:**
```bash
curl "http://localhost:8000/gold/convert?karat=21k&grams=10&to=USD"
```

**Convert 5 grams of 22k gold to SAR:**
```bash
curl "http://localhost:8000/gold/convert?karat=22k&grams=5&to=SAR"
```

**Compare current prices with previous record:**
```bash
curl http://localhost:8000/gold/compare
```

---

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | ❌ | API info and available endpoints |
| GET | `/gold/prices` | ✅ | Live gold prices for all karats in OMR |
| GET | `/gold/history` | ✅ | Historical price records from local database |
| GET | `/gold/convert` | ✅ | Convert gold price to another currency |
| GET | `/gold/compare` | ✅ | Compare current prices with previous record |

---
