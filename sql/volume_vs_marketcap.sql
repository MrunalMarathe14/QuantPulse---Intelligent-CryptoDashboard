-- Volume to Market Cap Ratio Analysis
-- High ratio = coin is actively traded relative to its size
-- Useful for spotting breakout candidates

SELECT 
    name,
    symbol,
    total_volume,
    market_cap,
    ROUND(
        CAST(total_volume AS FLOAT) / NULLIF(market_cap, 0) * 100, 
        2
    ) AS volume_to_mcap_pct
FROM crypto_prices
WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
  AND market_cap > 0
ORDER BY volume_to_mcap_pct DESC
LIMIT 20;