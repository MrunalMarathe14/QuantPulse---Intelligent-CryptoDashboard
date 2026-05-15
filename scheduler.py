# scheduler.py

from apscheduler.schedulers.blocking import BlockingScheduler
from fetch_data import run_pipeline
from alert_engine import check_volatility_alert
import subprocess
import logging
import os

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ─────────────────────────────────────────────
# BASE DIRECTORY
# ─────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# SCHEDULER
# ─────────────────────────────────────────────

scheduler = BlockingScheduler()

# ───────────────────────────────────────────── 
# MARKET DATA PIPELINE
# ─────────────────────────────────────────────

@scheduler.scheduled_job('interval', minutes=1)
def scheduled_market_fetch():

    logging.info("Running market data pipeline...")

    try:

        run_pipeline()

        logging.info("Market pipeline completed.")

    except Exception as e:

        logging.error(f"Market pipeline failed: {e}")

# ─────────────────────────────────────────────
# SENTIMENT PIPELINE
# ─────────────────────────────────────────────

@scheduler.scheduled_job("interval", minutes=30)
def scheduled_sentiment_fetch():

    logging.info("Running sentiment pipeline...")

    try:

        result = subprocess.run(
            ["python", "analytics/sentiment.py"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )

        logging.info(result.stdout)

        if result.stderr:
            logging.error(result.stderr)

        logging.info("Sentiment pipeline completed.")

    except Exception as e:

        logging.error(f"Sentiment pipeline failed: {e}")

@scheduler.scheduled_job('interval', minutes=15)
def scheduled_fetch():

    logging.info("Fetching market data...")

    run_pipeline()

    check_volatility_alert()

# ─────────────────────────────────────────────
# STARTUP
# ─────────────────────────────────────────────

if __name__ == "__main__":

    logging.info("===================================")
    logging.info("CRYPTO INTELLIGENCE SCHEDULER")
    logging.info("===================================")

    # Run immediately once
    scheduled_market_fetch()
    scheduled_sentiment_fetch()

    logging.info("Scheduler started successfully.")

    scheduler.start()