
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    
    def can_fit(item, bin_items, bin_width, bin_height):
        item_width, item_height = item
        positions = []
        
        for placed_item in bin_items:
            p_index, p_x, p_y, p_w, p_h = placed_item
            
            # Check all positions around the placed item
            test_positions = [
                (p_x + p_w, p_y),
                (p_x, p_y + p_h),
                (0, p_y + p_h),
                (p_x + p_w, 0)
            ]
            
            for tx, ty in test_positions:
                if all(
                    tx + item_width <= bin_width and 
                    ty + item_height <= bin_height and 
                    not any(
                        tx < px + pw and tx + item_width > px and 
                        ty < py + ph and ty + item_height > py 
                        for _, px, py, pw, ph in bin_items
                    )
                ):
                    positions.append((tx, ty))
        
        if not positions:  
            # If there are no valid positions around already placed items, try the base positions
            base_positions = [
                (0, 0)
            ]
            for bx, by in base_positions:
                if all(
                    bx + item_width <= bin_width and 
                    by + item_height <= bin_height and 
                    not any(
                        bx < px + pw and bx + item_width > px and 
                        by < py + ph and by + item_height > py 
                        for _, px, py, pw, ph in bin_items
                    )
                ):
                    positions.append((bx, by))

        return positions[0] if positions else None
    
    for i, (item_width, item_height) in enumerate(demand):
        placed = False
        for bin_items in bins:
            position = can_fit((item_width, item_height), bin_items, bin_width, bin_height)
            if position:
                bin_items.append((i, position[0], position[1], item_width, item_height))
                placed = True
                break
        if not placed:
            # Create a new bin if the item doesn't fit in any existing bin
            new_bin = [(i, 0, 0, item_width, item_height)]
            bins.append(new_bin)
    
    # Format the output as required
    formatted_bins = []
    for bin_items in bins:
        formatted_bin = [(item_index, x, y) for item_index, x, y, _, _ in bin_items]
        formatted_bins.append(formatted_bin)

    return formatted_bins
