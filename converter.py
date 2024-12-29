import time
import numpy as np
import matplotlib.pyplot as plt
from a import solve_flow_with_paths, findPaths
from mss import mss
import cv2
import pyautogui as auto
auto.FAILSAFE = True
from ppadb.client import Client
# from test import image2grid

# Set up MSS for screen capture
sct = mss()
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('No device attached')
    quit()
    
device = devices[0]

# device.shell('input touchscreen swipe 500 1000 500 500 200')
# quit()

N = 10

# Define the region to capture (adjust to target a specific window or area)
region = {
    "top": 355,  # y-coordinate of the top edge
    "left": 839,  # x-coordinate of the left edge
    "width": 425,  # width of the region
    "height": 425,  # height of the region
}

cell_height = region['height'] // N
cell_width = region['width'] // N

def convert_to_straight_lines(path):
    if not path:
        return []
    
    # Start with the first point
    straight_path = [path[0]]
    
    # Traverse the path
    for i in range(1, len(path) - 1):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]
        x3, y3 = path[i + 1]
        
        # Check if current point lies on a straight line with the previous and next points
        if (x1 == x2 == x3) or (y1 == y2 == y3):
            # Continue the line, no need to add the middle point
            continue
        else:
            # Add the point as a turning point
            straight_path.append((x2, y2))
    
    # Always add the last point
    straight_path.append(path[-1])
    
    return straight_path

def rc2xy(row, col):
    w = 1080 - 2
    h = 2400
    cell_width = w // N
    cell_height = w // N
    left = 2
    top = (h // 2) - (w // 2)
    return (col + 0.5) * cell_width + left, (row + 0.5) * cell_height + top

def applyPath(path):
    print(path)
    path = convert_to_straight_lines(path)
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        start_x, start_y = start
        end_x, end_y = end
        start_x, start_y = rc2xy(start_x, start_y)
        end_x, end_y = rc2xy(end_x, end_y)
        # if i == 0:
        #     auto.moveTo(start_x, start_y)
        # auto.dragTo(end_x, end_y, duration=0.1)
        # time.sleep(0.1)
        # if i == 0:
        #     # auto.moveTo(start_x, start_y)
        #     device.shell(f'input touchscreen swipe {start_x} {start_y} {end_x} {end_y} 50')
        # auto.dragTo(end_x, end_y, duration=0.1)
        device.shell(f'input touchscreen swipe {start_x} {start_y} {end_x} {end_y} 10')
        # time.sleep(0.1)

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
    'white': (255, 255, 255),
}

def image2grid(arr,color_map=colors, N=10):
    grid = []
    rows, cols, _ = arr.shape
    cell_height = rows // N
    cell_width = cols // N
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    index = 0
    pairs = {}
    detected_colors = {}

    def closest_color(pixel, color_map):
        min_dist = float('inf')
        best_match = None
        for key, color in color_map.items():
            dist = np.linalg.norm(np.array(pixel) - np.array(color))
            if dist < min_dist:
                min_dist = dist
                best_match = key
        return best_match if min_dist < 50 else None  # Adjust threshold as needed

    for i in range(N):
        row = []
        for j in range(N):
            cx, cy = j * cell_width + cell_width // 2, i * cell_height + cell_height // 2
            pixel = tuple(arr[cy, cx][:3][::-1].tolist())  # BGR to RGB
            
            matched_color = closest_color(pixel, color_map)
            if matched_color:
                row.append(matched_color)
                if matched_color not in pairs:
                    pairs[matched_color] = []
                pairs[matched_color].append((i, j))
            else:
                row.append(' ')
        grid.append(row)

    # Debugging: Print the grid
    print("Generated Grid:")
    for row in grid:
        print(' '.join(row))
    
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
