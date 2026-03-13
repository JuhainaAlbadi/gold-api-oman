# 🥇 Gold API — Oman Market

>  REST API that delivers real-time gold prices for the Oman market in Omani Rial (OMR). Built for the **Majan Programmer Club Challenge — 2026**.

---

## Tech Stack

- Python 3.11 + FastAPI
- SQLite
- goldapi.io — Live gold price data source
- API Key Authentication

---

## Features

✅ Live gold prices for karats 18k, 21k, 22k, 24k in OMR  
✅ Real-time data from goldapi.io with automatic fallback  
✅ Currency conversion (OMR → USD, EUR, SAR, AED, INR)  
✅ Historical price records stored in local SQLite database  
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
│   ├── scraper.py      # Live data fetching from goldapi.io
│   ├── database.py     # SQLite connection, schema, and queries
│   └── models.py       # Pydantic models for validation and serialization
├── gold_prices.db      # Auto-generated SQLite database (created on first run)
├── requirements.txt
├── .gitignore
└── README.md
```

## 🗄️ Database

Uses a local **SQLite** database to store price history automatically every time `/gold/prices` is called.

Each record stores:
- Timestamp of the request
- Data source (goldapi.io or fallback)
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

All endpoints (except `GET /`) require an API Key in the request header:
```
X-API-Key: goldapi-d69ksmmolq8qw-io
```

## API Documentation

After running the server, visit: `http://localhost:8000/docs`

---

## Example API Usage

**Get current gold prices:**
```bash
curl -H "X-API-Key: goldapi-d69ksmmolq8qw-io" \
     http://localhost:8000/gold/prices
```

**Get price history (last 5 records):**
```bash
curl -H "X-API-Key: goldapi-d69ksmmolq8qw-io" \
     "http://localhost:8000/gold/history?limit=5"
```

**Convert 10 grams of 21k gold to USD:**
```bash
curl -H "X-API-Key: goldapi-d69ksmmolq8qw-io" \
     "http://localhost:8000/gold/convert?karat=21k&grams=10&to=USD"
```

**Convert 5 grams of 22k gold to SAR:**
```bash
curl -H "X-API-Key: goldapi-d69ksmmolq8qw-io" \
     "http://localhost:8000/gold/convert?karat=22k&grams=5&to=SAR"
```

---

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | ❌ | API info and available endpoints |
| GET | `/gold/prices` | ✅ | Live gold prices for all karats in OMR |
| GET | `/gold/history` | ✅ | Historical price records from local database |
| GET | `/gold/convert` | ✅ | Convert gold price to another currency |

---



