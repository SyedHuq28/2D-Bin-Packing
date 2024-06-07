
import numpy as np
from typing import List, Tuple

def heuristics_v1(demand: np.ndarray, capacities: Tuple[int, int]) -> List[List[Tuple[int, int, int]]]:
    bin_width, bin_height = capacities
    bins = []
    
    remaining_items = sorted([(i, width, height) for i, (width, height) in enumerate(demand)], key=lambda x: max(x[1], x[2]), reverse=True)

    def can_place_item(bin_items, item_width, item_height):
        positions = []
        for current_item in bin_items:
            i, cx, cy, cwidth, cheight = current_item
            positions.append((cx + cwidth, cy))
            positions.append((cx, cy + cheight))
        
        positions = sorted(positions, key=lambda x: (x[0], x[1]))  # prioritize bottom-left first

        for x, y in positions:
            if x + item_width <= bin_width and y + item_height <= bin_height:
                if all(not (x < cx + cwidth and x + item_width > cx and y < cy + cheight and y + item_height > cy) for _, cx, cy, cwidth, cheight in bin_items):
                    return x, y
        return None

    while remaining_items:
        current_bin = []
        to_remove = []

        for item in remaining_items:
            i, item_width, item_height = item
            if not current_bin:
                current_bin.append((i, 0, 0, item_width, item_height))
                to_remove.append(item)
            else:
                position = can_place_item(current_bin, item_width, item_height)
                if position:
                    x, y = position
                    current_bin.append((i, x, y, item_width, item_height))
                    to_remove.append(item)

        bins.append([(i, x, y) for i, x, y, _, _ in current_bin])
        for item in to_remove:
            remaining_items.remove(item)

    return bins

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