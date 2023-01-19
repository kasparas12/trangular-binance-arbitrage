
from attr import dataclass


@dataclass
class Symbol:
    symbol: str
    ask_price: float
    bid_price: float