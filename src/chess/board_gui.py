import numpy as np


class BoardGUI:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.grid = self.create_grid()

    def create_grid(self):
        from src.chess.game import TILE_HEIGHT, TILE_WIDTH, TILE_NUMBER
        self.grid = np.full((TILE_NUMBER, TILE_NUMBER), None)
        grid = [[(i * TILE_WIDTH, j * TILE_HEIGHT) for i in range(TILE_NUMBER)] for j in range(TILE_NUMBER)]
        for i, row in enumerate(grid[::-1]):
            for j, tile in enumerate(row):
                if (i + j) % 2 == 1:
                    tile_color = (255, 195, 77)
                else:
                    tile_color = (230, 115, 0)
                self.grid[i, j] = Tile(tile_color, tile, TILE_WIDTH, TILE_HEIGHT)
        return self.grid

    def mark_tile_selected(self, tile):
        self.grid[tile].select()

    def mark_tile_deselected(self, tile, when_checked=False):
        self.grid[tile].deselect(when_checked)

    def mark_tile_checked(self, tile):
        self.grid[tile].set_color_when_checked()

    def mark_tile_moved(self, tile):
        self.grid[tile].set_color_when_moved()


class Tile:
    def __init__(self, color, start_position, tile_width, tile_height):
        self.primary_color = color
        self.color = color
        self.start_position = start_position
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.chosen = False

    def select(self):
        self.color = (75, 225, 35)
        self.chosen = True

    def deselect(self, when_checked=False):
        self.color = self.primary_color if not when_checked else (230, 30, 50)
        self.chosen = False

    def set_color_when_checked(self):
        self.color = (230, 30, 50)

    def set_color_when_moved(self):
        self.color = (252, 229, 52) if self.primary_color == (255, 195, 77) else (241, 205, 0)
