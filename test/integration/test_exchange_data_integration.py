import json
from decimal import Decimal
import datetime

import psycopg2
import psycopg2.extras
from yldtokenmonitor.get_exchange_data import main
from yldtokenmonitor.util.connect import Database
from yldtokenmonitor.util.db_config import get_db_config


class TestTokenExchange:
    def teardown_method(self):
        with Database(**get_db_config()).managed_cursor() as cur:
            cur.execute("TRUNCATE TABLE crypto.yldapp;")

    def get_exchange_data(self):
        with Database(**get_db_config()).managed_cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                '''SELECT id,
                        price_btc,
                        price_eth,
                        price_usd,
                        ath_btc,
                        ath_eth,
                        ath_usd,
                        ath_date_btc,
                        ath_date_eth,
                        ath_date_usd,
                        atl_date_btc,
                        atl_date_eth,
                        atl_date_usd,
                        atl_btc,
                        atl_eth,
                        atl_usd,
                        market_cap_btc,
                        market_cap_eth,
                        market_cap_usd,
                        last_updated
                        FROM crypto.yldapp;'''
            )
            table_data = [dict(r) for r in cur.fetchall()]
        return table_data

    def test_full_etl_run(self, mocker):
        with open('test/fixtures/sample_raw_token_data.csv') as json_file:
            data = json.load(json_file)
        mocker.patch(
            'yldtokenmonitor.get_exchange_data._get_token_exchange_data',
            return_value=data,
        )
        main()
        expected_result = {
            'id': 'yield-app',
            'price_btc': Decimal('0.0000098300'),
            'price_eth': Decimal('0.0001667800'),
            'price_usd': Decimal('0.376651'),
            'ath_btc': Decimal('0.0000263200'),
            'ath_eth': Decimal('0.0007163500'),
            'ath_usd': Decimal('1.290000'),
            'ath_date_btc': datetime.datetime(2021, 2, 16, 6, 54, 31, 749000),
            'ath_date_eth': datetime.datetime(2021, 2, 16, 6, 54, 31, 749000),
            'ath_date_usd': datetime.datetime(2021, 2, 16, 6, 54, 31, 749000),
            'atl_date_btc': datetime.datetime(2021, 1, 3, 7, 38, 56, 582000),
            'atl_date_eth': datetime.datetime(2021, 6, 1, 13, 37, 41, 689000),
            'atl_date_usd': datetime.datetime(2020, 12, 15, 13, 4, 47, 214000),
            'atl_btc': Decimal('0.0000035100'),
            'atl_eth': Decimal('0.0001062200'),
            'atl_usd': Decimal('0.090129'),
            'market_cap_btc': 1105,
            'market_cap_eth': 18659,
            'market_cap_usd': 42399468,
            'last_updated': datetime.datetime(2021, 7, 27, 21, 59, 10, 600000)
        }

        result = self.get_exchange_data()[0]
        assert result == expected_result
