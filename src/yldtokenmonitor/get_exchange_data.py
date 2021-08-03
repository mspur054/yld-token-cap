import datetime as dt
import logging
import os
import sys

import requests

from yldtokenmonitor.util.connect import Database
from yldtokenmonitor.util.db_config import get_db_config


def _get_token_exchange_data()->dict:
    """
    Uses the coingecko api to get token data

    Returns:
        [type]: [description]
    """
    url = 'https://api.coingecko.com/api/v3/coins/yield-app?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=false'

    try:
        res = requests.get(url)
    except requests.ConnectionError as e:
        logging.error(f"Was not able to connect to the API, {e}")
        sys.exit(1)
    return res.json()


def flatten(dct: dict[str, any]) -> dict[str, any]:
    """Flatten dictionary joining keys outer + inner

    Args:
        dct (dict[str, any]): [description]

    Returns:
        dict[str, any]: flattened dictionary
    """    

    outer = {}
    for key, val in dct.items():
        if isinstance(val, dict):
            val = [val]
        if isinstance(val, list):
            for subdict in val:
                deeper = flatten(subdict).items()
                outer.update({key+'_'+key2: val2 for key2, val2 in deeper})
        else:
            outer[key] = val

    return outer


def filter_data(initial_data: dict[str, any]) -> dict[str, any]:
    """filters API data to only keep required fields and currencies

    Args:
        initial_data (dict[str, any]): initial data that has been flattened

    Returns:
        dict[str, any]: filtered api data 
    """
    CURRENCIES = ['usd', 'btc', 'eth']
    MKT_FIELDS_TO_KEEP = ['current_price', 'ath',
                          'ath_date', 'atl_date', 'atl', 'market_cap', ]

    return {
        my_key: {
            x: initial_data.get(my_key).get(x)
            for x in initial_data.get(my_key)
            if x in CURRENCIES
        }
        for my_key in MKT_FIELDS_TO_KEEP
    }


def get_cleaned_data()->dict[str,any]:
    """Pulls data from api and prepares it for upload

    Returns:
        [type]: [description]
    """    
    initial = _get_token_exchange_data()
    dct = {'id': initial['id']}
    # filter and flatten and add
    dct.update(flatten(filter_data(initial['market_data'])))
    dct['last_updated'] = initial['last_updated']

    return dct


def __crypto_insert_query() -> str:
    """SQL query to insert data into database

    Returns:
        str: insert query
    """    
    return '''
        INSERT INTO crypto.yldapp (
            id,
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
        )
        VALUES (
             %(id)s,
             %(current_price_btc)s,
             %(current_price_eth)s,
             %(current_price_usd)s,
             %(ath_btc)s,
             %(ath_eth)s,
             %(ath_usd)s,
             %(ath_date_btc)s,
             %(ath_date_eth)s,
             %(ath_date_usd)s,
             %(atl_date_btc)s,
             %(atl_date_eth)s,
             %(atl_date_usd)s,
             %(atl_btc)s,
             %(atl_eth)s,
             %(atl_usd)s,
             %(market_cap_btc)s,
             %(market_cap_eth)s,
             %(market_cap_usd)s,
             %(last_updated)s
        );
    '''


def main() -> None:
    """Extract, clean and load data into database
    """    
    token_data = get_cleaned_data()
    with Database(**get_db_config()).managed_cursor() as cur:
        cur.execute(__crypto_insert_query(), token_data)
        print('done inserting')


if __name__ == "__main__":
    main()
