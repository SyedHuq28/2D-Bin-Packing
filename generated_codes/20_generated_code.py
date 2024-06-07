
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    current_bin = []
    current_x, current_y = 0, 0
    max_row_height = 0
    
    for i, (item_width, item_height) in enumerate(demand):
        # If adding this item exceeds the bin's width, move to the next row
        if current_x + item_width > bin_width:
            current_x = 0
            current_y += max_row_height
            max_row_height = 0
        
        # If adding this item exceeds the bin's height, move to a new bin
        if current_y + item_height > bin_height:
            bins.append(current_bin)
            current_bin = []
            current_x, current_y = 0, 0
            max_row_height = 0
        
        # Place the item in the current bin
        current_bin.append((i, current_x, current_y))
        current_x += item_width
        max_row_height = max(max_row_height, item_height)
    
    # Don't forget to add the last bin
    if current_bin:
        bins.append(current_bin)
    
    return bins
