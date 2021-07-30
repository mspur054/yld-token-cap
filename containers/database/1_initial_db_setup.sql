DROP TABLE IF EXISTS crypto.yldapp;
DROP SCHEMA IF EXISTS crypto;
CREATE SCHEMA crypto;
CREATE TABLE crypto.yldapp (
    id VARCHAR(50) NOT NULL,
    price_btc NUMERIC(12,10),
    price_eth NUMERIC(12,10),
    price_usd NUMERIC(12,6) NOT NULL,
    ath_btc NUMERIC(12,10),
    ath_eth NUMERIC(12,10),
    ath_usd NUMERIC(12,6),
    ath_date_btc TIMESTAMP,
    ath_date_eth TIMESTAMP,
    ath_date_usd TIMESTAMP,
    atl_date_btc TIMESTAMP,
    atl_date_eth TIMESTAMP,
    atl_date_usd TIMESTAMP,
    atl_btc NUMERIC(12,10),
    atl_eth NUMERIC(12,10),
    atl_usd NUMERIC(12,6),
    market_cap_btc BIGINT,
    market_cap_eth BIGINT,
    market_cap_usd BIGINT,
    last_updated TIMESTAMP NOT NULL,
    added_to_table TIMESTAMP without time zone default (now() at time zone 'utc')
);

