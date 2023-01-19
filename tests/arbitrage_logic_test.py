from logic.arbitrage_logic import find_all_triangular_pairs
from models.pair import Pair

def test_find_all_triangular_pairs_should_find_one_pair():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="LTC")]
    
    result = find_all_triangular_pairs(input_pairs)
        
    assert len(result) == 1
    
def test_find_all_triangular_pairs_should_find_zero_pairs_1():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BNB", quoteAsset="LTC")]
    
    result = find_all_triangular_pairs(input_pairs)
    
    assert len(result) == 0
    
def test_find_all_triangular_pairs_should_find_zero_pairs_2():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="BTC"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="LTC", quoteAsset="ETH")]
    
    result = find_all_triangular_pairs(input_pairs)
            
    assert len(result) == 0
    
def test_find_all_triangular_pairs_should_find_two_pairs_1():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="LTC"),
                   Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="BTC", quoteAsset="LTC"),
                   Pair(baseAsset="BNB", quoteAsset="BTC"), Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="BNB")]
    
    result = find_all_triangular_pairs(input_pairs)
    
    assert len(result) == 2
    
def test_find_all_triangular_pairs_should_find_two_pairs_2():
    input_pairs = [Pair(baseAsset="BTC", quoteAsset="ETH"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="LTC"),
                   Pair(baseAsset="ETH", quoteAsset="BTC"), Pair(baseAsset="ETH", quoteAsset="LTC"), Pair(baseAsset="BTC", quoteAsset="LTC")]
    
    result = find_all_triangular_pairs(input_pairs)
    
    print(result)
        
    assert len(result) == 2