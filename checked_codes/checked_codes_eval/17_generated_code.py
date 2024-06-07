
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    n = demand.shape[0]

    items = [(i, demand[i][0], demand[i][1]) for i in range(n)]
    items.sort(key=lambda x: -max(x[1], x[2]))  # Sort items by the larger dimension

    bins = []

    def fits_in_bin(item, bin_items, bin_width, bin_height):
        item_width, item_height = item[1], item[2]
        x_positions = []
        y_positions = []

        for _, x, y in bin_items:
            if x + item_width <= bin_width and y + item_height <= bin_height:
                x_positions.append(x + item_width)
            if y + item_height <= bin_height and x + item_width <= bin_width:
                y_positions.append(y + item_height)

        start_x, start_y = 0, 0

        for pos in sorted(x_positions):
            start_x = pos
            if pos + item_width <= bin_width:
                break

        for pos in sorted(y_positions):
            start_y = pos
            if pos + item_height <= bin_height:
                break

        if start_x + item_width <= bin_width and start_y + item_height <= bin_height:
            return start_x, start_y

        return None

    for item in items:
        placed = False
        for bin in bins:
            position = fits_in_bin(item, bin, bin_width, bin_height)
            if position:
                x, y = position
                bin.append((item[0], x, y))
                placed = True
                break
        if not placed:
            bins.append([(item[0], 0, 0)])  # Create a new bin and place item at origin

    return bins
