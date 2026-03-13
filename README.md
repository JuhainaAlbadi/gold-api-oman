# 🥇 Gold API - Oman Market

**A REST API that provides live gold prices for the Oman market in Omani Rial (OMR)**

Built for the **Majan Programmer Club Challenge** — March 2026

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn app.main:app --reload
```

Server will run at: `http://localhost:8000`

### 3. Interactive docs (Swagger)

Open in your browser: `http://localhost:8000/docs`

---

## 🔑 Authentication

All endpoints require an **API Key** in the request header:
```
X-API-Key: gold-oman-2026-demo
```

---

## 📡 Endpoints

### `GET /` — General Info
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "api": "Gold API - Oman Market",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### `GET /gold/prices` — Current Gold Prices

Returns live gold prices for karats 18k, 21k, 22k, 24k in the Oman market.
```bash
curl -H "X-API-Key: gold-oman-2026-demo" \
     http://localhost:8000/gold/prices
```

**Response:**
```json
{
  "source": "omangoldprice.com",
  "currency": "OMR",
  "unit": "gram",
  "market": "Oman Gold Market",
  "timestamp": "2026-03-13T10:30:00Z",
  "prices": {
    "18k": 49.30,
    "21k": 57.51,
    "22k": 60.25,
    "24k": 64.55
  }
}
```

---

### `GET /gold/history` — Price History

Returns the last N records saved in the local database.
```bash
curl -H "X-API-Key: gold-oman-2026-demo" \
     "http://localhost:8000/gold/history?limit=5"
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit`   | int  | 10      | Number of records (max: 100) |

**Response:**
```json
{
  "count": 5,
  "history": [
    {
      "timestamp": "2026-03-13T10:30:00Z",
      "source": "omangoldprice.com",
      "prices": {
        "18k": 49.30,
        "21k": 57.51,
        "22k": 60.25,
        "24k": 64.55
      }
    }
  ]
}
```

---

### `GET /gold/convert` — Currency Conversion

Converts a gold price from Omani Rial (OMR) to another currency.
```bash
curl -H "X-API-Key: gold-oman-2026-demo" \
     "http://localhost:8000/gold/convert?karat=22k&grams=5&to=USD"
```

**Parameters:**
| Parameter | Type   | Default | Description |
|-----------|--------|---------|-------------|
| `karat`   | string | `24k`   | Karat: 18k, 21k, 22k, 24k |
| `grams`   | float  | `1.0`   | Weight in grams |
| `to`      | string | `USD`   | Currency: USD, EUR, SAR, AED, INR |

**Response:**
```json
{
  "karat": "22k",
  "grams": 5.0,
  "price_per_gram_omr": 60.25,
  "total_omr": 301.25,
  "converted_to": "USD",
  "total_converted": 782.45,
  "exchange_rate": 2.5974,
  "timestamp": "2026-03-13T10:30:00Z"
}
```

---

## 🏗️ Project Structure
```
gold-api-oman/
├── app/
│   ├── main.py        # FastAPI app + all endpoints
│   ├── scraper.py     # Fetches live data from omangoldprice.com
│   ├── database.py    # SQLite — local price storage
│   └── models.py      # Pydantic models for request/response
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Main framework |
| **Uvicorn** | ASGI server |
| **BeautifulSoup4** | Web scraping |
| **SQLite** | Local database |
| **Pydantic** | Data validation |
| **Requests** | HTTP client |

---



