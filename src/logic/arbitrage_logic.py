from models.pair import Pair, TriangularPair
from models.symbol import Symbol
from enum import Enum

class Direction(Enum):
    FORWARD = 1
    REVERSE = 2

def find_all_triangular_pairs(pairs: list[Pair]) -> list[TriangularPair]:
        
    found_pairs: list[TriangularPair] = []
    
    for firstPair in pairs:
        for secondPair in pairs:
            if firstPair != secondPair and firstPair.baseAsset != firstPair.quoteAsset and secondPair.baseAsset != secondPair.quoteAsset and (firstPair.baseAsset == secondPair.baseAsset or firstPair.baseAsset == secondPair.quoteAsset or firstPair.quoteAsset == secondPair.baseAsset or firstPair.quoteAsset == secondPair.quoteAsset):
                for thirdPair in pairs:
                    if (thirdPair == firstPair or thirdPair == secondPair or thirdPair.baseAsset == thirdPair.quoteAsset):
                        continue
                    basket = [firstPair.baseAsset, firstPair.quoteAsset, secondPair.baseAsset, secondPair.quoteAsset, thirdPair.baseAsset, thirdPair.quoteAsset]
                    pair_found = True
                    for item in basket:
                        appearance_counter = 0
                        for lookupItem in basket:
                            if item == lookupItem:
                                appearance_counter += 1
                        if appearance_counter != 2:
                            pair_found = False
                            break
                    if pair_found == True:
                        new_pair = TriangularPair(pair_a_base=firstPair.baseAsset, pair_b_base=secondPair.baseAsset, pair_c_base=thirdPair.baseAsset, pair_a_quote=firstPair.quoteAsset, pair_b_quote=secondPair.quoteAsset, pair_c_quote=thirdPair.quoteAsset)
                        if new_pair.pair in [x.pair for x in found_pairs]:
                            pair_found = False
                        else:
                            found_pairs.append(new_pair)
    return found_pairs


    '''
    Binance - stronger coin is always on the left, ex: BTCUSDT so if going from the Base to the Quote (BTC -> USDT) we should * (Bid)
    if going from the Quote to the Base (BTC <- USDT) we should * (1 / Ask)
    '''
