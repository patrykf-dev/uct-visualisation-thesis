from enum import Enum


class FigureType(Enum):
    PAWN = 1,
    KNIGHT = 2,
    BISHOP = 3,
    ROOK = 4,
    QUEEN = 5,
    KING = 6


class Color(Enum):
    WHITE = 0,
    BLACK = 1


class MoveType(Enum):
    NORMAL = 0,
    PAWN_DOUBLE_MOVE = 1,
    EN_PASSANT = 2,
    PROMOTION = 3,
    CASTLE_SHORT = 4,
    CASTLE_LONG = 5


class GameStatus(Enum):
    IN_PROGRESS = 0
    CHECKMATE_WHITE = 1
    CHECKMATE_BLACK = 2
    STALEMATE = 3
    DRAW = 4
    THREEFOLD_REPETITION = 5
    PERPETUAL_CHECK = 6
    FIFTY_MOVE_RULE = 7


class TileColor(Enum):
    LIGHT_SQUARE = 0
    DARK_SQUARE = 1
    SELECTED = 2
    CHECKED = 3
    LAST_MOVE_LIGHT = 4
    LAST_MOVE_DARK = 5


class TileMarkType(Enum):
    SELECTED = 0,
    DESELECTED = 1,
    MOVED = 2,
    CHECKED = 3


class TileMarkArgs:
    """
    CLass contains information about tile-marking type and its position.
    Tile can be:
    - selected, when a figure is selected
    - marked as check
    - marked as a past move
    """
    def __init__(self, pos, tile_mark_type: TileMarkType):
        self.pos = pos
        self.tile_mark_type = tile_mark_type
