from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass
class Pair:
    baseAsset: str
    quoteAsset: str
    

@dataclass_json
@dataclass
class TriangularPair:
    pair_a_base: str
    pair_b_base: str
    pair_c_base: str
    
    pair_a_quote: str
    pair_b_quote: str
    pair_c_quote: str
    
    pair: Optional[str] = None
        
    pair_a_ask: Optional[float] = None
    pair_a_bid: Optional[float] = None
    
    pair_b_ask: Optional[float] = None
    pair_b_bid: Optional[float] = None
    
    pair_c_ask: Optional[float] = None
    pair_c_bid: Optional[float] = None
    
    def __post_init__(self):
        self.pair =  ','.join(sorted([f"{self.pair_a_base}{self.pair_a_quote}", f"{self.pair_b_base}{self.pair_b_quote}", f"{self.pair_c_base}{self.pair_c_quote}"]))
    
    def add_bid_ask_prices(self, pair_a_ask: float, pair_a_bid: float, pair_b_ask: float, pair_b_bid: float, pair_c_ask: float, pair_c_bid: float):
        self.pair_a_ask = pair_a_ask
        self.pair_a_bid = pair_a_bid
        
        self.pair_b_ask = pair_b_ask
        self.pair_b_bid = pair_b_bid
        
        self.pair_c_ask = pair_c_ask
        self.pair_c_bid = pair_c_bid