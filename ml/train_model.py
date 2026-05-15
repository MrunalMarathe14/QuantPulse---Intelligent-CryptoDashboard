# ml/train_model.py

import sqlite3
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

DB_PATH = "data/crypto.db"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)

query = """
SELECT *
FROM crypto_prices
WHERE symbol='btc'
ORDER BY fetched_at
"""

df = pd.read_sql_query(query, conn)

conn.close()

print(df.head())

# ─────────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────────

df["future_price"] = df["price_usd"].shift(-1)

df["target"] = (
    df["future_price"] > df["price_usd"]
).astype(int)

features = [
    "price_change_percentage_24h",
    "price_change_percentage_7d",
    "total_volume",
    "market_cap",
    "ath_change_percentage"
]

df = df.dropna()

X = df[features]

y = df["target"]

# ─────────────────────────────────────────────
# TRAIN TEST SPLIT
# ─────────────────────────────────────────────

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ─────────────────────────────────────────────
# TRAIN MODEL
# ─────────────────────────────────────────────

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ─────────────────────────────────────────────
# EVALUATION
# ─────────────────────────────────────────────

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"\nModel Accuracy: {accuracy:.2f}")

# ─────────────────────────────────────────────
# SAVE MODEL
# ─────────────────────────────────────────────

joblib.dump(
    model,
    "ml/crypto_prediction_model.pkl"
)

print("\nModel saved successfully.")