
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted(((index, w, h) for index, (w, h) in enumerate(demand)), key=lambda x: max(x[1], x[2]), reverse=True)
    bins = []
    
    for index, width, height in items:
        placed = False
        for b in bins:
            if try_place_item(b, index, width, height, bin_width, bin_height):
                placed = True
                break
        if not placed:
            new_bin = []
            place_in_new_bin(new_bin, index, width, height, bin_width, bin_height)
            bins.append(new_bin)
            
    return bins

def try_place_item(bin, index, width, height, bin_width, bin_height):
    for x in range(bin_width - width + 1):
        for y in range(bin_height - height + 1):
            if not overlaps(bin, x, y, width, height):
                bin.append((index, x, y))
                return True
    return False

def place_in_new_bin(bin, index, width, height, bin_width, bin_height):
    bin.append((index, 0, 0))

def overlaps(bin, x, y, width, height):
    for _, bx, by in bin:
        if not (x + width <= bx or bx + bin[0][1] <= x or y + height <= by or by + bin[0][2] <= y):
            return True
    return False
