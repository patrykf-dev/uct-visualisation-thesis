from enum import Enum


class Game(Enum):
    Chess = 1,
    Mancala = 2


class GameMode(Enum):
    PLAYER_VS_PLAYER = 1,
    PLAYER_VS_PC = 1,
    PC_VS_PC = 3
