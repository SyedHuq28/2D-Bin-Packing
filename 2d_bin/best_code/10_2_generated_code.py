
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

    def fit_item(bin_items, item, bin_width, bin_height):
        item_index, item_width, item_height = item

        for bx in range(bin_width - item_width + 1):
            for by in range(bin_height - item_height + 1):
                if all(not (x < bx + item_width and x + w > bx and y < by + item_height and y + h > by)
                       for _, x, y, w, h in bin_items):
                    return bx, by
        return None

    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)

    for item in items:
        item_index, item_width, item_height = item[0], item[1], item[2]
        placed = False

        for bin_representation in bins:
            bin_slots = bin_representation['slots']
            position = fits_in_bin((item_width, item_height), bin_representation, bin_slots)
            if position is not None:
                x, y = position
                bin_representation['slots'][y:y+item_height, x:x+item_width] = 1
                bin_representation['items'].append((item_index, x, y))
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
            bin_representation['items'].append((item_index, x, y))
            bins.append(bin_representation)
    
    return [bin_representation['items'] for bin_representation in bins]