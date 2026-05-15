-- Market Overview Summary Statistics

SELECT
    COUNT(*) AS total_coins_tracked,
    ROUND(SUM(market_cap) / 1e9, 2) AS total_market_cap_billion_usd,
    ROUND(SUM(total_volume) / 1e9, 2) AS total_24h_volume_billion_usd,
    ROUND(AVG(price_change_percentage_24h), 2) AS avg_24h_change_pct,
    COUNT(CASE WHEN price_change_percentage_24h > 0 THEN 1 END) AS coins_up,
    COUNT(CASE WHEN price_change_percentage_24h < 0 THEN 1 END) AS coins_down
FROM crypto_prices
WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices);