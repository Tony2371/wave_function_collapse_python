import json
from utils import *
import pygame
from math import floor

with open('configuration.json', 'r') as config_file:
    config = json.load(config_file)
    chunk_width = config['chunk_width']
    chunk_height = config['chunk_height']

scale_multiplier = 100 # SCALE in pixels. 100 pixels is 1 meter

pygame.init()
screen = pygame.display.set_mode((chunk_width*scale_multiplier, chunk_height*scale_multiplier)) # 100 is a scale multiplier
clock = pygame.time.Clock()
running = True

# PRELOADS
tilemap = TileMap(chunk_width, chunk_height, scale_multiplier)
cursor = Cursor()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:  # Check if the event is KEYDOWN
            if event.key == pygame.K_r:
                cursor.switch_tile()
                

    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor.pos_x = floor(mouse_x/100)*100
    cursor.pos_y = floor(mouse_y/100)*100



    # GENERAL RENDERING PART
    for tile in tilemap.tiles:
        screen.blit(tile.loaded_texture, (tile.pos_x, tile.pos_y))
    
    screen.blit(cursor.loaded_texture, (cursor.pos_x, cursor.pos_y)) # cursor should be rendered above everything


    pygame.display.flip()
    clock.tick(30)


pygame.quit()