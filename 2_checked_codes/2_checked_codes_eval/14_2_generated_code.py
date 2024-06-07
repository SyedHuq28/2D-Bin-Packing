
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)
    bins = []
    
    def fit_item(bin_items, bin_slots, item, bin_width, bin_height):
        item_index, item_width, item_height = item
        for y in range(bin_height - item_height + 1):
            for x in range(bin_width - item_width + 1):
                if bin_slots[y:y+item_height, x:x+item_width].sum() == 0:
                    return (x, y)
        return None
    
    for item in items:
        item_index, item_width, item_height = item
        placed = False

        for bin_representation in bins:
            bin_slots = bin_representation['slots']
            position = fit_item(bin_representation['items'], bin_slots, item, bin_width, bin_height)
            if position is not None:
                x, y = position
                bin_slots[y:y+item_height, x:x+item_width] = 1
                bin_representation['items'].append((item_index, x, y, item_width, item_height))
                placed = True
                break

        if not placed:
            bin_slots = np.zeros((bin_height, bin_width), dtype=int)
            bin_representation = {
                'slots': bin_slots,
                'items': []
            }
            position = fit_item([], bin_slots, item, bin_width, bin_height)
            if position is None:
                raise Exception("Item cannot fit in an empty bin, check item size relative to bin size.")
            x, y = position
            bin_slots[y:y+item_height, x:x+item_width] = 1
            bin_representation['items'].append((item_index, x, y, item_width, item_height))
            bins.append(bin_representation)
    
    result = []
    for bin_representation in bins:
        result_bin = [(item[0], item[1], item[2]) for item in bin_representation['items']]
        result.append(result_bin)
    
    return result
