import cv2
import numpy as np
import matplotlib.pyplot as plt


# Load the provided image
image_path = "./a.jpeg"
image = cv2.imread(image_path)

# Resize for better visualization (optional)
image = cv2.resize(image, (800, 800))
def image2grid(image, n=8):
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display the dimensions of the image (to decide the grid size)
    image_height, image_width, _ = image.shape

    # Define the grid size (rows x columns)
    grid_rows, grid_cols = n, n  # Based on your provided example

    # Calculate the cell size
    cell_height = image_height // grid_rows
    cell_width = image_width // grid_cols

    # Create a grid representation
    grid = []
    colors = {
        '251_137_2': 'o',
        '0_140_0': 'g',
        '254_0_2': 'r',
        '234_225_0': 'y',
        '2_255_255': 'c', # cyan
        '11_41_253': 'b', # blue
        '165_41_41': 'm', # magenta
        '253_10_198': 'p' # pink
    }

    # Loop through the grid and assign colors
    for i in range(grid_rows):
        row = []
        for j in range(grid_cols):
            pixel = image_rgb[i * cell_height + cell_height // 2, j * cell_width + cell_width // 2]
            color = '_'.join(map(str, pixel))
            row.append(colors[color] if color in colors else 0)
        grid.append(row)
    
    return grid

# show grid image

if __name__ == "__main__":
    grid = image2grid(image)
    for i in grid:
        for v in i:
            print(v, end=' ')
        print()
    # print(grid)
    # plt.imshow(grid)
    # plt.title("Grid Representation")
    # plt.show()
# print(grid)
# plt.imshow(grid)
# plt.title("Grid Representation")
# plt.show()
# Display the grid


