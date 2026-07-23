-- ============================================================
-- GOLD LAYER
-- ============================================================

CREATE SCHEMA IF NOT EXISTS crypto_market.gold;

-- ============================================================
-- TOP 100 CRYPTOCURRENCIES
-- ============================================================

CREATE OR REPLACE VIEW crypto_market.gold.top_100_crypto AS

SELECT

    id,
    symbol,
    name,

    current_price,

    market_cap,

    market_cap_rank,

    total_volume,

    price_change_percentage_24h,

    last_updated

FROM crypto_market.silver.crypto_prices

ORDER BY market_cap_rank;

-- ============================================================
-- MARKET SUMMARY
-- ============================================================

CREATE OR REPLACE VIEW crypto_market.gold.market_summary AS

SELECT

    COUNT(*) AS total_assets,

    SUM(market_cap) AS total_market_cap,

    SUM(total_volume) AS total_volume,

    AVG(price_change_percentage_24h)
        AS average_price_change

FROM crypto_market.silver.crypto_prices;

-- ============================================================
-- TOP GAINERS
-- ============================================================

CREATE OR REPLACE VIEW crypto_market.gold.top_gainers AS

SELECT *

FROM crypto_market.silver.crypto_prices

ORDER BY price_change_percentage_24h DESC

LIMIT 10;

-- ============================================================
-- TOP LOSERS
-- ============================================================

CREATE OR REPLACE VIEW crypto_market.gold.top_losers AS

SELECT *

FROM crypto_market.silver.crypto_prices

ORDER BY price_change_percentage_24h ASC

LIMIT 10;

-- ============================================================
-- MARKET CAP DISTRIBUTION
-- ============================================================

CREATE OR REPLACE VIEW crypto_market.gold.market_cap_distribution AS

SELECT

    name,

    symbol,

    market_cap

FROM crypto_market.silver.crypto_prices

ORDER BY market_cap DESC;