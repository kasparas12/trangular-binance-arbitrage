import json
from time import monotonic
from dotenv import load_dotenv
from integrations.binance import get_binance_tradeable_pairs
from logic.arbitrage_logic import find_all_triangular_pairs, transform_triangular_pair_to_dict, transform_dict_to_triangular_pair
from constants.constants import TRIANGULAR_PAIRS_SAVE_FILE_PATH

'''Getting all pairs from Binance and finding triangular pairs'''
'''Might take 7-8 minutes to fully run'''
def step1():
    start_time = monotonic()    
    pairs = get_binance_tradeable_pairs()
    
    triangular_pairs = find_all_triangular_pairs(pairs)    
    
    with open(TRIANGULAR_PAIRS_SAVE_FILE_PATH, 'w') as fp:
        json.dump([transform_triangular_pair_to_dict(x) for x in triangular_pairs], fp)
        
    print(f"Run time {monotonic() - start_time} seconds")
    print(f"Total triangular pairs found: {len(triangular_pairs)}")
    
    
'''Loading triangular pairs from file and calculating surface rates with real-time prices'''
def step2():
     with open(TRIANGULAR_PAIRS_SAVE_FILE_PATH, 'r') as fp:
        loaded_dictionary : dict = json.load(fp)
        triangualr_pairs = [transform_dict_to_triangular_pair(x) for x in loaded_dictionary]
        print(triangualr_pairs)


if __name__ == "__main__":
    load_dotenv()
    
    step1()
    step2()