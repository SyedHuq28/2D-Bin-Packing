
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    n = demand.shape[0]
    
    # Sorting items by height (descending order) can help packing strategy
    items_with_index = sorted([(i, demand[i][0], demand[i][1]) for i in range(n)], key=lambda x: x[2], reverse=True)
    
    bins = []
    
    for item_index, item_width, item_height in items_with_index:
        placed = False
        for current_bin in bins:
            max_height = max([item[2] + demand[item[0]][1] for item in current_bin], default=0)

            if max_height + item_height <= bin_height:
                x_position = 0
                for existing_item in current_bin:
                    item_existing_width = demand[existing_item[0]][0]
                    item_existing_height = demand[existing_item[0]][1]
                    x_position = max(x_position, existing_item[1] + item_existing_width)
                    
                    if x_position + item_width <= bin_width:
                        current_bin.append((item_index, x_position, max_height))
                        placed = True
                        break

                if placed:
                    break
        
        if not placed:
            bins.append([(item_index, 0, 0)])
    
    return bins
