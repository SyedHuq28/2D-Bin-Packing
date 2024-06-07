
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted(enumerate(demand), key=lambda x: max(x[1]), reverse=True)

    bins = []
    for item_index, (item_width, item_height) in items:
        placed = False
        for bin in bins:
            for y in range(bin_height):
                for x in range(bin_width):
                    if (x + item_width <= bin_width and 
                        y + item_height <= bin_height and 
                        not any(item[1] < x + item_width and item[1] + demand[item[0], 0] > x and 
                                item[2] < y + item_height and item[2] + demand[item[0], 1] > y for item in bin)):
                        bin.append((item_index, x, y))
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
        if not placed:
            new_bin = [(item_index, 0, 0)]
            bins.append(new_bin)
    
    return bins
