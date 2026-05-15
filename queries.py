# queries.py
import sqlite3
import pandas as pd

DB_PATH = "data/crypto.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_latest_snapshot():
    """Get the most recent fetch's data."""
    query = """
        SELECT *
        FROM crypto_prices
        WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
        ORDER BY market_cap_rank ASC
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_top_gainers(limit=10):
    """Top coins by 24h price change (most recent snapshot)."""
    query = f"""
        SELECT name, symbol, price_usd, price_change_percentage_24h, market_cap
        FROM crypto_prices
        WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
          AND price_change_percentage_24h IS NOT NULL
        ORDER BY price_change_percentage_24h DESC
        LIMIT {limit}
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_top_losers(limit=10):
    """Top coins by 24h price change (worst performers)."""
    query = f"""
        SELECT name, symbol, price_usd, price_change_percentage_24h, market_cap
        FROM crypto_prices
        WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
          AND price_change_percentage_24h IS NOT NULL
        ORDER BY price_change_percentage_24h ASC
        LIMIT {limit}
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_volume_vs_marketcap():
    """Volume to market cap ratio — finds over/under-traded coins."""
    query = """
        SELECT 
            name,
            symbol,
            total_volume,
            market_cap,
            ROUND(CAST(total_volume AS FLOAT) / NULLIF(market_cap, 0) * 100, 2) AS volume_to_mcap_ratio
        FROM crypto_prices
        WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
          AND market_cap > 0
        ORDER BY volume_to_mcap_ratio DESC
        LIMIT 20
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_btc_dominance():
    """BTC market cap as % of total market cap."""
    query = """
        WITH latest AS (
            SELECT * FROM crypto_prices
            WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
        ),
        totals AS (
            SELECT 
                SUM(market_cap) AS total_mcap,
                SUM(CASE WHEN symbol = 'btc' THEN market_cap ELSE 0 END) AS btc_mcap,
                SUM(CASE WHEN symbol = 'eth' THEN market_cap ELSE 0 END) AS eth_mcap
            FROM latest
        )
        SELECT
            ROUND(btc_mcap / total_mcap * 100, 2) AS btc_dominance_pct,
            ROUND(eth_mcap / total_mcap * 100, 2) AS eth_dominance_pct,
            ROUND((total_mcap - btc_mcap - eth_mcap) / total_mcap * 100, 2) AS altcoin_dominance_pct,
            total_mcap,
            btc_mcap
        FROM totals
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_volatility_rank():
    """Rank coins by 24h absolute price change (most volatile)."""
    query = """
        SELECT
            name,
            symbol,
            price_usd,
            ABS(price_change_percentage_24h) AS volatility_24h,
            price_change_percentage_24h AS direction_24h
        FROM crypto_prices
        WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
        ORDER BY volatility_24h DESC
        LIMIT 15
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_price_history(coin_symbol, limit=50):
    """Get historical price data for a specific coin across fetches."""
    query = f"""
        SELECT fetched_at, price_usd, price_change_percentage_24h, total_volume
        FROM crypto_prices
        WHERE LOWER(symbol) = LOWER('{coin_symbol}')
        ORDER BY fetched_at DESC
        LIMIT {limit}
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df