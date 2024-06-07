
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted(enumerate(demand), key=lambda x: max(x[1]), reverse=True)
    
    bins = []
    current_bin = []
    current_x = 0
    current_y = 0
    max_row_height = 0
    
    for idx, (width, height) in items:
        if current_x + width > bin_width:
            current_x = 0
            current_y += max_row_height
            max_row_height = 0
        
        if current_y + height > bin_height:
            bins.append(current_bin)
            current_bin = []
            current_x = 0
            current_y = 0
            max_row_height = 0
        
        current_bin.append((idx, current_x, current_y))
        current_x += width
        max_row_height = max(max_row_height, height)
        
    if current_bin:
        bins.append(current_bin)
    
    return bins
