# QuantPulse — Intelligent CryptoDashboard 📊

A real-time cryptocurrency intelligence platform with sentiment analysis, automated alerts, SQL-powered market analytics, and an experimental ML prediction module.

---

## 🚀 Features

- **Real-Time Data Pipeline** — Fetches live crypto market data and stores it in a local SQLite database
- **Sentiment Analysis** — Analyzes market sentiment and stores results for trend tracking
- **Automated Alerts** — Email and Telegram notifications triggered by market conditions
- **SQL Analytics** — Pre-built queries for BTC dominance and market overview dashboards
- **ML Prediction (WIP)** — Experimental XGBoost-based price prediction module planned for future enhancement
- **Modular Architecture** — Clean separation of concerns across alerts, analytics, data, and ML modules

---

## 🗂️ Project Structure

```
CRYPTODASHBOARD/
│
├── alerts/
│   ├── alert_engine.py          # Core alerting logic
│   ├── email_alerts.py          # Email notification handler
│   └── telegram_alert.py        # Telegram bot integration
│
├── analytics/
│   ├── sentiment.py             # Sentiment analysis engine
│   ├── sentiment_queries.py     # DB queries for sentiment data
│   └── store_sentiment.py       # Sentiment storage handler
│
├── data/
│   ├── crypto.db                # SQLite database (gitignored)
│   └── pipeline.log             # Pipeline execution logs (gitignored)
│
├── ml/
│   ├── train_model.py           # Model training script (XGBoost)
│   ├── predict.py               # Prediction inference script
│   └── crypto_prediction_model.pkl  # Trained model artifact (gitignored)
│
├── sql/
│   ├── btc_dominance.sql        # BTC dominance analytics query
│   └── market_overview.sql      # Market overview analytics query
│
├── screenshots/                 # Project screenshots
├── fetch_data.py                # Main data fetching pipeline
├── queries.py                   # Shared DB query utilities
├── .env                         # Secret keys (gitignored)
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.13 |
| Database | SQLite |
| ML (Experimental) | XGBoost, scikit-learn |
| Alerts | Telegram Bot API, SMTP |
| Analytics | SQL, Pandas |
| Environment | python-dotenv |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/MrunalMarathe14/QuantPulse---Intelligent-CryptoDashboard.git
cd QuantPulse---Intelligent-CryptoDashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver@gmail.com
```

### 4. Run the data pipeline
```bash
python fetch_data.py
```

### 5. Start alerts
```bash
python alerts/alert_engine.py
```

---

## 📈 ML Model (Work in Progress)

> ⚠️ The ML module is currently experimental and not production-ready.

- **Algorithm:** XGBoost Regressor
- **Status:** Prototype — model accuracy is still being improved
- **Artifact:** `ml/crypto_prediction_model.pkl`

### 🔮 Planned Enhancements
- Feature engineering with OHLCV indicators and rolling averages
- Hyperparameter tuning with cross-validation
- LSTM / time-series models for better sequential prediction
- Backtesting framework to evaluate prediction accuracy

---

## 🔔 Alert System

Alerts are triggered based on configurable market conditions:
- Price crossing a threshold
- Unusual volume spikes
- Sentiment shifts

Notifications are sent via **Telegram** and **Email** simultaneously.

---

## 📊 SQL Dashboards

| Query | Description |
|---|---|
| `btc_dominance.sql` | Tracks Bitcoin's market dominance over time |
| `market_overview.sql` | Summarizes top coins by volume, price change, and cap |

---

## 🔒 Security

- All API keys and credentials are stored in `.env` and never committed to version control
- `.env` is listed in `.gitignore`

---

## 🙋‍♀️ Author

**Mrunal Marathe**  
B.Tech Computer Science | MIT World Peace University, Pune  
[GitHub](https://github.com/MrunalMarathe14)

---

## 📄 License

This project is for educational and portfolio purposes.
