import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import os

from fetch_data import run_pipeline
from ml.predict import get_btc_prediction

from queries import (
    get_latest_snapshot,
    get_top_gainers,
    get_top_losers,
    get_volume_vs_marketcap,
    get_btc_dominance,
    get_volatility_rank
)

from analytics.sentiment_queries import (
    get_sentiment_distribution,
    get_coin_sentiment,
    get_sentiment_timeline
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="QuantPulse | Crypto Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CACHE FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data(ttl=300)
def load_snapshot():
    return get_latest_snapshot()

@st.cache_data(ttl=300)
def load_dominance():
    return get_btc_dominance()

@st.cache_data(ttl=300)
def load_gainers():
    return get_top_gainers(10)

@st.cache_data(ttl=300)
def load_losers():
    return get_top_losers(10)

@st.cache_data(ttl=300)
def load_volume():
    return get_volume_vs_marketcap()

@st.cache_data(ttl=300)
def load_volatility():
    return get_volatility_rank()

@st.cache_data(ttl=300)
def load_sentiment_distribution():
    return get_sentiment_distribution()

@st.cache_data(ttl=300)
def load_coin_sentiment():
    return get_coin_sentiment()

@st.cache_data(ttl=300)
def load_sentiment_timeline():
    return get_sentiment_timeline()

@st.cache_data(ttl=300)
def load_prediction():
    return get_btc_prediction()

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>

.main {
    background-color: #0d1117;
}

.stMetric {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 15px;
}

div[data-testid="stMetricValue"] {
    color: white;
}

div[data-testid="stMetricLabel"] {
    color: #8b949e;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:

    st.title("⚙️ Controls")

    if st.button("🔄 Refresh Data Now", use_container_width=True):

        with st.spinner("Fetching latest crypto market data..."):
            run_pipeline()

        st.success("Data refreshed successfully!")

    st.divider()

    st.caption("Market Data → CoinGecko API")
    st.caption("News Data → CoinDesk RSS")
    st.caption("Sentiment Model → FinBERT")

    if os.path.exists("data/crypto.db"):

        try:

            conn = sqlite3.connect("data/crypto.db")

            last_fetch = pd.read_sql_query(
                """
                SELECT MAX(fetched_at) as last
                FROM crypto_prices
                """,
                conn
            ).iloc[0]["last"]

            conn.close()

            st.info(f"Last Updated:\n{last_fetch} UTC")

        except:
            st.warning("Database exists but no records found.")

    else:

        st.warning("Database not found.")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.title("📊 QuantPulse")

st.caption("""
AI-powered crypto intelligence platform featuring:

• Real-time market analytics  
• Sentiment intelligence  
• Volatility monitoring  
• ML forecasting  
• Market behavior analysis  
""")

# ─────────────────────────────────────────────
# DATABASE CHECK
# ─────────────────────────────────────────────

if not os.path.exists("data/crypto.db"):

    st.warning("⚠️ No database found. Fetch market data first.")
    st.stop()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market Overview",
    "🏆 Gainers & Losers",
    "💧 Volume Analysis",
    "⚡ Volatility",
    "🧠 Sentiment Intelligence",
    "🤖 ML Forecasting"
])

# ─────────────────────────────────────────────
# TAB 1 — MARKET OVERVIEW
# ─────────────────────────────────────────────

with tab1:

    df = load_snapshot()
    dom = load_dominance()

    if not df.empty:

        col1, col2, col3, col4, col5 = st.columns(5)

        total_mcap = df["market_cap"].sum() / 1e9
        total_vol = df["total_volume"].sum() / 1e9
        avg_change = df["price_change_percentage_24h"].mean()

        col1.metric("Market Cap", f"${total_mcap:,.0f}B")
        col2.metric("24h Volume", f"${total_vol:,.0f}B")
        col3.metric("Avg Change", f"{avg_change:.2f}%")

        col4.metric(
            "Coins Up",
            (df["price_change_percentage_24h"] > 0).sum()
        )

        col5.metric(
            "Coins Down",
            (df["price_change_percentage_24h"] < 0).sum()
        )

        st.divider()

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Top 20 Market Cap Distribution")

            fig_tree = px.treemap(
                df.head(20),
                path=["name"],
                values="market_cap",
                color="price_change_percentage_24h",
                color_continuous_scale=["#f85149", "#3fb950"],
                color_continuous_midpoint=0
            )

            fig_tree.update_layout(height=450)

            st.plotly_chart(
                fig_tree,
                use_container_width=True
            )

        with right:

            st.subheader("Market Dominance")

            if not dom.empty:

                row = dom.iloc[0]

                fig_pie = go.Figure(data=[go.Pie(
                    labels=["BTC", "ETH", "ALT"],
                    values=[
                        row["btc_dominance_pct"],
                        row["eth_dominance_pct"],
                        row["altcoin_dominance_pct"]
                    ],
                    hole=0.5
                )])

                fig_pie.update_layout(height=400)

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True
                )

