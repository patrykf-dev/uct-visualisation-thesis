from enum import Enum

import numpy as np


class BoardGUI:
    def __init__(self, tiles_count, tile_width, tile_height):
        self.grid = self.create_grid(tiles_count, tile_width, tile_height)

    def create_grid(self, tiles_count, tile_width, tile_height):
        self.grid = np.full((tiles_count, tiles_count), None)
        grid = [[(i * tile_width, j * tile_height) for i in range(tiles_count)] for j in range(tiles_count)]
        for i, row in enumerate(grid[::-1]):
            for j, tile in enumerate(row):
                if (i + j) % 2 == 1:
                    tile_color = (255, 195, 77)
                else:
                    tile_color = (230, 115, 0)
                self.grid[i, j] = Tile(tile_color, tile, tile_width, tile_height)
        return self.grid

    def mark_tile_selected(self, tile):
        self.grid[tile].select()

    def mark_tile_deselected(self, tile, when_checked=False):
        self.grid[tile].deselect(when_checked)

    def mark_tile_checked(self, tile):
        self.grid[tile].set_color_when_checked()

    def mark_tile_moved(self, tile):
        self.grid[tile].set_color_when_moved()


class TileMarkType(Enum):
    SELECTED = 0,
    DESELECTED = 1,
    MOVED = 2,
    CHECKED = 3


class Tile:
    SELECTED_COLOR = (75, 225, 35)
    CHECKED_COLOR = (230, 30, 50)
    LAST_MOVED_COLOR = (160, 160, 160)

    def __init__(self, color, start_position, tile_width, tile_height):
        self.primary_color = color
        self.color = color
        self.start_position = start_position
        self.tile_width = tile_width
        self.tile_height = tile_height

    def select(self):
        self.color = Tile.SELECTED_COLOR

    def deselect(self, when_checked=False):
        self.color = self.primary_color if not when_checked else Tile.CHECKED_COLOR

    def set_color_when_checked(self):
        self.color = Tile.CHECKED_COLOR

    def set_color_when_moved(self):
        self.color = Tile.LAST_MOVED_COLOR
