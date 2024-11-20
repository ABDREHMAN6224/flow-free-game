import cv2
import numpy as np
import matplotlib.pyplot as plt


# Load the provided image
image_path = "./a.jpeg"
image = cv2.imread(image_path)

# Resize for better visualization (optional)
image = cv2.resize(image, (800, 800))

# Convert the image to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the dimensions of the image (to decide the grid size)
image_height, image_width, _ = image.shape

# Define the grid size (rows x columns)
grid_rows, grid_cols = 8, 8  # Based on your provided example

# Calculate the cell size
cell_height = image_height // grid_rows
cell_width = image_width // grid_cols

# Create a grid representation
grid = []

# Loop through the grid and assign colors
for i in range(grid_rows):
    row = []
    for j in range(grid_cols):
        # Extract the cell
        cell = image_rgb[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]

        # Calculate the average color in the cell
        avg_color = np.mean(cell.reshape(-1, 3), axis=0)
        avg_color = tuple(map(int, avg_color))  # Convert to integer tuple

        # Assign a unique label to the color
        if np.all(avg_color == [255, 255, 255]):
            row.append(0)  # Assign 0 for white (empty cell)
        else:
            row.append(avg_color)
    grid.append(row)

# show image
# plt.imshow(image_rgb)
# plt.title("Original Image")
# plt.axis('off')
# plt.show()

# show grid image
plt.imshow(grid)
plt.title("Grid Representation")
plt.show()
# Display the grid


