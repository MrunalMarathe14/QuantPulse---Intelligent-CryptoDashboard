# ml/predict.py

import sqlite3
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DB_PATH = "data/crypto.db"


def get_btc_prediction():

    try:

        conn = sqlite3.connect(DB_PATH)

        query = """
            SELECT
                fetched_at,
                price_usd,
                total_volume,
                market_cap,
                price_change_percentage_24h
            FROM crypto_prices
            WHERE symbol='btc'
            ORDER BY fetched_at
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        if len(df) < 20:
            return None

        # ─────────────────────────────
        # FEATURE ENGINEERING
        # ─────────────────────────────

        df["returns"] = df["price_usd"].pct_change()

        df["volume_change"] = (
            df["total_volume"].pct_change()
        )

        df["marketcap_change"] = (
            df["market_cap"].pct_change()
        )

        df["future_price"] = (
            df["price_usd"].shift(-1)
        )

        df["target"] = (
            df["future_price"] > df["price_usd"]
        ).astype(int)

        df.dropna(inplace=True)

        features = [
            "returns",
            "volume_change",
            "marketcap_change",
            "price_change_percentage_24h"
        ]

        X = df[features]

        y = df["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        # ─────────────────────────────
        # TRAIN MODEL
        # ─────────────────────────────

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        # ─────────────────────────────
        # LATEST PREDICTION
        # ─────────────────────────────

        latest_features = X.iloc[-1:]

        pred = model.predict(latest_features)[0]

        probabilities = model.predict_proba(
            latest_features
        )[0]

        confidence = max(probabilities) * 100

        direction = "UP" if pred == 1 else "DOWN"

        return {
            "prediction": direction,
            "confidence": confidence,
            "model_accuracy": accuracy * 100
        }

    except Exception as e:

        print("ML Error:", e)

        return None