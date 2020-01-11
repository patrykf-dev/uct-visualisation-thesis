import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from chess.algorithm_relay.chess_state import ChessState
from chess.chess_canvas import ChessCanvas
from main_application.enums import Game, GameMode
from main_application.game_window import GameWindow
from main_application.gui_settings import MonteCarloSettings, DisplaySettings
from main_application.mc_window_manager import MonteCarloWindowManager
from main_application.window_machine_vs_machine import MachineVsMachineWindow
from main_application.window_player_vs_machine import PlayerVsMachineWindow
from main_application.window_player_vs_player import PlayerVsPlayerWindow
from mancala.algorithm_relay.mancala_state import MancalaState
from mancala.mancala_canvas import MancalaCanvas


def create_proper_window(parent: QMainWindow, game: Game, game_mode: GameMode,
                         mc_settings: MonteCarloSettings, display_settings: DisplaySettings) -> GameWindow:
    """
    Based on user decisions, function creates a proper window with game and visualization, applying chosen settings.
    :param parent: main window object
    :param game: game chosen by user by radiobutton (chess, mancala etc.)
    :param game_mode: game mode chosen by user by radiobutton (player vs PC etc.)
    :param mc_settings: settings given by user by values in text fields (max iterations etc.)
    :param display_settings: settings connected with displaying algorithm's progress
    :return: QMainWindow object
    """
    if game == Game.Chess:
        canvas = ChessCanvas()
        start_state = ChessState(canvas.chess_manager.board)
    else:
        canvas = MancalaCanvas()
        start_state = MancalaState(canvas.board)

    manager = MonteCarloWindowManager(canvas, game_mode, start_state, mc_settings, game)

    window = None
    if game_mode == GameMode.PLAYER_VS_PC:
        window = PlayerVsMachineWindow(parent, manager, display_settings)
    elif game_mode == GameMode.PLAYER_VS_PLAYER:
        window = PlayerVsPlayerWindow(parent, manager)
    elif game_mode == GameMode.PC_VS_PC:
        manager.canvas.set_player_can_click(False)
        window = MachineVsMachineWindow(parent, manager, display_settings)

    if game == Game.Chess:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "chess-icon.png")
        window.setWindowIcon(QIcon(icon_path))
        window.setWindowTitle("Chess")
    elif game == Game.Mancala:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "mancala-icon.png")
        window.setWindowIcon(QIcon(icon_path))
        window.setWindowTitle("Mancala")

    return window
