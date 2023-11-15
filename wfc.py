import json
import os
from utils import *
import random

with open('configuration.json', 'r') as config_file:
    config = json.load(config_file)
    chunk_width = config['chunk_width']
    chunk_height = config['chunk_height']

with open(f"generated_samples/{os.listdir('generated_samples')[0]}") as file:
    rules_dict = json.load(file)

all_states = list(set(rules_dict.keys()))

scale_multiplier = 100 # SCALE in pixels. 100 pixels is 1 meter

pygame.init()
screen = pygame.display.set_mode((chunk_width*scale_multiplier, chunk_height*scale_multiplier)) # 100 is a scale multiplier
clock = pygame.time.Clock()
running = True

# PRELOADS
collapse_map = GridCollapse(chunk_width, chunk_height, max_states=len(set(rules_dict.keys())),scale_multiplier=scale_multiplier)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    initial_tile_coord = (400, 400)
    for i, tile in enumerate(collapse_map.tiles):
        if tile.pos_x == initial_tile_coord[0] and tile.pos_y == initial_tile_coord[1] and not isinstance(tile, Structure):
            tile_name, rotation = random.choice(all_states).split('|')
            collapse_map.tiles[i] = Structure(tile.pos_x, tile.pos_y, tile_name=tile_name, rotation=int(rotation))

    # UPDATE ENTROPY
    try:
        collapse_map.update_entropy(rules=rules_dict)
        collapse_map.collapse_tile()
    except:
        pass
    
    # RENDERNG
    screen.fill((30,50,50))
    for tile in collapse_map.tiles:
        if isinstance(tile, Structure):
            screen.blit(tile.loaded_texture, (tile.pos_x, tile.pos_y))

        if isinstance(tile, Tile):
            font = pygame.font.Font('freesansbold.ttf', 18)
            text = font.render(f'{tile.max_states}', True, (250, 250, 250))
            screen.blit(text, (tile.pos_x+40, tile.pos_y+45))
            

    pygame.display.flip()
    clock.tick(30)