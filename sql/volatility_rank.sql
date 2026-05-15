-- Volatility Ranking: Most volatile coins in last 24h
-- ABS() gives us the magnitude regardless of direction

SELECT
    name,
    symbol,
    price_usd,
    ABS(price_change_percentage_24h) AS volatility_24h,
    CASE 
        WHEN price_change_percentage_24h > 0 THEN 'UP'
        WHEN price_change_percentage_24h < 0 THEN 'DOWN'
        ELSE 'STABLE'
    END AS direction
FROM crypto_prices
WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
ORDER BY volatility_24h DESC
LIMIT 15;