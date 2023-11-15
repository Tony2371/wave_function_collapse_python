import json
from utils import *
import pygame
from math import floor
import pickle
import time

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
            if event.key == pygame.K_e:
                cursor.rotate_tile()
            
            if event.key == pygame.K_s:
               tilemap.generate_rules()
               pygame.image.save(screen, f'generated_samples/sample_{time.time()}.jpg')
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in tilemap.tiles:
                if tile.pos_x == cursor.pos_x and tile.pos_y == cursor.pos_y:
                    if event.button == 1:
                        tile.update_tile(cursor.selected_tile_name, cursor.selected_rotation)
                    if event.button == 3:
                        tile.update_tile('floor_outside', 0)
                    
                    if event.button == 4:
                        cursor.switch_tile_foward()
                    if event.button == 5:
                        cursor.switch_tile_backwards()
                

    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor.pos_x = floor(mouse_x/100)*100
    cursor.pos_y = floor(mouse_y/100)*100

    # GENERAL RENDERING PART
    for tile in tilemap.tiles:
        screen.blit(tile.loaded_texture, (tile.pos_x, tile.pos_y))

    '''
    for tile in set(tilemap.tiles):
        if tile.name != 'floor_outside':
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render(f'{tile.name}', True, (0, 0, 0))
            all_x = [i.pos_x for i in tilemap.tiles if i.name == tile.name]
            sum_pos_x = sum(all_x)/len(all_x)
            all_y = [i.pos_y for i in tilemap.tiles if i.name == tile.name]
            sum_pos_y = sum(all_y)/len(all_y)

            screen.blit(text, (sum_pos_x, sum_pos_y+45))
    '''
    
    screen.blit(cursor.loaded_texture, (cursor.pos_x, cursor.pos_y)) # cursor should be rendered above everything
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f'Selected tile: {cursor.selected_tile_name}', True, (0, 0, 0))
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)


pygame.quit()

