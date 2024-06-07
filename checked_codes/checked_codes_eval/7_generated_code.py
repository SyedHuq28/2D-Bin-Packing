
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    
    # Sort items by height first, then by width as a tie breaker (descending order)
    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: (-x[2], -x[1]))
    
    def can_place_item(current_bin, x, y, item_width, item_height):
        if x + item_width > bin_width or y + item_height > bin_height:
            return False
        for _, bx, by, b_width, b_height in current_bin:
            if not (x + item_width <= bx or x >= bx + b_width or y + item_height <= by or y >= by + b_height):
                return False
        return True

    for item_index, item_width, item_height in items:
        placed = False
        for current_bin in bins:
            for x in range(bin_width):
                for y in range(bin_height):
                    if can_place_item(current_bin, x, y, item_width, item_height):
                        current_bin.append((item_index, x, y, item_width, item_height))
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
        if not placed:
            new_bin = [(item_index, 0, 0, item_width, item_height)]
            bins.append(new_bin)
    
    # Convert to desired output format
    output_bins = []
    for b in bins:
        output_bins.append([(i, x, y) for i, x, y, w, h in b])
    
    return output_bins
