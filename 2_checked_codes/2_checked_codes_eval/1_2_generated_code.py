
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: (max(x[1], x[2]), x[1] * x[2]), reverse=True)
    bins = []

    def fits_in_bin(x, y, item_width, item_height, bin_slots):
        if x + item_width > bin_width or y + item_height > bin_height:
            return False
        if np.any(bin_slots[y:y+item_height, x:x+item_width]):
            return False
        return True

    for item in items:
        item_index, item_width, item_height = item
        placed = False
        
        for bin_representation in bins:
            bin_slots = bin_representation['slots']
            for y in range(bin_height - item_height + 1):
                for x in range(bin_width - item_width + 1):
                    if fits_in_bin(x, y, item_width, item_height, bin_slots):
                        bin_slots[y:y+item_height, x:x+item_width] = 1
                        bin_representation['items'].append((item_index, x, y))
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
        
        if not placed:
            bin_slots = np.zeros((bin_height, bin_width), dtype=int)
            position_found = False
            for y in range(bin_height - item_height + 1):
                for x in range(bin_width - item_width + 1):
                    if fits_in_bin(x, y, item_width, item_height, bin_slots):
                        bin_slots[y:y+item_height, x:x+item_width] = 1
                        position = (x, y)
                        position_found = True
                        break
                if position_found:
                    break
            if not position_found:
                raise Exception("Item does not fit in a new bin.")
            new_bin = {
                'slots': bin_slots,
                'items': [(item_index, position[0], position[1])]
            }
            bins.append(new_bin)

    result = [bin_representation['items'] for bin_representation in bins]
    
    return result
