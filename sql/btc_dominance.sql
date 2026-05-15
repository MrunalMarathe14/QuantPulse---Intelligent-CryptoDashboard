-- Bitcoin & Ethereum Market Dominance
-- Shows BTC%, ETH%, and Altcoin% of total market

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
    ROUND((total_mcap - btc_mcap - eth_mcap) / total_mcap * 100, 2) AS altcoin_pct
FROM totals;