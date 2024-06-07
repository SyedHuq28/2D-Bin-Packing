

import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted(enumerate(demand), key=lambda x: max(x[1]), reverse=True) # Sort by largest dimension first
    bins = []

    for item_index, (item_width, item_height) in items:
        placed = False

        for bin in bins:
            for y in range(bin_height - item_height + 1):
                for x in range(bin_width - item_width + 1):
                    # Check for overlap
                    if all(not (x < px + pw and x + item_width > px and y < py + ph and y + item_height > py)
                           for _, px, py, pw, ph in bin):
                        bin.append((item_index, x, y, item_width, item_height))
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break

        if not placed:
            bins.append([(item_index, 0, 0, item_width, item_height)])
    
    result_bins = [[(item_index, x, y) for item_index, x, y, _, _ in bin] for bin in bins]
    return result_bins
