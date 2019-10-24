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


class MoveStatus(Enum):
    FIGURE_SELECTED = 0,
    FIGURE_NOT_SELECTED = 1


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
