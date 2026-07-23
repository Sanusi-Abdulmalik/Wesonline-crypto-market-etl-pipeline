-- ============================================================
-- SILVER LAYER
-- ============================================================

BEGIN;

-- ============================================================
-- Create Schema
-- ============================================================

CREATE SCHEMA IF NOT EXISTS crypto_market.silver;

-- ============================================================
-- Create Main Table
-- ============================================================

CREATE TABLE IF NOT EXISTS crypto_market.silver.crypto_prices (

    id STRING,
    symbol STRING,
    name STRING,

    current_price FLOAT,
    market_cap FLOAT,
    market_cap_rank INTEGER,

    fully_diluted_valuation FLOAT,

    total_volume FLOAT,

    high_24h FLOAT,
    low_24h FLOAT,

    price_change_24h FLOAT,
    price_change_percentage_24h FLOAT,

    market_cap_change_24h FLOAT,
    market_cap_change_percentage_24h FLOAT,

    circulating_supply FLOAT,
    total_supply FLOAT,
    max_supply FLOAT,

    ath FLOAT,
    ath_change_percentage FLOAT,
    ath_date TIMESTAMP_NTZ,

    atl FLOAT,
    atl_change_percentage FLOAT,
    atl_date TIMESTAMP_NTZ,

    last_updated TIMESTAMP_NTZ,

    batch_id STRING,
    pipeline_name STRING,
    pipeline_version STRING,
    environment STRING,
    ingested_at TIMESTAMP_NTZ
);

-- ============================================================
-- Create Staging Table
-- ============================================================

DROP TABLE IF EXISTS crypto_market.silver.crypto_prices_stage;

CREATE TRANSIENT TABLE crypto_market.silver.crypto_prices_stage
LIKE crypto_market.silver.crypto_prices;

-- ============================================================
-- Ensure Stage Table is Empty
-- ============================================================

TRUNCATE TABLE crypto_market.silver.crypto_prices_stage;

-- ============================================================
-- Load Latest Parquet Files
-- ============================================================

COPY INTO crypto_market.silver.crypto_prices_stage
FROM @CRYPTO_MARKET.SILVER.CRYPTO_STAGE
FILE_FORMAT = (
    FORMAT_NAME = 'CRYPTO_MARKET.SILVER.MY_PARQUET_FORMAT'
)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

-- ============================================================
-- Merge into Silver
-- ============================================================

MERGE INTO crypto_market.silver.crypto_prices AS target
USING (

    SELECT *
    FROM crypto_market.silver.crypto_prices_stage
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY id
        ORDER BY ingested_at DESC
    ) = 1

) source
ON target.id = source.id

WHEN MATCHED THEN
UPDATE SET

    symbol = source.symbol,
    name = source.name,

    current_price = source.current_price,
    market_cap = source.market_cap,
    market_cap_rank = source.market_cap_rank,

    fully_diluted_valuation = source.fully_diluted_valuation,
    total_volume = source.total_volume,

    high_24h = source.high_24h,
    low_24h = source.low_24h,

    price_change_24h = source.price_change_24h,
    price_change_percentage_24h = source.price_change_percentage_24h,

    market_cap_change_24h = source.market_cap_change_24h,
    market_cap_change_percentage_24h =
        source.market_cap_change_percentage_24h,

    circulating_supply = source.circulating_supply,
    total_supply = source.total_supply,
    max_supply = source.max_supply,

    ath = source.ath,
    ath_change_percentage = source.ath_change_percentage,
    ath_date = source.ath_date,

    atl = source.atl,
    atl_change_percentage = source.atl_change_percentage,
    atl_date = source.atl_date,

    last_updated = source.last_updated,

    batch_id = source.batch_id,
    pipeline_name = source.pipeline_name,
    pipeline_version = source.pipeline_version,
    environment = source.environment,
    ingested_at = source.ingested_at

WHEN NOT MATCHED THEN
INSERT (

    id,
    symbol,
    name,

    current_price,
    market_cap,
    market_cap_rank,

    fully_diluted_valuation,

    total_volume,

    high_24h,
    low_24h,

    price_change_24h,
    price_change_percentage_24h,

    market_cap_change_24h,
    market_cap_change_percentage_24h,

    circulating_supply,
    total_supply,
    max_supply,

    ath,
    ath_change_percentage,
    ath_date,

    atl,
    atl_change_percentage,
    atl_date,

    last_updated,

    batch_id,
    pipeline_name,
    pipeline_version,
    environment,
    ingested_at

)
VALUES (

    source.id,
    source.symbol,
    source.name,

    source.current_price,
    source.market_cap,
    source.market_cap_rank,

    source.fully_diluted_valuation,

    source.total_volume,

    source.high_24h,
    source.low_24h,

    source.price_change_24h,
    source.price_change_percentage_24h,

    source.market_cap_change_24h,
    source.market_cap_change_percentage_24h,

    source.circulating_supply,
    source.total_supply,
    source.max_supply,

    source.ath,
    source.ath_change_percentage,
    source.ath_date,

    source.atl,
    source.atl_change_percentage,
    source.atl_date,

    source.last_updated,

    source.batch_id,
    source.pipeline_name,
    source.pipeline_version,
    source.environment,
    source.ingested_at
);

-- ============================================================
-- Cleanup
-- ============================================================

TRUNCATE TABLE crypto_market.silver.crypto_prices_stage;

COMMIT;