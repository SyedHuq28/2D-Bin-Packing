
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    import numpy as np

    bin_width, bin_height = capacities
    bins = []
    
    def fit_item(bin_slots, item_width, item_height):
        for y in range(bin_height - item_height + 1):
            for x in range(bin_width - item_width + 1):
                if bin_slots[y:y+item_height, x:x+item_width].sum() == 0:
                    return x, y
        return None

    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)
    
    for item in items:
        item_index, item_width, item_height = item
        placed = False

        for bin_representation in bins:
            bin_slots = bin_representation['slots']
            position = fit_item(bin_slots, item_width, item_height)
            if position is not None:
                x, y = position
                bin_representation['slots'][y:y+item_height, x:x+item_width] = 1
                bin_representation['items'].append((item_index, x, y))
                placed = True
                break

        if not placed:
            new_bin_slots = np.zeros((bin_height, bin_width), dtype=int)
            position = fit_item(new_bin_slots, item_width, item_height)
            if position is None:
                raise Exception("Item cannot be placed in an empty bin, check item size relative to bin size.")
            x, y = position
            new_bin_slots[y:y+item_height, x:x+item_width] = 1
            new_bin_representation = {
                'slots': new_bin_slots,
                'items': [(item_index, x, y)]
            }
            bins.append(new_bin_representation)
    
    return [bin_representation['items'] for bin_representation in bins]
