# analytics/sentiment.py

import feedparser
from transformers import pipeline
import pandas as pd

from store_sentiment import store_sentiment

# ─────────────────────────────────────────────
# LOAD FINBERT MODEL
# ─────────────────────────────────────────────

classifier = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

# ─────────────────────────────────────────────
# COIN DETECTION
# ─────────────────────────────────────────────

COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "dogecoin": "DOGE",
    "ripple": "XRP"
}

def detect_coin(title):

    title_lower = title.lower()

    for keyword, symbol in COINS.items():

        if keyword in title_lower:
            return symbol

    return "GENERAL"

# ─────────────────────────────────────────────
# FETCH NEWS
# ─────────────────────────────────────────────

def fetch_crypto_news(limit=10):

    url = "https://www.coindesk.com/arc/outboundfeeds/rss/"

    feed = feedparser.parse(url)

    news_data = []

    for entry in feed.entries[:limit]:

        news_data.append({
            "title": entry.title,
            "published": entry.published
        })

    return pd.DataFrame(news_data)

# ─────────────────────────────────────────────
# SENTIMENT ANALYSIS
# ─────────────────────────────────────────────

def analyze_sentiment(df):

    sentiments = []
    scores = []
    coins = []

    for title in df["title"]:

        result = classifier(title)[0]

        sentiments.append(result["label"])
        scores.append(round(result["score"], 4))
        coins.append(detect_coin(title))

    df["sentiment"] = sentiments
    df["confidence"] = scores
    df["coin"] = coins

    return df

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":

    news_df = fetch_crypto_news(limit=10)

    sentiment_df = analyze_sentiment(news_df)

    store_sentiment(sentiment_df)

    print("\n===== SENTIMENT RESULTS =====\n")

    print(sentiment_df.head())