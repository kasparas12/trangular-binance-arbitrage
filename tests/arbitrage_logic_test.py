from logic.arbitrage_logic import find_all_triangular_pairs
from models.pair import Pair

def test_find_all_triangular_pairs_should_find_one_pair():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="LTC")]
    
    result = find_all_triangular_pairs(input_pairs)
    
    assert len(result) == 1
    
def test_find_all_triangular_pairs_should_find_zero_pairs():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BNB", quoteAsset="LTC")]
    
    result = find_all_triangular_pairs(input_pairs)
    
    assert len(result) == 0
    
def test_find_all_triangular_pairs_should_find_two_pairs():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="LTC"),
                   Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="BTC", quoteAsset="LTC"),
                   Pair(baseAsset="BNB", quoteAsset="BTC"), Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="BNB")]
    
    result = find_all_triangular_pairs(input_pairs)
    
    assert len(result) == 2