# ─────────────────────────────────────────────
# TAB 2 — GAINERS / LOSERS
# ─────────────────────────────────────────────

with tab2:

    gainers = load_gainers()
    losers = load_losers()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🚀 Top Gainers")

        fig_g = px.bar(
            gainers,
            x="price_change_percentage_24h",
            y="name",
            orientation="h",
            color="price_change_percentage_24h",
            text="price_change_percentage_24h"
        )

        fig_g.update_traces(
            texttemplate="%{text:.2f}%"
        )

        st.plotly_chart(fig_g, use_container_width=True)

    with col2:

        st.subheader("📉 Top Losers")

        fig_l = px.bar(
            losers,
            x="price_change_percentage_24h",
            y="name",
            orientation="h",
            color="price_change_percentage_24h",
            text="price_change_percentage_24h"
        )

        fig_l.update_traces(
            texttemplate="%{text:.2f}%"
        )

        st.plotly_chart(fig_l, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 3 — VOLUME ANALYSIS
# ─────────────────────────────────────────────

with tab3:

    st.subheader("💧 Volume vs Market Cap")

    vol_df = load_volume()

    fig = px.scatter(
        vol_df,
        x="market_cap",
        y="total_volume",
        size="volume_to_mcap_ratio",
        color="volume_to_mcap_ratio",
        hover_name="name",
        text="symbol"
    )

    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 4 — VOLATILITY
# ─────────────────────────────────────────────

with tab4:

    st.subheader("⚡ Volatility Rankings")

    vol_rank = load_volatility()

    fig = px.bar(
        vol_rank,
        x="name",
        y="volatility_24h",
        color="direction_24h",
        text="volatility_24h"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%"
    )

    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 5 — SENTIMENT
# ─────────────────────────────────────────────

with tab5:

    st.subheader("🧠 Sentiment Intelligence")

    sentiment_df = load_sentiment_distribution()
    coin_df = load_coin_sentiment()
    timeline_df = load_sentiment_timeline()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Sentiment Distribution")

        if not sentiment_df.empty:

            fig_pie = px.pie(
                sentiment_df,
                names="sentiment",
                values="count",
                hole=0.5
            )

            st.plotly_chart(
                fig_pie,
                use_container_width=True
            )

    with col2:

        st.subheader("Coin Sentiment")

        if not coin_df.empty:

            fig_coin = px.bar(
                coin_df,
                x="coin",
                y="count",
                color="sentiment",
                barmode="group"
            )

            st.plotly_chart(
                fig_coin,
                use_container_width=True
            )

    st.divider()

    st.subheader("Rolling Sentiment Trend")

    if not timeline_df.empty:

        score_map = {
            "positive": 1,
            "neutral": 0,
            "negative": -1
        }

        timeline_df["score"] = (
            timeline_df["sentiment"]
            .map(score_map)
        )

        timeline_df["rolling_score"] = (
            timeline_df["score"]
            .rolling(5)
            .mean()
        )

        fig_line = px.line(
            timeline_df,
            x="fetched_at",
            y="rolling_score"
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

    st.divider()

    st.subheader("Latest Sentiment Records")

    try:

        conn = sqlite3.connect("data/crypto.db")

        raw_df = pd.read_sql_query("""
            SELECT
                title,
                sentiment,
                confidence,
                coin,
                fetched_at
            FROM news_sentiment
            ORDER BY id DESC
            LIMIT 20
        """, conn)

        conn.close()

        st.dataframe(
            raw_df,
            use_container_width=True,
            height=400
        )

    except Exception as e:

        st.warning(f"Sentiment error: {e}")

# ─────────────────────────────────────────────
# TAB 6 — ML FORECASTING
# ─────────────────────────────────────────────

with tab6:

    st.subheader("🤖 BTC Direction Prediction")

    prediction = load_prediction()

    if prediction:

        col1, col2, col3 = st.columns(3)

        direction = prediction["prediction"]
        confidence = prediction["confidence"]
        accuracy = prediction["model_accuracy"]

        emoji = "📈" if direction == "UP" else "📉"

        col1.metric(
            "Prediction",
            f"{emoji} {direction}"
        )

        col2.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        col3.metric(
            "Model Accuracy",
            f"{accuracy:.2f}%"
        )

        st.divider()

        st.info("""
Model Features:
• Price momentum  
• Volume movement  
• Market cap changes  
• Short-term volatility  

Algorithm:
RandomForestClassifier
""")

    else:

        st.warning(
            "Not enough historical data for ML prediction."
        )