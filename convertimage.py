import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Function to create and save image
def create_image(color, filename):
    img = np.zeros((64, 64, 3), dtype=np.uint8)
    if color == "green":
        img[:, :] = [0, 255, 0]  # Green
    elif color == "brown":
        img[:, :] = [139, 69, 19]  # Brown (forest)
    elif color == "gray":
        img[:, :] = [128, 128, 128]  # Gray (mountain)
    elif color == "blue":
        img[:, :] = [0, 0, 255]  # Blue (city)
    image = Image.fromarray(img)
    image.save(filename)

# Create and save the images
create_image("green", "grass.png")
create_image("brown", "forest.png")
create_image("gray", "mountain.png")
create_image("blue", "city.png")