import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple
import random
import numpy as np

import numpy as np
from typing import List, Tuple
import time




def plot_rectangles(bin_number: int, bin: List[Tuple[int, int, int]], demand: np.ndarray, bin_capacities: Tuple[int, int]) -> Tuple[float, float]:
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
    utilization = (total_block_area / bin_area) * 100

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    return area_left, utilization


bin_capacities = (200, 100)

start_time = time.time()
bins = heuristics_v1(rectangles_array, bin_capacities)  # Assuming heuristics_v1 is already defined
end_time = time.time()
time1 = end_time - start_time

total_bins = len(bins)
total_area_left = 0
utilizations = []

for bin_number, bin in enumerate(bins, start=1):
    area_left, utilization = plot_rectangles(bin_number, bin, rectangles_array, bin_capacities)
    total_area_left += area_left
    utilizations.append(utilization)
    print(f'Bin {bin_number} has {area_left:.2f} units of area left, utilization: {utilization:.2f}%')

print(f'Total number of bins = {total_bins}')
print(f'Total area left in bins = {total_area_left:.2f}')

result = {
    'total_bins': total_bins,
    'total_area_left': total_area_left,
    'utilizations': utilizations
}

# Print the resulting dictionary
print(result)