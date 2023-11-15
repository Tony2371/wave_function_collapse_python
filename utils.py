import pygame
import os
import time
import json
import random

class GridCollapse:
    def __init__(self, size_x, size_y, max_states, scale_multiplier=100):
        self.size_x = size_x
        self.size_y = size_y
        self.scale_multiplier = scale_multiplier
        self.tiles = [Tile(x*scale_multiplier, y*scale_multiplier, max_states=max_states) for x in range(size_x) for y in range(size_y)]

    def update_entropy(self, rules):
        for i in range(3):
            for core_tile in self.tiles:
                if isinstance(core_tile, Structure):
                    for i, neigbour in enumerate(self.tiles):
                        #UPDATE LEFT
                        if core_tile.pos_x == neigbour.pos_x-100 and core_tile.pos_y == neigbour.pos_y:
                            if isinstance(neigbour, Tile):
                                possible_tiles = rules[f'{core_tile.name}|{core_tile.rotation}']['left']
                                for possible_tile in possible_tiles:
                                    self.tiles[i].possible_tiles.add(possible_tile)
                                self.tiles[i].update_entropy()
                        
                        #UPDATE RIGHT
                        if core_tile.pos_x == neigbour.pos_x+100 and core_tile.pos_y == neigbour.pos_y:
                            if isinstance(neigbour, Tile):
                                possible_tiles = rules[f'{core_tile.name}|{core_tile.rotation}']['right']
                                for possible_tile in possible_tiles:
                                    self.tiles[i].possible_tiles.add(possible_tile)
                                self.tiles[i].update_entropy()

                        #UPDATE UP
                        if core_tile.pos_x == neigbour.pos_x and core_tile.pos_y == neigbour.pos_y-100:
                            if isinstance(neigbour, Tile):
                                possible_tiles = rules[f'{core_tile.name}|{core_tile.rotation}']['up']
                                for possible_tile in possible_tiles:
                                    self.tiles[i].possible_tiles.add(possible_tile)
                                self.tiles[i].update_entropy()
                        
                        #UPDATE DOWN
                        if core_tile.pos_x == neigbour.pos_x and core_tile.pos_y == neigbour.pos_y+100:
                            if isinstance(neigbour, Tile):
                                possible_tiles = rules[f'{core_tile.name}|{core_tile.rotation}']['down']
                                for possible_tile in possible_tiles:
                                    self.tiles[i].possible_tiles.add(possible_tile)
                                self.tiles[i].update_entropy()
        
    def collapse_tile(self):
        lowest_entropy = min([i.max_states for i in self.tiles if isinstance(i, Tile)])
        candidates_for_collapse = [i for i in self.tiles if isinstance(i, Tile) and i.max_states == lowest_entropy]
        
        for i, candidate in enumerate(self.tiles):
            if candidate == random.choice(candidates_for_collapse):
                name, rotation = random.choice(list(candidate.possible_tiles)).split('|')
                self.tiles[i] = Structure(pos_x=candidate.pos_x, pos_y=candidate.pos_y, tile_name=name, rotation=int(rotation))
                break

class TileMap:
    def __init__(self, size_x, size_y, scale_multiplier=100):
        self.size_x = size_x
        self.size_y = size_y
        self.scale_multiplier = scale_multiplier
        self.tiles = [Structure(x*scale_multiplier, y*scale_multiplier) for x in range(size_x) for y in range(size_y)]

    def generate_rules(self):
        rules_dict = {}
        for tile in self.tiles:
            if f'{tile.name}|{tile.rotation}' not in rules_dict:
                rules_dict[f'{tile.name}|{tile.rotation}'] = {'up': set(),
                                                              'down': set(),
                                                              'left': set(),
                                                              'right': set()}
            try:                
                rules_dict[f'{tile.name}|{tile.rotation}']['up'].add([f'{i.name}|{i.rotation}' for i in self.tiles if i.pos_x == tile.pos_x and i.pos_y == tile.pos_y-100][0])
            except:
                pass
            try:
                rules_dict[f'{tile.name}|{tile.rotation}']['down'].add([f'{i.name}|{i.rotation}' for i in self.tiles if i.pos_x == tile.pos_x and i.pos_y == tile.pos_y+100][0])
            except:
                pass
            try:
                rules_dict[f'{tile.name}|{tile.rotation}']['left'].add([f'{i.name}|{i.rotation}' for i in self.tiles if i.pos_x == tile.pos_x-100 and i.pos_y == tile.pos_y][0])
            except:
                pass
            try:
                rules_dict[f'{tile.name}|{tile.rotation}']['right'].add([f'{i.name}|{i.rotation}' for i in self.tiles if i.pos_x == tile.pos_x+100 and i.pos_y == tile.pos_y][0])
            except:
                pass

        for value in rules_dict.keys():
            print(value)
            print(rules_dict[value])
        

        for key in rules_dict:
            for direction in rules_dict[key]:
                rules_dict[key][direction] = list(rules_dict[key][direction])
        with open(f'generated_samples/rules_{time.time()}.json', 'w') as file:
            json.dump(rules_dict, file, indent=4)
        print('--------------------------')

class Structure:
    def __init__(self, pos_x, pos_y, tile_name='floor_outside', rotation=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = tile_name
        self.rotation = rotation
        self.loaded_texture = pygame.image.load(f'textures_structures/{tile_name}.png')
        self.loaded_texture = pygame.transform.rotate(self.loaded_texture, self.rotation)

    def update_tile(self, tile_name, rotation):
        self.name = tile_name
        self.rotation = rotation
        self.loaded_texture = pygame.image.load(f'textures_structures/{tile_name}.png')
        self.loaded_texture = pygame.transform.rotate(self.loaded_texture, self.rotation)

class Tile:
    def __init__(self, pos_x, pos_y, max_states):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.max_states = max_states
        self.possible_tiles = set()
    
    def update_entropy(self):
        self.max_states = len(self.possible_tiles)
        

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
            