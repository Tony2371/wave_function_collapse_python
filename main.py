import json
from utils import *
import cv2
import numpy as np
import time

# Read configuration settings
with open('configuration.json', 'r') as config_file:
    config = json.load(config_file)
    chunk_width = config['chunk_width']
    chunk_height = config['chunk_height']

scale_multiplier = 100 # SCALE in pixels. 100 pixels is 1 meter

# Initialize the tile map with values from the configuration file
tilemap = TileMap(chunk_width, chunk_height, scale_multiplier)

running = True

while running:


    # RENDERING PART
    chunk = np.zeros((chunk_height*scale_multiplier, chunk_width*scale_multiplier, 3), dtype="uint8")


    for tile in tilemap.tiles:
        floor = cv2.imread('textures/floor.png')
    

        x_offset = tile[0]
        y_offset = tile[1]
        chunk[y_offset:y_offset+floor.shape[0], x_offset:x_offset+floor.shape[1]] = floor


    cv2.imshow('Overlayed Image', chunk)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()

    running = False
