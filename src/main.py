from time import monotonic
from dotenv import load_dotenv
from integrations.binance import get_binance_tradeable_pairs
from logic.arbitrage_logic import find_all_triangular_pairs

if __name__ == "__main__":
    load_dotenv()
    start_time = monotonic()

    pairs = get_binance_tradeable_pairs()
    triangular_pairs = find_all_triangular_pairs(pairs)
    
    print(f"Run time {monotonic() - start_time} seconds")
    print(f"Total triangular pairs found: {len(triangular_pairs)}")
    
    for x in triangular_pairs:
        print(x)