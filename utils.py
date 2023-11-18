import pygame
import os

class TileBase:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class TileStructure:
    def __init__(self, structure_type, rotation):
        self.structure_type = structure_type
        self.rotation = rotation

class TileRoom:
    def __init__(self, room_type):
        self.room_type = room_type

class Tile:
    def __init__(self, pos_x, pos_y):
        self.location = TileBase(pos_x, pos_y)
        self.room = None
        self.structure = None

    def set_room(self, room_type):
        self.room = TileRoom(room_type)

    def set_structure(self, structure_type, rotation):
        self.structure = TileStructure(structure_type, rotation)


class TileMap:
    def __init__(self, size_x, size_y, scale_multiplier=100):
        self.size_x = size_x
        self.size_y = size_y
        self.scale_multiplier = scale_multiplier
        self.tiles = [Tile(pos_x=x*scale_multiplier, pos_y=y*scale_multiplier) for x in range(size_x) for y in range(size_y)]

class Cursor:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.available_tiles = [tile_name.replace('.png', '') for tile_name in os.listdir('textures_structures')]
        self.selected_tile_index = 0
        self.selected_tile_name = self.available_tiles[self.selected_tile_index]
        self.selected_rotation = 0
        self.loaded_texture = pygame.image.load(f'textures_structures/{self.available_tiles[self.selected_tile_index]}.png')
        self.loaded_texture.set_alpha(128)

    def switch_tile_foward(self):
        self.selected_tile_index += 1
        if self.selected_tile_index >= len(self.available_tiles):
            self.selected_tile_index = 0
            
        self.loaded_texture = pygame.image.load(f'textures_structures/{self.available_tiles[self.selected_tile_index]}.png')
        self.loaded_texture.set_alpha(128)
        self.selected_tile_name = self.available_tiles[self.selected_tile_index]
        self.selected_rotation = 0
    
    def switch_tile_backwards(self):
        self.selected_tile_index -= 1
        if self.selected_tile_index <= -1*len(self.available_tiles)-1:
            self.selected_tile_index = 0
        
        self.loaded_texture = pygame.image.load(f'textures_structures/{self.available_tiles[self.selected_tile_index]}.png')
        self.loaded_texture.set_alpha(128)
        self.selected_tile_name = self.available_tiles[self.selected_tile_index]
        self.selected_rotation = 0
    
    def rotate_tile(self):
        self.loaded_texture = pygame.transform.rotate(self.loaded_texture, -90)
        self.selected_rotation -= 90
        if self.selected_rotation <= -360:
            self.selected_rotation = 0

class TextureCache:
    def __init__(self):
        self.textures = {}

    def get_texture(self, file_path):
        if file_path not in self.textures:
            # Load the texture if it's not already loaded
            self.textures[file_path] = pygame.image.load(file_path)
        return self.textures[file_path]
