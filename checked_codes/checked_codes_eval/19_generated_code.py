
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    
    remaining_items = sorted([(i, width, height) for i, (width, height) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)

    def can_place_item(bin_items, item_width, item_height):
        positions = []
        for current_item in bin_items:
            i, cx, cy, cwidth, cheight = current_item
            positions.append((cx + cwidth, cy))
            positions.append((cx, cy + cheight))
        
        positions = sorted(positions, key=lambda x: (x[0], x[1]))  # prioritize bottom-left first

        for x, y in positions:
            if x + item_width <= bin_width and y + item_height <= bin_height:
                if all(not (x < cx + cwidth and x + item_width > cx and y < cy + cheight and y + item_height > cy) for _, cx, cy, cwidth, cheight in bin_items):
                    return x, y
        return None

    while remaining_items:
        current_bin = []
        to_remove = []

        for item in remaining_items:
            i, item_width, item_height = item
            if not current_bin:
                current_bin.append((i, 0, 0, item_width, item_height))
                to_remove.append(item)
            else:
                position = can_place_item(current_bin, item_width, item_height)
                if position:
                    x, y = position
                    current_bin.append((i, x, y, item_width, item_height))
                    to_remove.append(item)

        bins.append([(i, x, y) for i, x, y, _, _ in current_bin])
        for item in to_remove:
            remaining_items.remove(item)

    return bins
