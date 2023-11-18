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
cursor_type = 'room'
cursor = Cursor(cursor_type=cursor_type)
texture_cache = TextureCache()

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
            for i, tile in enumerate(tilemap.tiles):
                if tile.location.pos_x == cursor.pos_x and tile.location.pos_y == cursor.pos_y:
                    if event.button == 1:
                        tilemap.tiles[i] = Tile(pos_x=cursor.pos_x, 
                                                pos_y=cursor.pos_y)
                        if cursor_type == 'structure':
                            tilemap.tiles[i].set_structure(structure_type=cursor.selected_tile_name, 
                                                            rotation=cursor.selected_rotation)
                        if cursor_type == 'room':
                            tilemap.tiles[i].set_room(room_type=cursor.selected_tile_name)

                    if event.button == 3:
                        tilemap.tiles[i].room = None
                        tilemap.tiles[i].structure = None
                    
                    if event.button == 4:
                        cursor.switch_tile_foward()
                    if event.button == 5:
                        cursor.switch_tile_backwards()
                

    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor.pos_x = floor(mouse_x/100)*100
    cursor.pos_y = floor(mouse_y/100)*100

    # GENERAL RENDERING PART
    screen.fill((0,0,0))
    for tile in tilemap.tiles:
        if isinstance(tile.structure, TileStructure):
            loaded_texture = pygame.transform.rotate(texture_cache.structure_textures[tile.structure.structure_type], tile.structure.rotation)
            screen.blit(loaded_texture, (tile.location.pos_x, tile.location.pos_y))
        
        if isinstance(tile.room, TileRoom):
            loaded_texture = pygame.transform.scale(texture_cache.room_textures[tile.room.room_type], (100, 100))
            screen.blit(loaded_texture, (tile.location.pos_x, tile.location.pos_y))

        else:
            screen.blit(texture_cache.empty_texture, (tile.location.pos_x, tile.location.pos_y))

    
    screen.blit(cursor.loaded_texture, (cursor.pos_x, cursor.pos_y)) # cursor should be rendered above everything
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f'Selected tile: {cursor.selected_tile_name}', True, (0, 0, 0))
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)


pygame.quit()

