
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    import numpy as np
    
    bin_width, bin_height = capacities
    n = demand.shape[0]
    item_indices = np.argsort(demand[:,1])[::-1]  # Sort items by height in descending order
    bins = []
    
    current_bin = []
    current_width = 0
    current_height = 0
    max_row_height = 0

    for i in item_indices:
        item_width, item_height = demand[i]
        
        if current_width + item_width <= bin_width and current_height + item_height <= bin_height:
            # Place item in current row if it fits horizontally
            current_bin.append((i, current_width, current_height))
            current_width += item_width
            max_row_height = max(max_row_height, item_height)
        elif current_height + max_row_height + item_height <= bin_height and item_width <= bin_width:
            # Move to next row if it fits vertically
            current_height += max_row_height
            current_width = 0
            max_row_height = item_height
            current_bin.append((i, current_width, current_height))
            current_width += item_width
        else:
            # If it doesn't fit, open a new bin
            bins.append(current_bin)
            current_bin = [(i, 0, 0)]
            current_width = item_width
            current_height = 0
            max_row_height = item_height
    
    if current_bin:
        bins.append(current_bin)

    return bins
