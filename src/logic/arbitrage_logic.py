from models.pair import Pair, TriangularPair
from models.symbol import Symbol
from copy import deepcopy

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

def calculate_surface_rate(pair: TriangularPair, prices: list[Symbol]):
        
    a_base = pair.pair_a_base
    b_base = pair.pair_b_base 
    c_base = pair.pair_c_base
    
    a_quote = pair.pair_a_quote
    b_quote = pair.pair_b_quote
    c_quote = pair.pair_c_quote


    a_pair = f"{a_base}{a_quote}"
    
    a_ask = next((x.ask_price for x in prices if x.symbol == a_pair), None)
    print(f"{a_pair}: {a_ask}")
