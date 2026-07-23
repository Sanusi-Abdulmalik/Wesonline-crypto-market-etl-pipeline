-- 01 Row Count
SELECT
'01_row_count',
IFF(COUNT(*) = 0, 1, 0)
FROM crypto_market.silver.crypto_prices;

-- 02 Duplicate IDs within Batch
SELECT
'02_duplicate_id_batch',
COUNT(*)
FROM (
    SELECT id, batch_id
    FROM crypto_market.silver.crypto_prices
    GROUP BY id, batch_id
    HAVING COUNT(*) > 1
);

-- 03 Required Columns
SELECT
'03_null_checks',
COUNT(*)
FROM crypto_market.silver.crypto_prices
WHERE
id IS NULL
OR symbol IS NULL
OR name IS NULL;

-- 04 Negative Values
SELECT
'04_negative_values',
COUNT(*)
FROM crypto_market.silver.crypto_prices
WHERE
current_price < 0
OR market_cap < 0
OR total_volume < 0;

-- 05 Future Dates (5-minute tolerance)
SELECT
'05_future_dates',
COUNT(*)
FROM crypto_market.silver.crypto_prices
WHERE
last_updated > DATEADD(MINUTE, 5, CURRENT_TIMESTAMP());

-- 06 Invalid Market Rank
SELECT
'06_invalid_market_rank',
COUNT(*)
FROM crypto_market.silver.crypto_prices
WHERE
market_cap_rank IS NOT NULL
AND market_cap_rank <= 0;