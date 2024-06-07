
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted([(i, width, height) for i, (width, height) in enumerate(demand)], key=lambda x: (-max(x[1], x[2]), min(x[1], x[2])))
    bins = []

    for item_index, item_width, item_height in items:
        placed = False
        
        for bin in bins:
            for x in range(bin_width - item_width + 1):
                for y in range(bin_height - item_height + 1):
                    overlap = False

                    for _, bx, by, bwidth, bheight in bin:
                        if not (x + item_width <= bx or x >= bx + bwidth or y + item_height <= by or y >= by + bheight):
                            overlap = True
                            break
                    
                    if not overlap:
                        bin.append((item_index, x, y, item_width, item_height))
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
                
        if not placed:
            bins.append([(item_index, 0, 0, item_width, item_height)])
            
    result = []
    for bin in bins:
        single_bin = [(i, x, y) for i, x, y, w, h in bin]
        result.append(single_bin)
    
    return result
