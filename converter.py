import time
import numpy as np
import matplotlib.pyplot as plt
from mss import mss
import cv2

# Set up MSS for screen capture
sct = mss()

N = 10

# Define the region to capture (adjust to target a specific window or area)
region = {
    "top": 330,  # y-coordinate of the top edge
    "left": 768,  # x-coordinate of the left edge
    "width": 450,  # width of the region
    "height": 450,  # height of the region
}

# Initialize Matplotlib figure
# plt.ion()  # Interactive mode on
# fig, ax = plt.subplots()
# image = ax.imshow(np.zeros((region['height'], region['width'], 3), dtype=np.uint8))
window = cv2.namedWindow("window", cv2.WINDOW_NORMAL)

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
            print(frame)
            print("Exited.")
            break
        # time.sleep(max(0, 1 / 20 - (time.time() - start_time)))
except KeyboardInterrupt:
    print(frame)
    print("Exited.")
finally:
    plt.ioff()  # Turn off interactive mode
    plt.show()
