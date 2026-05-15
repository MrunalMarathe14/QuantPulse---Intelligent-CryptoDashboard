# alert_engine.py

import sqlite3
import pandas as pd

from telegram_alert import send_telegram_alert
DB_PATH = "data/crypto.db"

def check_volatility_alert():

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            name,
            price_change_percentage_24h
        FROM crypto_prices
        ORDER BY fetched_at DESC
        LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    for _, row in df.iterrows():

        change = abs(row["price_change_percentage_24h"])

        if change >= 10:

            msg = f"""
🚨 VOLATILITY ALERT

Coin: {row['name']}
24h Move: {change:.2f}%

Extreme market movement detected.
"""

            send_telegram_alert(msg)

            print("Alert Sent")

if __name__ == "__main__":

    check_volatility_alert()