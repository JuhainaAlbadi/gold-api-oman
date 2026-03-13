"""
database.py — SQLite local storage for gold price history
"""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("gold_prices.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Creates the database tables on first run."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gold_prices (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT    NOT NULL,
                source    TEXT,
                price_18k REAL,
                price_21k REAL,
                price_22k REAL,
                price_24k REAL,
                raw_json  TEXT
            )
        """)
        conn.commit()
    print("[DB] Database initialized ✅")


def save_prices(data: dict):
    """Saves a new price record to the database."""
    prices = data.get("prices", {})
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO gold_prices
                (timestamp, source, price_18k, price_21k, price_22k, price_24k, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                data.get("source", "unknown"),
                prices.get("18k"),
                prices.get("21k"),
                prices.get("22k"),
                prices.get("24k"),
                json.dumps(data),
            ),
        )
        conn.commit()


def get_history(limit: int = 10) -> list[dict]:
    """Returns the last {limit} price records from the database."""
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT timestamp, source, price_18k, price_21k, price_22k, price_24k
            FROM gold_prices
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "timestamp": r[0],
            "source": r[1],
            "prices": {
                "18k": r[2],
                "21k": r[3],
                "22k": r[4],
                "24k": r[5],
            },
        }
        for r in rows
    ]