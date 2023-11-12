class TileMap:
    def __init__(self, size_x, size_y, scale_multiplier=100):
        self.size_x = size_x
        self.size_y = size_y
        self.scale_multiplier = scale_multiplier
        self.tiles = [(x * scale_multiplier, y * scale_multiplier) for x in range(size_x) for y in range(size_y)]