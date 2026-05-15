# 📊 Crypto Market Intelligence Dashboard

> **Problem**: Manually tracking crypto market movements across 100+ coins is slow, error-prone, and doesn't scale.
> **Solution**: An automated pipeline that fetches live data via API, stores it in SQL, and visualizes it in an interactive dashboard.
> **Result**: Zero manual effort — data refreshes every 15 minutes with full historical tracking.

---

## Live Preview

![Dashboard Overview](screenshots/dashboard_overview.png)

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Data Source | CoinGecko REST API |
| Storage | SQLite (via Python sqlite3) |
| Processing | Python, Pandas |
| SQL Analysis | SQLite queries |
| Dashboard | Streamlit + Plotly |
| Scheduling | APScheduler |

---

## Features

- **Live API Fetching** — Pulls top 100 coins by market cap from CoinGecko
- **SQL Analytics** — 5+ queries: top gainers/losers, volume analysis, BTC dominance, volatility ranking
- **Interactive Dashboard** — 4 tabs with charts, treemaps, scatter plots, and KPI cards
- **Auto-Scheduler** — Refreshes every 15 minutes, logs all pipeline runs
- **Historical Tracking** — Every fetch is stored, enabling price history analysis

---

## SQL Queries

All queries are in `/sql` folder. Key analyses:

| Query | File | Description |
|-------|------|-------------|
| Top Gainers | `top_gainers.sql` | 24h best performers |
| Volume/MCap | `volume_vs_marketcap.sql` | Trading activity ratio |
| BTC Dominance | `btc_dominance.sql` | Market share analysis |
| Volatility | `volatility_rank.sql` | Most volatile coins |
| Overview | `market_overview.sql` | Summary statistics |

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/crypto-market-intelligence-dashboard
cd crypto-market-intelligence-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fetch initial data
python fetch_data.py

# 4. Launch dashboard
streamlit run dashboard.py

# 5. (Optional) Start auto-scheduler in a separate terminal
python scheduler.py
```

---

## Project Structure

```
├── data/crypto.db          # SQLite database
├── sql/                    # All SQL queries as .sql files
├── fetch_data.py           # API → Database pipeline
├── queries.py              # SQL query functions
├── dashboard.py            # Streamlit dashboard
├── scheduler.py            # 15-min auto-refresh
└── requirements.txt
```

---

*Built as a portfolio project demonstrating end-to-end data pipeline skills: API integration, SQL analysis, Python data processing, and dashboard visualization.*