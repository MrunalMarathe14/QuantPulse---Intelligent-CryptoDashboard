# analytics/sentiment_queries.py

import sqlite3
import pandas as pd

DB_PATH = "data/crypto.db"

def get_sentiment_distribution():

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT sentiment,
               COUNT(*) as count
        FROM news_sentiment
        GROUP BY sentiment
    """

    try:

        df = pd.read_sql_query(query, conn)

    except:

        df = pd.DataFrame()

    conn.close()

    return df

def get_coin_sentiment():

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT coin,
               sentiment,
               COUNT(*) as count
        FROM news_sentiment
        GROUP BY coin, sentiment
    """

    try:

        df = pd.read_sql_query(query, conn)

    except:

        df = pd.DataFrame()

    conn.close()

    return df

def get_sentiment_timeline():

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT fetched_at,
               sentiment,
               COUNT(*) as count
        FROM news_sentiment
        GROUP BY fetched_at, sentiment
        ORDER BY fetched_at
    """

    try:

        df = pd.read_sql_query(query, conn)

    except:

        df = pd.DataFrame()

    conn.close()

    return df