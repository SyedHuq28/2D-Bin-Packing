
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    items = [(i, width, height) for i, (width, height) in enumerate(demand)]
    
    # Sort items by the larger dimension (height) then by smaller dimension (width)
    items.sort(key=lambda x: (-max(x[1], x[2]), min(x[1], x[2])))

    # List to hold the bins
    bins = []

    def fits_in_bin(bin_items, item, bin_width, bin_height):
        def is_position_valid(occupied_positions, x, y, item_w, item_h):
            for ox, oy, ow, oh in occupied_positions:
                if not (x + item_w <= ox or x >= ox + ow or y + item_h <= oy or y >= oy + oh):
                    return False
            return True

        occupied_positions = []
        for i, (index, x, y, w, h) in enumerate(bin_items):
            occupied_positions.append((x, y, w, h))

        for x in range(bin_width - item[1] + 1):
            for y in range(bin_height - item[2] + 1):
                if is_position_valid(occupied_positions, x, y, item[1], item[2]):
                    return (x, y)
        return None
    
    for item in items:
        placed = False
        for bin_index, bin_items in enumerate(bins):
            position = fits_in_bin(bin_items, item, bin_width, bin_height)
            if position:
                x, y = position
                bin_items.append((item[0], x, y, item[1], item[2]))
                placed = True
                break
        
        if not placed:
            new_bin = [(item[0], 0, 0, item[1], item[2])]
            bins.append(new_bin)
    
    # Convert to required output format
    result = []
    for bin_items in bins:
        bin_result = [(index, x, y) for index, x, y, _, _ in bin_items]
        result.append(bin_result)

    return result

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple
import random
import numpy as np

import numpy as np
from typing import List, Tuple




def plot_rectangles(bin_number: int, bin: List[Tuple[int, int, int]], demand: np.ndarray, bin_capacities: Tuple[int, int]) -> float:
    fig, ax = plt.subplots(1, figsize=(8, 8))
    ax.set_title(f'Bin {bin_number} Contents')
    bin_width, bin_height = bin_capacities
    ax.set_xlim(0, bin_width)
    ax.set_ylim(0, bin_height)
    
    total_block_area = 0
    
    for item, x, y in bin:
        width, height = demand[item]
        rect_patch = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect_patch)
        ax.text(x + width / 2, y + height / 2, f'{width}x{height}', ha='center', va='center')
        total_block_area += width * height

    bin_area = bin_width * bin_height
    area_left = bin_area - total_block_area

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    return area_left




class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def __repr__(self):
        return f"Rectangle({self.width}, {self.height})"

def generate_rectangles(num_rectangles):
    rectangles = []
    for _ in range(num_rectangles):
        width = random.randint(1, 200)  # Adjust range as needed
        height = random.randint(1, 100)  # Adjust range as needed
        rectangles.append(Rectangle(width, height))
    return rectangles

def rectangles_to_array(rectangles):
    # Create an array where each row is [width, height] of a rectangle
    data = np.array([[rect.width, rect.height] for rect in rectangles])
    return data

# Example of generating and converting rectangles
rectangles = generate_rectangles(50)
rectangles_array = rectangles_to_array(rectangles)

# Print the resulting array
print(rectangles_array)

bin_capacities = (200, 100)

bins = heuristics_v1(rectangles_array, bin_capacities)

total_bins = len(bins)
total_area_left = 0

for bin_number, bin in enumerate(bins, start=1):
    area_left = plot_rectangles(bin_number, bin, rectangles_array, bin_capacities)
    total_area_left += area_left
    print(f'Bin {bin_number} has {area_left:.2f} units of area left')

print(f'Total number of bins = {total_bins}')
print(f'Total area left in bins = {total_area_left:.2f}')

result = {
    'total_bins': total_bins,
    'total_area_left': total_area_left
}