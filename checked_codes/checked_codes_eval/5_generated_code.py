
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = [(i, width, height) for i, (width, height) in enumerate(demand)]
    
    # Sort items by the larger dimension (height) then by smaller dimension (width)
    items.sort(key=lambda x: (-max(x[1], x[2]), min(x[1], x[2])))

    # List to hold the bins
    bins = []

    def fits_in_bin(bin_items, item, bin_width, bin_height):
        def is_position_valid(occupied_positions, x, y, item_w, item_h):
            for ox, oy, ow, oh in occupied_positions:
                if not (x + item_w <= ox or x >= ox + ow or y + item_h <= oy or y >= oy + oh):
                    return False
            return True

        occupied_positions = []
        for i, (index, x, y, w, h) in enumerate(bin_items):
            occupied_positions.append((x, y, w, h))

        for x in range(bin_width - item[1] + 1):
            for y in range(bin_height - item[2] + 1):
                if is_position_valid(occupied_positions, x, y, item[1], item[2]):
                    return (x, y)
        return None
    
    for item in items:
        placed = False
        for bin_index, bin_items in enumerate(bins):
            position = fits_in_bin(bin_items, item, bin_width, bin_height)
            if position:
                x, y = position
                bin_items.append((item[0], x, y, item[1], item[2]))
                placed = True
                break
        
        if not placed:
            new_bin = [(item[0], 0, 0, item[1], item[2])]
            bins.append(new_bin)
    
    # Convert to required output format
    result = []
    for bin_items in bins:
        bin_result = [(index, x, y) for index, x, y, _, _ in bin_items]
        result.append(bin_result)

    return result