def calculate_surface_rate(pair: TriangularPair, prices: list[Symbol]):

    min_surface_rate = 0.1
    starting_amount = 1
    surface_dict = {}
    contract_2 = ""
    contract_3 = ""
    direction_trade_1 = ""
    direction_trade_2 = ""
    direction_trade_3 = ""
    acquired_coin_t2 = 0
    acquired_coin_t3 = 0
    calculated = False
    tax_rate_perc = 0.001
    
    a_base = pair.pair_a_base
    b_base = pair.pair_b_base 
    c_base = pair.pair_c_base
    
    a_quote = pair.pair_a_quote
    b_quote = pair.pair_b_quote
    c_quote = pair.pair_c_quote

    a_pair = f"{a_base}{a_quote}"
    b_pair = f"{b_base}{b_quote}"
    c_pair = f"{c_base}{c_quote}"

    a_ask = float(next((x.ask_price for x in prices if x.symbol == a_pair), None))
    a_bid = float(next((x.bid_price for x in prices if x.symbol == a_pair), None))
    
    b_ask = float(next((x.ask_price for x in prices if x.symbol == b_pair), None))
    b_bid = float(next((x.bid_price for x in prices if x.symbol == b_pair), None))

    c_ask = float(next((x.ask_price for x in prices if x.symbol == c_pair), None))
    c_bid = float(next((x.bid_price for x in prices if x.symbol == c_pair), None))
        
    directions = [Direction.FORWARD, Direction.REVERSE]
    for direction in directions:
        
        calculated = False
        
        # Set additional variables for swap information
        swap_1 = 0
        swap_2 = 0
        swap_3 = 0
        swap_1_rate = 0
        swap_2_rate = 0
        swap_3_rate = 0
        swap_1_tax = 0
        swap_2_tax = 0
        swap_3_tax = 0
        

        if direction == Direction.FORWARD:
            swap_1 = a_base
            swap_2 = a_quote
            
            swap_1_rate = 1 * a_bid           
            direction_trade_1 = "base_to_quote"
            
        if direction == Direction.REVERSE:
            swap_1 = a_quote
            swap_2 = a_base
            
            swap_1_rate = 1 * (1 / a_ask)
            direction_trade_1 = "quote_to_base"

        # Place first trade
        contract_1 = a_pair
        
        acquired_coin_t1 = starting_amount * swap_1_rate
        swap_1_tax = starting_amount * tax_rate_perc
        acquired_coin_t1_after_tax = (starting_amount - swap_1_tax) * swap_1_rate
        
        '''Scenario 1: a_quote maches b_quote'''
        if direction == Direction.FORWARD:       
            if a_quote == b_quote and calculated == False:
                swap_2_rate = 1 * (1 / b_ask)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate
                direction_trade_2 = "quote_to_base"
                contract_2 = b_pair
                
                if b_base == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 * (c_bid)
                    direction_trade_2 = "base_to_quote"
                    contract_3 = c_pair

                if b_base == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = 1 * (1 / c_ask)
                    direction_trade_2 = "quote_to_base"
                    contract_3 = c_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate

                calculated = True
                
        '''Scenario 2: a_quote maches b_base'''
        if direction == Direction.FORWARD:       
            if a_quote == b_base and calculated == False:
                swap_2_rate = 1 * (b_bid)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate

                direction_trade_2 = "base_to_quote"
                contract_2 = b_pair
                
                if b_quote == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 * (c_bid)
                    direction_trade_2 = "base_to_quote"
                    contract_3 = c_pair

                if b_quote == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = 1 * (1 / c_ask)
                    direction_trade_2 = "quote_to_base"
                    contract_3 = c_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate

                calculated = True
                
        '''Scenario 3: a_quote maches c_base'''
        if direction == Direction.FORWARD:       
            if a_quote == c_base and calculated == False:
                swap_2_rate = 1 * (c_bid)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate

                direction_trade_2 = "base_to_quote"
                contract_2 = c_pair
                
                if c_base == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 * (b_bid)
                    direction_trade_2 = "base_to_quote"
                    contract_3 = b_pair

                if c_base == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = 1 * (1 / b_ask)
                    direction_trade_2 = "quote_to_base"
                    contract_3 = b_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate

                calculated = True
                
        '''Scenario 4: a_quote maches c_quote'''
        if direction == Direction.FORWARD:       
            
            if a_quote == c_quote and calculated == False:
                swap_2_rate = 1 * (1 / c_ask)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate

                direction_trade_2 = "quote_to_base"
                contract_2 = b_pair
                
                if c_quote == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 * (b_bid)
                    direction_trade_2 = "base_to_quote"
                    contract_3 = b_pair

                if c_quote == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = 1 * (1 / b_ask)
                    direction_trade_2 = "quote_to_base"
                    contract_3 = b_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate

                calculated = True
                
        '''Scenario 1: a_base maches b_quote'''
        if direction == Direction.REVERSE:       
            if a_base == b_quote and calculated == False:
                swap_2_rate = 1 * (1 / b_ask)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate

                direction_trade_2 = "quote_to_base"
                contract_2 = b_pair
                
                if b_base == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 * (c_bid)
                    direction_trade_3 = "base_to_quote"
                    contract_3 = c_pair

                if b_base == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = 1 * (1 / c_ask)
                    direction_trade_3 = "quote_to_base"
                    contract_3 = c_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate

                calculated = True
                
        '''Scenario 2: a_base maches b_base'''
        if direction == Direction.REVERSE:       
            if a_base == b_base and calculated == False:
                swap_2_rate = 1 * (b_bid)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate
                
                direction_trade_2 = "base_to_quote"
                contract_2 = b_pair
                
                if b_quote == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 * (c_bid)
                    direction_trade_3 = "base_to_quote"
                    contract_3 = c_pair

                if b_quote == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = 1 * (1 / c_ask)
                    direction_trade_3 = "quote_to_base"
                    contract_3 = c_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate
                
                calculated = True
                
        '''Scenario 3: a_base maches c_quote'''
        if direction == Direction.REVERSE:       
            if a_base == c_quote and calculated == False:
                swap_2_rate = 1 * (1 / c_ask)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate
                
                direction_trade_2 = "quote_to_base"
                contract_2 = c_pair
                
                if c_base == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 * (b_bid)
                    direction_trade_3 = "base_to_quote"
                    contract_3 = b_pair

                if c_base == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = 1 * (1 / b_ask)
                    direction_trade_2 = "quote_to_base"
                    contract_3 = b_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate
                
                calculated = True
                
        '''Scenario 4: a_base maches c_base'''
        if direction == Direction.REVERSE:       
            if a_base == c_base and calculated == False:
                swap_2_rate = 1 * (c_bid)
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                swap_2_tax = acquired_coin_t1 * tax_rate_perc
                acquired_coin_t2_after_tax = (acquired_coin_t1_after_tax - swap_2_tax) * swap_2_rate

                direction_trade_2 = "base_to_quote"
                contract_2 = c_pair
                
                if c_quote == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 * (b_bid)
                    direction_trade_3 = "base_to_quote"
                    contract_3 = b_pair

                if c_quote == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = 1 * (1 / b_ask)
                    direction_trade_3 = "quote_to_base"
                    contract_3 = b_pair
                    
                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                swap_3_tax = acquired_coin_t2 * tax_rate_perc
                acquired_coin_t3_after_tax = (acquired_coin_t2_after_tax - swap_3_tax) * swap_3_rate

                calculated = True
                
        # Trade Descriptions
        trade_description_1 = f"{direction} {contract_1} Start with {swap_1} of {starting_amount}. Swap at {swap_1_rate} for {swap_2} acquiring {acquired_coin_t1} Paid fees: {swap_1_tax} Left after fees: {acquired_coin_t1_after_tax}."
        trade_description_2 = f"{direction} {contract_2} Swap {acquired_coin_t1} of {swap_2} at {swap_2_rate} for {swap_3} acquiring {acquired_coin_t2}. Paid fees: {swap_2_tax} Left after fees: {acquired_coin_t2_after_tax}"
        trade_description_3 = f" {direction} {contract_3} Swap {acquired_coin_t2} of {swap_3} at {swap_3_rate} for {swap_1} acquiring {acquired_coin_t3}. Paid fees: {swap_3_tax} Left after fees: {acquired_coin_t3_after_tax}"
        
        profit_loss = acquired_coin_t3 - starting_amount
        profit_loss_perc = (profit_loss / starting_amount) * 100 if profit_loss != 0 else 0
        
        profit_loss_after_tax = acquired_coin_t3_after_tax - starting_amount
        profit_loss_perc_after_tax = (profit_loss_after_tax / starting_amount) * 100 if profit_loss != 0 else 0


        if (profit_loss_perc_after_tax > 0):     
            if (acquired_coin_t3 > starting_amount):
                print(f"NEW TRADE Profit and loss percentage: {profit_loss_perc}% after taxes of {tax_rate_perc}% per trade it is left: {profit_loss_perc_after_tax}%")
                print(trade_description_1)
                print(trade_description_2)
                print(trade_description_3)