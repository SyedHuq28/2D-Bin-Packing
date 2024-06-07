
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    import numpy as np

    bin_width, bin_height = capacities
    bins = []
    
    def fits_in_bin(item, bin_representation, bin_slots):
        item_width, item_height = item
        for y in range(bin_height - item_height + 1):
            for x in range(bin_width - item_width + 1):
                if bin_slots[y:y+item_height, x:x+item_width].sum() == 0:
                    return (x, y)
        return None
    
    sorted_indices = np.argsort(-demand[:, 1])  # Sort items by height in descending order
    for idx in sorted_indices:
        item_width, item_height = demand[idx]
        placed = False
        
        for bin_representation in bins:
            bin_slots = bin_representation['slots']
            position = fits_in_bin((item_width, item_height), bin_representation, bin_slots)
            if position is not None:
                x, y = position
                bin_representation['slots'][y:y+item_height, x:x+item_width] = 1
                bin_representation['items'].append((idx, x, y))
                placed = True
                break
        
        if not placed:
            bin_slots = np.zeros((bin_height, bin_width), dtype=int)
            bin_representation = {
                'slots': bin_slots,
                'items': []
            }
            position = fits_in_bin((item_width, item_height), bin_representation, bin_slots)
            if position is None:
                raise Exception("The item does not fit in a new bin, check bin size.")
            x, y = position
            bin_representation['slots'][y:y+item_height, x:x+item_width] = 1
            bin_representation['items'].append((idx, x, y))
            bins.append(bin_representation)
    
    return [bin_representation['items'] for bin_representation in bins]
