
def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    from typing import List, Tuple
    import numpy as np
    
    bin_width, bin_height = capacities
    items = sorted([(i, w, h) for i, (w, h) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)
    bins = []
    
    class Bin:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.items = []
            self.slots = np.zeros((height, width), dtype=int)
        
        def fits(self, item_width, item_height):
            for y in range(self.height - item_height + 1):
                for x in range(self.width - item_width + 1):
                    if self.slots[y:y+item_height, x:x+item_width].sum() == 0:
                        return (x, y)
            return None
        
        def place(self, item_index, item_width, item_height, x, y):
            self.slots[y:y+item_height, x:x+item_width] = 1
            self.items.append((item_index, x, y))
    
    for item_index, item_width, item_height in items:
        placed = False
        for bin in bins:
            position = bin.fits(item_width, item_height)
            if position is not None:
                x, y = position
                bin.place(item_index, item_width, item_height, x, y)
                placed = True
                break
        
        if not placed:
            new_bin = Bin(bin_width, bin_height)
            position = new_bin.fits(item_width, item_height)
            assert position is not None, "Item cannot fit in an empty bin, check item size relative to bin size."
            x, y = position
            new_bin.place(item_index, item_width, item_height, x, y)
            bins.append(new_bin)
    
    result = [bin.items for bin in bins]
    return result
