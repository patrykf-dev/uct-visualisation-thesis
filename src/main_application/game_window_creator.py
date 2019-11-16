from PyQt5.QtWidgets import QMainWindow

from src.main_application.chess_game_window import ChessGameWindow
from src.main_application.enums import Game, GameMode


def create_proper_window(parent: QMainWindow, game: Game, game_mode: GameMode) -> QMainWindow:
    return ChessGameWindow(parent)
