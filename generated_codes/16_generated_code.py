
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    current_bin = []
    current_x = 0
    current_y = 0
    max_height_in_row = 0

    for i, (item_width, item_height) in enumerate(demand):
        if item_width > bin_width or item_height > bin_height:
            print(f"Item {i} with dimensions {(item_width, item_height)} cannot fit in the bin at all.")
            continue

        if current_x + item_width > bin_width:
            current_x = 0
            current_y += max_height_in_row
            max_height_in_row = 0

        if current_y + item_height > bin_height:
            bins.append(current_bin)
            current_bin = []
            current_x = 0
            current_y = 0
            max_height_in_row = 0

        current_bin.append((i, current_x, current_y))
        current_x += item_width
        max_height_in_row = max(max_height_in_row, item_height)

    if current_bin:
        bins.append(current_bin)

    return bins
