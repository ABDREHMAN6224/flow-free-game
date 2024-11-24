import time
import numpy as np
import matplotlib.pyplot as plt
from mss import mss
import cv2
# from test import image2grid

# Set up MSS for screen capture
sct = mss()

N = 10

# Define the region to capture (adjust to target a specific window or area)
region = {
    "top": 345,  # y-coordinate of the top edge
    "left": 768,  # x-coordinate of the left edge
    "width": 450,  # width of the region
    "height": 445,  # height of the region
}

# Initialize Matplotlib figure
# plt.ion()  # Interactive mode on
# fig, ax = plt.subplots()
# image = ax.imshow(np.zeros((region['height'], region['width'], 3), dtype=np.uint8))
window = cv2.namedWindow("window", cv2.WINDOW_NORMAL)

def image2grid(arr):
    grid = []
    rows, cols, _ = arr.shape
    cell_height = rows // N
    cell_width = cols // N
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    index = 0
    for i in range(N):
        row = []
        for j in range(N):
            d = min(cell_height, cell_width) // 6
            cx, cy = j * cell_width + cell_width // 2, i * cell_height + cell_height // 2
            pixel = arr[cy][cx]
            allEqual = True
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                x, y = cx + dx * d, cy + dy * d
                if np.abs(np.sum(pixel - arr[y][x])) < 40:
                    allEqual = False
                    break
            if allEqual:
                print(i, j)
            if allEqual and np.average(pixel) > 40:
                row.append(alphabet[index])
                index += 1
            else:
                row.append(0)
            # row.append(list(arr[i * cell_height + cell_height // 2][j * cell_width + cell_width // 2]))
        grid.append(row)
        
    return grid


try:
    while True:
        start_time = time.time()

        # Capture the screen
        screenshot = sct.grab(region)

        # Convert the screenshot to a NumPy array
        frame = np.array(screenshot)

        


        # Update the image in the plot
        # image.set_data(frame)
        cv2.imshow("window", frame)
        # check for 's'
        if cv2.waitKey(1) == ord('s'):
            print(image2grid(frame))

            # print(frame)
            print("Exited.")
            break
        # time.sleep(max(0, 1 / 20 - (time.time() - start_time)))
except KeyboardInterrupt:
    print(frame)
    print("Exited.")
finally:
    plt.ioff()  # Turn off interactive mode
    plt.show()
