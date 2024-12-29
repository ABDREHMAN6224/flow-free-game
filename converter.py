import time
import numpy as np
import matplotlib.pyplot as plt
from a import solve_flow_with_paths, findPaths
# from mss import mss
# import cv2
# import pyautogui as auto
# auto.FAILSAFE = True
from ppadb.client import Client
# from test import image2grid

# Set up MSS for screen capture
# sct = mss()
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('No device attached')
    quit()
    
device = devices[0]

image = device.screencap()
with open('screen.png', 'wb') as f:
    f.write(image)
    

# show the image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('screen.png')
img_array = np.array(img)
imgplot = plt.imshow(img)
plt.show()
N = 10

w = 1080 - 2
h = 2400
cell_width = w // N
cell_height = w // N
left = 0
top = (h // 2) - (w // 2) - 12

cropped = img_array[top:top + w, left:left + w]

imgplot = plt.imshow(cropped)
plt.show()
# print(img_array.shape)
cropped = cropped * 255
print(cropped)


# # device.shell('input touchscreen swipe 500 1000 500 500 200')
# quit()
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
    
    if (np.subtract(straight_path[-1], straight_path[-2]) ** 2).sum() == 1:
        straight_path.pop()
    
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
    path = convert_to_straight_lines(path)
    print("Path: ", path)
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
# window = cv2.namedWindow("window", cv2.WINDOW_NORMAL)

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


# try:
#     while True:
#         screenshot = sct.grab(region)
#         frame = np.array(screenshot)
#         cv2.imshow("window", frame)
#         key = cv2.waitKey(1)
#         if key == ord('s'):
#             pairs, grid = image2grid(frame)
#             print(pairs)
#             print(grid)
#             i = 0
#             keys = list(pairs.keys())
#             grid = [[0] * N for _ in range(N)]
#             color_map = {color: idx + 1 for idx, color in enumerate(pairs.keys())}
#             for color, positions in pairs.items():
#                 for x, y in positions:
#                     grid[x][y] = color_map[color]            
#             solved_grid = solve_flow_with_paths(grid, 10, pairs, color_map)
#             paths = findPaths(solved_grid, pairs, color_map)
#             print(paths)
#             for path in paths:
#                 time.sleep(0.1)
#                 applyPath(paths[path])

#         if key == ord('q'):
#             break
# except KeyboardInterrupt:
#     print(frame)
#     print("Exited.")
# finally:
#     plt.ioff()  # Turn off interactive mode
#     plt.show()


pairs, grid = image2grid(cropped)
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
    # time.sleep(0.1)
    applyPath(paths[path])