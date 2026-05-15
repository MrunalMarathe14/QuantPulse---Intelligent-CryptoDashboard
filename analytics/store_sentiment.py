# analytics/store_sentiment.py

import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "crypto.db"
)

def store_sentiment(df):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            published TEXT,
            sentiment TEXT,
            confidence REAL,
            coin TEXT,
            fetched_at TEXT
        )
    """)

    df["fetched_at"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    df.to_sql(
        "news_sentiment",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    conn.close()

    print("Sentiment stored successfully.")