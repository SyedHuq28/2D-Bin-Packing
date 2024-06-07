
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted(enumerate(demand), key=lambda x: -max(x[1]))  # Sort items by the largest dimension in descending order
    bins = []
    
    for item_index, (item_width, item_height) in items:
        placed = False
        for bin in bins:
            if try_place_item(bin, item_index, item_width, item_height, bin_width, bin_height):
                placed = True
                break
        if not placed:
            new_bin = []
            if try_place_item(new_bin, item_index, item_width, item_height, bin_width, bin_height):
                bins.append(new_bin)
                
    return bins

def try_place_item(bin: List[Tuple[int,int,int]], item_index: int, item_width: int, item_height: int,
                   bin_width: int, bin_height: int) -> bool:
    if not bin:  # If the bin is empty, place the item at the origin.
        bin.append((item_index, 0, 0))
        return True
    
    possible_positions = []
    for _, x, y in bin:
        possible_positions.append((x + item_width, y))
        possible_positions.append((x, y + item_height))
        
    possible_positions = list(set(possible_positions))  # Remove duplicates
    
    for (x_position, y_position) in possible_positions:
        if (x_position + item_width <= bin_width) and (y_position + item_height <= bin_height):
            overlap = False
            for _, x, y in bin:
                if not (x_position + item_width <= x or x_position >= x + item_width or 
                        y_position + item_height <= y or y_position >= y + item_height):
                    overlap = True
                    break
            if not overlap:
                bin.append((item_index, x_position, y_position))
                return True
    return False
