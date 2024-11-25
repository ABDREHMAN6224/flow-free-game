import time
import numpy as np
import matplotlib.pyplot as plt
from a import solve_flow_with_paths, findPaths
from mss import mss
import cv2
import pyautogui as auto
auto.FAILSAFE = True
# from test import image2grid

# Set up MSS for screen capture
sct = mss()

N = 10

# Define the region to capture (adjust to target a specific window or area)
region = {
    "top": 370,  # y-coordinate of the top edge
    "left": 1476,  # x-coordinate of the left edge
    "width": 1900 - 1476,  # width of the region
    "height": 797 - 370,  # height of the region
}

cell_height = region['height'] // N
cell_width = region['width'] // N

def rc2xy(row, col):
    return (col + 0.5) * cell_width + region['left'], (row + 0.5) * cell_height + region['top']

def applyPath(path):
    print(path)
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        start_x, start_y = start
        end_x, end_y = end
        start_x, start_y = rc2xy(start_x, start_y)
        end_x, end_y = rc2xy(end_x, end_y)
        if i == 0:
            auto.moveTo(start_x, start_y)
        auto.dragTo(end_x, end_y, duration=0.1)
        time.sleep(0.1)

# Initialize Matplotlib figure
# plt.ion()  # Interactive mode on
# fig, ax = plt.subplots()
# image = ax.imshow(np.zeros((region['height'], region['width'], 3), dtype=np.uint8))
window = cv2.namedWindow("window", cv2.WINDOW_NORMAL)

colors = {
    'pink': (255, 10, 202),
    'yellow': (233, 224, 0),
    'cyan': (0, 254, 255),
    'green': (0, 141, 0),
    'orange': (252, 137, 1),
    'red': (254, 0, 0),
    'purple': (127, 0, 127),
    'blue': (12, 41, 255),
    'mehroon': (165, 42, 43),
}

def image2grid(arr):
    grid = []
    rows, cols, _ = arr.shape
    cell_height = rows // N
    cell_width = cols // N
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    index = 0
    pairs = {}
    colors = {}
    for i in range(N):
        row = []
        for j in range(N):
            d = min(cell_height, cell_width) // 6
            cx, cy = j * cell_width + cell_width // 2, i * cell_height + cell_height // 2
            pixel = tuple(arr[cy][cx][:3][::-1].tolist())
            
            # if i == 3 and j == 1:
            #     print(pixel)
            if pixel in colors.values():
                for key, value in colors.items():
                    if pixel == value:
                        row.append(key)
                        print(i, j, key)
                        if key not in pairs:
                            pairs[key] = []
                        pairs[key].append((i, j))
                        break
            elif np.sum(pixel) > 100:
                colors[alphabet[index]] = pixel
                row.append(alphabet[index])
                print(i, j, alphabet[index])
                if alphabet[index] not in pairs:
                    pairs[alphabet[index]] = []
                pairs[alphabet[index]].append((i, j))
                index += 1
            else:
                row.append(' ')
        grid.append(row)

    for row in grid:
        for cell in row:
            print(cell[0], end=' ')
        print()
        
    return pairs, grid


try:
    while True:
        screenshot = sct.grab(region)
        frame = np.array(screenshot)
        cv2.imshow("window", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            pairs, grid = image2grid(frame)
            print(pairs)
            print(grid)
            i = 0
            keys = list(pairs.keys())
            grid = [[0] * N for _ in range(N)]
            color_map = {color: idx + 1 for idx, color in enumerate(pairs.keys())}
            for color, positions in pairs.items():
                for x, y in positions:
                    grid[x][y] = color_map[color]            
            solved_grid = solve_flow_with_paths(grid, 10, pairs, color_map)
            paths = findPaths(solved_grid, pairs, color_map)
            print(paths)
            for path in paths:
                time.sleep(0.1)
                applyPath(paths[path])

        if key == ord('q'):
            break
except KeyboardInterrupt:
    print(frame)
    print("Exited.")
finally:
    plt.ioff()  # Turn off interactive mode
    plt.show()
