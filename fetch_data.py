# fetch_data.py
import requests
import sqlite3
import pandas as pd
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
DB_PATH = "data/crypto.db"

def fetch_crypto_data(limit=100):
    """Fetch top N coins by market cap from CoinGecko API."""
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d"
    }
    
    logging.info(f"Fetching data for top {limit} coins from CoinGecko API...")
    
    try:
        response = requests.get(COINGECKO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Successfully fetched {len(data)} coins.")
        return data
    except requests.exceptions.Timeout:
        logging.error("API request timed out.")
        return []
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return []


def parse_to_dataframe(raw_data):
    """Convert raw API response to a clean pandas DataFrame."""
    if not raw_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(raw_data)
    
    # Select only the columns we need
    cols = [
        'id', 'symbol', 'name', 'current_price', 'market_cap',
        'market_cap_rank', 'total_volume', 'price_change_percentage_24h',
        'price_change_percentage_7d_in_currency', 'circulating_supply',
        'total_supply', 'ath', 'ath_change_percentage', 'last_updated'
    ]
    
    # Some cols may not exist — use only available ones
    cols = [c for c in cols if c in df.columns]
    df = df[cols].copy()
    
    # Rename for clarity
    df.rename(columns={
        'price_change_percentage_7d_in_currency': 'price_change_percentage_7d',
        'current_price': 'price_usd'
    }, inplace=True)
    
    # Add fetch timestamp
    df['fetched_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # Clean nulls
    df.fillna(0, inplace=True)
    
    logging.info(f"Parsed DataFrame: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def store_to_sqlite(df, db_path=DB_PATH):
    """Store DataFrame to SQLite, creating table if not exists."""
    if df.empty:
        logging.warning("Empty DataFrame — nothing to store.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id TEXT,
            symbol TEXT,
            name TEXT,
            price_usd REAL,
            market_cap REAL,
            market_cap_rank INTEGER,
            total_volume REAL,
            price_change_percentage_24h REAL,
            price_change_percentage_7d REAL,
            circulating_supply REAL,
            total_supply REAL,
            ath REAL,
            ath_change_percentage REAL,
            last_updated TEXT,
            fetched_at TEXT
        )
    """)
    
    # Insert new records (append — we keep history)
    df.to_sql('crypto_prices', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    
    logging.info(f"Stored {len(df)} records to {db_path}")


def run_pipeline():
    """Main pipeline: fetch → parse → store."""
    logging.info("=== Pipeline started ===")
    raw = fetch_crypto_data(limit=100)
    df = parse_to_dataframe(raw)
    store_to_sqlite(df)
    logging.info("=== Pipeline complete ===")
    return df


if __name__ == "__main__":
    run_pipeline()