
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