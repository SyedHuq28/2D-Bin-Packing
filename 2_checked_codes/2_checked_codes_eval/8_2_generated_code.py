

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []

    def fit_item_in_bin(item, bin_slots):
        item_width, item_height = item
        for y in range(bin_height - item_height + 1):
            for x in range(bin_width - item_width + 1):
                if np.all(bin_slots[y:y + item_height, x:x + item_width] == 0):
                    return (x, y)
        return None

    # Sort items by the larger dimension in descending order, to try fitting larger items first
    sorted_items = sorted(enumerate(demand), key=lambda iwh: max(iwh[1][0], iwh[1][1]), reverse=True)

    for item_index, (item_width, item_height) in sorted_items:
        placed = False

        for bin_representation in bins:
            bin_slots = bin_representation['slots']
            position = fit_item_in_bin((item_width, item_height), bin_slots)
            if position is not None:
                x, y = position
                bin_slots[y:y+item_height, x:x+item_width] = 1
                bin_representation['items'].append((item_index, x, y))
                placed = True
                break

        if not placed:
            # Create a new bin
            bin_slots = np.zeros((bin_height, bin_width), dtype=int)
            position = fit_item_in_bin((item_width, item_height), bin_slots)
            assert position is not None, "Item cannot fit in an empty bin. Check item and bin sizes."
            x, y = position
            bin_slots[y:y + item_height, x:x + item_width] = 1
            bins.append({
                'slots': bin_slots,
                'items': [(item_index, x, y)]
            })

    return [bin_representation['items'] for bin_representation in bins]

