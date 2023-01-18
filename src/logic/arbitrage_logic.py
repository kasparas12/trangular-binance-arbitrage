from models.pair import Pair

def find_all_triangular_pairs(pairs: list[Pair]) -> list[list[Pair]]:
    print('Finding triangualr pairs...')
    
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
