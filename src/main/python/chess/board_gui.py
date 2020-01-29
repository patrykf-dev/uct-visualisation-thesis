
import numpy as np


class BoardGUI:
    """
    Class responsible for GUI board tile colors.
    """
    def __init__(self, tiles_count, tile_width, tile_height):
        self.grid = self.create_grid(tiles_count, tile_width, tile_height)

    def create_grid(self, tiles_count, tile_width, tile_height):
        """
        Fill board with colors. Even tiles are the lighter and odd one are the darker.

		Args:
			tiles_count:  How big the chessboard is (we assume 8x8)
			tile_width:  depends on the game window size
			tile_height:  depends on the game window size

		"""
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
        """
        Selects a tile - marks it with color in GUI.

		Args:
			tile:  Tile object

		"""
        self.grid[tile].select()

    def mark_tile_deselected(self, tile, when_checked=False):
        """
        Deselects a tile - turns tile color to a previous one it had.

		Args:
			tile:  Tile object
			when_checked:  bool flag to be passed further

		"""
        self.grid[tile].deselect(when_checked)

    def mark_tile_checked(self, tile):
        """
        Marks the tile to signalize that the king is ckeched.

		Args:
			tile:  Tile object

		"""
        self.grid[tile].set_color_when_checked()

    def mark_tile_moved(self, tile):
        """
        Marks tiles of last move (old and nwe positions).

		Args:
			tile:  Tile object

		"""
        self.grid[tile].set_color_when_moved()


class Tile:
    """
    Class responsible for keeping information about specific GUI board tile - its position and color
    """
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
        """
        When the user clicks on tile in GUI, it should be seen as selected.
        """
        self.color = Tile.SELECTED_COLOR

    def deselect(self, when_checked=False):
        """
        Tile deselection - when the user chooses tile and then chooses another, the previous selected tile must
         be deselected. The same idea is when th user moves.

		Args:
			when_checked:  When check, tile below the king is marked as well. When deselecting, we need to keep it.

		"""
        self.color = self.primary_color if not when_checked else Tile.CHECKED_COLOR

    def set_color_when_checked(self):
        """
        Marks tile on the king position to signalize check.
        """
        self.color = Tile.CHECKED_COLOR

    def set_color_when_moved(self):
        """
        When the move is done, we need to inform user in GUI which one was it. Ols and new moved figure's positions are
        marked.
        """
        self.color = Tile.LAST_MOVED_COLOR

