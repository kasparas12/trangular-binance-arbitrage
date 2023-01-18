from models.pair import Pair

def transform_triangular_pair_to_dict(pair: list[Pair]) -> dict:
    return {
        'a_base': pair[0].baseAsset,
        'b_base': pair[1].baseAsset,
        'c_base': pair[2].baseAsset,
        'a_quote': pair[0].quoteAsset,
        'b_quote': pair[1].quoteAsset,
        'c_quote': pair[2].quoteAsset,
        'pair': f"{pair[0].baseAsset}{pair[0].quoteAsset}_{pair[1].baseAsset}{pair[1].quoteAsset}_{pair[2].baseAsset}{pair[2].quoteAsset}"
    }
    
def transform_dict_to_triangular_pair(pair: dict) -> list[Pair]:
    return [Pair(baseAsset=pair["a_base"], quoteAsset=pair["a_quote"]), Pair(baseAsset=pair["b_base"], quoteAsset=pair["b_quote"]), Pair(baseAsset=pair["c_base"], quoteAsset=pair["c_quote"])]

def find_all_triangular_pairs(pairs: list[Pair]) -> list[list[Pair]]:
        
    found_pairs: list[list[Pair]] = []
    for firstPair in pairs:
        for secondPair in pairs:
            if firstPair != secondPair and (firstPair.baseAsset == secondPair.baseAsset or firstPair.baseAsset == secondPair.quoteAsset or firstPair.quoteAsset == secondPair.baseAsset or firstPair.quoteAsset == secondPair.quoteAsset):
                for thirdPair in pairs:
                    if (thirdPair == firstPair or thirdPair == secondPair):
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
                        for already_found_pair in found_pairs:
                            if firstPair in already_found_pair and secondPair in already_found_pair and thirdPair in already_found_pair:
                                pair_found = False
                                break
                        if pair_found:
                            found_pairs.append([firstPair, secondPair, thirdPair])
    return found_pairs