from PyQt5.QtWidgets import QMainWindow

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_canvas import ChessCanvas
from src.main_application.enums import Game, GameMode
from src.main_application.gui_settings import MonteCarloSettings, DisplaySettings
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.main_application.window_machine_vs_machine import MachineVsMachineWindow
from src.main_application.window_player_vs_machine import PlayerVsMachineWindow
from src.main_application.window_player_vs_player import PlayerVsPlayerWindow
from src.mancala.algorithm_relay.mancala_state import MancalaState
from src.mancala.mancala_canvas import MancalaCanvas


def create_proper_window(parent: QMainWindow, game: Game, game_mode: GameMode,
                         mc_settings: MonteCarloSettings, display_settings: DisplaySettings) -> QMainWindow:
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

    manager = MonteCarloWindowManager(canvas, game_mode, start_state, mc_settings)

    if game_mode == GameMode.PLAYER_VS_PC:
        return PlayerVsMachineWindow(parent, manager, display_settings)
    elif game_mode == GameMode.PLAYER_VS_PLAYER:
        return PlayerVsPlayerWindow(parent, manager)
    elif game_mode == GameMode.PC_VS_PC:
        return MachineVsMachineWindow(parent, manager, display_settings)
