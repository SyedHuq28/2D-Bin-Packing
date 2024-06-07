
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)
    bins = []
    
    def fits_in_bin(item, bin_items, bin_width, bin_height):
        item_index, item_width, item_height = item

        for y in range(bin_height - item_height + 1):
            for x in range(bin_width - item_width + 1):
                if all(not (x_pos < x + item_width and x_pos + w > x and y_pos < y + item_height and y_pos + h > y)
                       for _, x_pos, y_pos, w, h in bin_items):
                    return x, y
        return None

    for item in items:
        item_index, item_width, item_height = item
        placed = False

        for bin_items in bins:
            position = fits_in_bin(item, bin_items, bin_width, bin_height)
            if position is not None:
                bin_items.append((item_index, position[0], position[1], item_width, item_height))
                placed = True
                break

        if not placed:
            new_bin = []
            position = fits_in_bin(item, new_bin, bin_width, bin_height)
            assert position is not None, "Item cannot fit in an empty bin, check item size relative to bin size."
            new_bin.append((item_index, position[0], position[1], item_width, item_height))
            bins.append(new_bin)

    result = []
    for bin_items in bins:
        result_bin = [(item_index, x, y) for item_index, x, y, w, h in bin_items]
        result.append(result_bin)
    
    return result