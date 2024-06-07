
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    current_bin = []
    x_cursor, y_cursor, max_height_in_row = 0, 0, 0
    
    for i, (item_width, item_height) in enumerate(demand):
        if x_cursor + item_width > bin_width:
            x_cursor = 0
            y_cursor += max_height_in_row
            max_height_in_row = 0
        
        if y_cursor + item_height > bin_height:
            bins.append(current_bin)
            current_bin = []
            x_cursor, y_cursor, max_height_in_row = 0, 0, 0
        
        current_bin.append((i, x_cursor, y_cursor))
        x_cursor += item_width
        max_height_in_row = max(max_height_in_row, item_height)
    
    if current_bin:
        bins.append(current_bin)
    
    return bins
