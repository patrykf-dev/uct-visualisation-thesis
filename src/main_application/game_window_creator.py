from PyQt5.QtWidgets import QMainWindow

from src.chess.chess_canvas import ChessCanvas
from src.main_application.enums import Game, GameMode
from src.main_application.window_machine_vs_machine import MachineVsMachineWindow
from src.main_application.window_player_vs_machine import PlayerVsMachineWindow
from src.main_application.window_player_vs_player import PlayerVsPlayerWindow


def create_proper_window(parent: QMainWindow, game: Game, game_mode: GameMode) -> QMainWindow:
    canvas = ChessCanvas(game_mode)
    if game_mode == GameMode.PLAYER_VS_PC:
        return PlayerVsMachineWindow(canvas, parent)
    elif game_mode == GameMode.PLAYER_VS_PLAYER:
        return PlayerVsPlayerWindow(canvas, parent)
    elif game_mode == GameMode.PC_VS_PC:
        return MachineVsMachineWindow(canvas, parent)
