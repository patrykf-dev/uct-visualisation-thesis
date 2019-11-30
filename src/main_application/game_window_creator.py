from PyQt5.QtWidgets import QMainWindow

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_canvas import ChessCanvas
from src.main_application.enums import Game, GameMode
from src.main_application.mc_settings import MonteCarloSettings
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.main_application.window_machine_vs_machine import MachineVsMachineWindow
from src.main_application.window_player_vs_machine import PlayerVsMachineWindow
from src.main_application.window_player_vs_player import PlayerVsPlayerWindow
from src.mancala.algorithm_relay.mancala_state import MancalaState
from src.mancala.mancala_canvas import MancalaCanvas


def create_proper_window(parent: QMainWindow, game: Game, game_mode: GameMode,
                         settings: MonteCarloSettings) -> QMainWindow:
    if game == Game.Chess:
        canvas = ChessCanvas()
        start_state = ChessState(canvas.chess_manager.board)
    else:
        canvas = MancalaCanvas()
        start_state = MancalaState(canvas.board)

    manager = MonteCarloWindowManager(canvas, game_mode, start_state, settings)

    if game_mode == GameMode.PLAYER_VS_PC:
        return PlayerVsMachineWindow(manager, parent)
    elif game_mode == GameMode.PLAYER_VS_PLAYER:
        return PlayerVsPlayerWindow(manager, parent)
    elif game_mode == GameMode.PC_VS_PC:
        return MachineVsMachineWindow(manager, parent)
