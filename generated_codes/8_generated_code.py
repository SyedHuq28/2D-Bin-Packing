
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted(enumerate(demand), key=lambda x: max(x[1]), reverse=True)
    
    bins = []
    
    def fits_in_bin(item_w, item_h, bin_layout):
        for x in range(bin_width - item_w + 1):
            for y in range(bin_height - item_h + 1):
                if all(item_w + i <= bin_width and item_h + j <= bin_height and
                       all((x+i, y+j) not in bin_layout for i in range(item_w) for j in range(item_h))):
                    return True, x, y
        return False, -1, -1
    
    for item_index, (item_w, item_h) in items:
        placed = False
        for bin in bins:
            bin_layout = {(x, y) for _, x, y in bin}
            fits, x, y = fits_in_bin(item_w, item_h, bin_layout)
            if fits:
                bin.append((item_index, x, y))
                placed = True
                break
        if not placed:
            new_bin_layout = [(item_index, 0, 0)]
            bins.append(new_bin_layout)
    
    return bins
