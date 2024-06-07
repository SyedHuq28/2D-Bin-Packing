
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    import numpy as np

    bin_width, bin_height = capacities
    bins = []

    def fit_item_in_bin(item, bin_representation):
        item_width, item_height = item
        for y in range(bin_height - item_height + 1):
            for x in range(bin_width - item_width + 1):
                if np.all(bin_representation[y:y + item_height, x:x + item_width] == 0):
                    return x, y
        return None

    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: x[2], reverse=True)

    for item_index, item_width, item_height in items:
        placed = False
        for bin_representation in bins:
            position = fit_item_in_bin((item_width, item_height), bin_representation['slots'])
            if position is not None:
                x, y = position
                bin_representation['slots'][y:y + item_height, x:x + item_width] = 1
                bin_representation['items'].append((item_index, x, y))
                placed = True
                break

        if not placed:
            bin_slots = np.zeros((bin_height, bin_width), dtype=int)
            position = fit_item_in_bin((item_width, item_height), bin_slots)
            if position is None:
                raise Exception("The item does not fit in a new bin, check bin size.")
            x, y = position
            bin_slots[y:y + item_height, x:x + item_width] = 1
            bins.append({'slots': bin_slots, 'items': [(item_index, x, y)]})

    result = [bin_representation['items'] for bin_representation in bins]
    return result
