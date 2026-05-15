-- Top 10 Crypto Gainers (Last 24 Hours)
-- Uses the most recent data snapshot from the crypto_prices table

SELECT 
    name,
    symbol,
    price_usd,
    price_change_percentage_24h,
    market_cap
FROM crypto_prices
WHERE fetched_at = (SELECT MAX(fetched_at) FROM crypto_prices)
  AND price_change_percentage_24h IS NOT NULL
ORDER BY price_change_percentage_24h DESC
LIMIT 10;