from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_game_manager import ChessGameManager
from src.main_application.enums import GameMode
from src.main_application.game_canvas import GameCanvas
from src.uct.algorithm.mc_game_manager import MonteCarloGameManager


class ChessCanvas(GameCanvas):
    def __init__(self, game_mode: GameMode):
        super().__init__(game_mode)
        self.chess_manager = ChessGameManager(self.WIDTH, self.HEIGHT)
        game_state = ChessState(self.chess_manager.board)
        self.monte_carlo_manager = MonteCarloGameManager(game_state)

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        self.chess_manager.canvas_drawer.draw_board(QPainter(self))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if self.game_mode == GameMode.PC_VS_PC:
            return
        super().mousePressEvent(event)
        x = event.x()
        y = event.y()
        self.react_to_player_click(x, y)

    def perform_algorithm_move(self):
        super().perform_algorithm_move()
        move = self.monte_carlo_manager.calculate_next_move(max_iterations=30, max_moves_per_simulation=10)
        print(f"Algorithm decided to go {move.position_from} -> {move.position_to} for player {move.player}")

        if self.game_mode == GameMode.PC_VS_PC:
            self.chess_manager.deselect_last_moved()

        self.chess_manager.deselect_king()
        self.chess_manager.board.perform_legal_move(move)
        self.chess_manager.reset_selected_tile()
        self.on_update_tree(self.monte_carlo_manager.tree.root)
        if self.game_mode == GameMode.PC_VS_PC:
            self.monte_carlo_manager.perform_previous_move()
        self.repaint()

    def react_to_player_click(self, x, y):
        grid_pos = self.chess_manager.canvas_drawer.grid_click_to_tile(x, y)
        player_moved, player_move = self.chess_manager.react_to_tile_click(grid_pos)
        self.repaint()

        if player_moved and self.game_mode == GameMode.PLAYER_VS_PC:
            self.chess_manager.deselect_last_moved()
            self.monte_carlo_manager.notify_move_performed(player_move)
            super().perform_player_move()
