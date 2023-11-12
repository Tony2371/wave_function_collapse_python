import pygame
import os

class TileMap:
    def __init__(self, size_x, size_y, scale_multiplier=100):
        self.size_x = size_x
        self.size_y = size_y
        self.scale_multiplier = scale_multiplier
        self.tiles = [Structure(x*scale_multiplier, y*scale_multiplier) for x in range(size_x) for y in range(size_y)]

class Structure:
    def __init__(self, pos_x, pos_y, tile_type='floor_outside'):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = type
        self.loaded_texture = pygame.image.load(f'textures/{tile_type}.png')

class Cursor:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.available_tiles = [tile_name.replace('.png', '') for tile_name in os.listdir('textures')]
        self.selected_tile_index = 0
        self.loaded_texture = pygame.image.load(f'textures/{self.available_tiles[self.selected_tile_index]}.png')
        self.loaded_texture.set_alpha(128)

    def switch_tile(self):
        self.selected_tile_index += 1
        if self.selected_tile_index >= len(self.available_tiles):
            self.selected_tile_index = 0
            
        self.loaded_texture = pygame.image.load(f'textures/{self.available_tiles[self.selected_tile_index]}.png')
        self.loaded_texture.set_alpha(128)
        