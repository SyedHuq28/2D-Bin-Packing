
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    
    sorted_indices = np.argsort(-demand[:, 1])  # sort items by height in descending order
    
    current_bin = []
    current_x = 0
    current_y = 0
    max_height_in_row = 0
    
    for i in sorted_indices:
        item_width, item_height = demand[i]
        
        if current_x + item_width > bin_width:  # if item doesn't fit horizontally, move to a new row
            current_x = 0
            current_y += max_height_in_row
            max_height_in_row = 0
        
        if current_y + item_height > bin_height:  # if item doesn't fit vertically, create a new bin
            bins.append(current_bin)
            current_bin = []
            current_x = 0
            current_y = 0
        
        current_bin.append((i, current_x, current_y))
        current_x += item_width
        max_height_in_row = max(max_height_in_row, item_height)
    
    if current_bin:  # append the last bin if not empty
        bins.append(current_bin)
    
    return bins
