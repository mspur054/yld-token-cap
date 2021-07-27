import datetime as dt
import logging
import sys
import requests
import json

CURRENCIES = ['usd', 'btc', 'eth']
MKT_FIELDS_TO_KEEP = ['current_price', 'ath','ath_date', 'atl_date', 'atl', 'market_cap',]

def get_token_exchange_data():
    url = 'https://api.coingecko.com/api/v3/coins/yield-app?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=false'

    try:
        res = requests.get(url)
    except requests.ConnectionError as e:
        logging.error(f"Was not able to connect to API, {e}")
        sys.exit(1)
    return res.json() 


def flatten(dct:dict[str,any])->dict[str,any]:
    #flatten dictionary joining keys outer + inner
    outer = {}
    for key, val in dct.items():
        if isinstance(val, dict):
            val = [val]
        if isinstance(val, list):
            for subdict in val:
                deeper = flatten(subdict).items()
                outer.update({key+'_'+key2:val2 for key2,val2 in deeper})
        else:
            outer[key] = val
    
    return outer


def filter_data(initial_data:dict[str,any])->dict[str,any]:
    
    dct = {my_key:{x: initial_data.get(my_key).get(x) for x in initial_data.get(my_key) if x in CURRENCIES} for my_key in MKT_FIELDS_TO_KEEP}

    return dct
    

def get_cleaned_data():
    initial = get_token_exchange_data()
    dct = {}
    dct['id'] = initial['id']
    # filter and flatten and add
    dct.update(flatten(filter_data(initial)))
    dct['last_updated'] = initial['last_updated']






