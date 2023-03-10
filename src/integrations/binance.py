import os
import requests
from constants.constants import *
from models.pair import Pair
from models.symbol import Symbol

def get_binance_tradeable_pairs() -> list[Pair]:
    pairs = []
    base_url = os.environ[BINANCE_BASE_ENDPOINT] 
    url = f"{base_url}{BINANCE_EXCHANGE_INFORMATION_API}?permissions=SPOT"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Binance API Exchange Info Returned: {response.status_code}')
    for symbol in response.json()["symbols"]:
        if symbol["status"] == "TRADING" and symbol["isSpotTradingAllowed"] == True:
            pairs.append(Pair(symbol["baseAsset"], symbol["quoteAsset"]))
    return pairs

def get_binance_book_tickers() -> list[Symbol]:
    symbols = []
    base_url = os.environ[BINANCE_BASE_ENDPOINT] 
    url = f"{base_url}{BINANCE_BOOK_TICKER_API}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f'Binance API Book Tickers API Returned: {response.status_code}')
    for symbol in response.json():
        symbols.append(Symbol(symbol=symbol["symbol"], ask_price=symbol["askPrice"], bid_price=symbol["bidPrice"]))
    return symbols
