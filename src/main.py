import json
from time import monotonic
from dotenv import load_dotenv
from integrations.binance import get_binance_tradeable_pairs, get_binance_book_tickers
from logic.arbitrage_logic import find_all_triangular_pairs, calculate_surface_rate
from constants.constants import TRIANGULAR_PAIRS_SAVE_FILE_PATH
from models.pair import TriangularPair

'''Getting all pairs from Binance and finding triangular pairs'''
'''Might take 7-8 minutes to fully run'''
def step1():
    start_time = monotonic()    
    pairs = get_binance_tradeable_pairs()
    
    triangular_pairs = find_all_triangular_pairs(pairs)    
    
    with open(TRIANGULAR_PAIRS_SAVE_FILE_PATH, 'w') as fp:
        fp.write(TriangularPair.schema().dumps(triangular_pairs, many=True))
        
    print(f"Run time {monotonic() - start_time} seconds")
    print(f"Total triangular pairs found: {len(triangular_pairs)}")
    
    
'''Loading triangular pairs from file and calculating surface rates with real-time prices'''
def step2():
     with open(TRIANGULAR_PAIRS_SAVE_FILE_PATH, 'r') as fp:
        text = fp.read()
        triangualr_pairs = TriangularPair.schema().loads(text, many=True)
        
        prices = get_binance_book_tickers()
        
        for pair in triangualr_pairs:
            calculate_surface_rate(pair, prices)


if __name__ == "__main__":
    load_dotenv()
    
    # step1()
    step2()