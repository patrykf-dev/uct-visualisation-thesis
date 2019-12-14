from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from src.chess.chess_game_manager import ChessGameManager
from src.main_application.game_canvas import GameCanvas
from src.chess.algorithm_relay.chess_state import ChessState


class ChessCanvas(GameCanvas):
    def __init__(self):
        super().__init__()
        self.chess_manager = ChessGameManager(self.WIDTH, self.HEIGHT)

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        self.chess_manager.canvas_drawer.draw_board(QPainter(self))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        x = event.x()
        y = event.y()
        self.react_to_player_click(x, y)

    def perform_algorithm_move(self, move):
        self.chess_manager.deselect_king()
        self.chess_manager.board.perform_legal_move(move)
        self.chess_manager.reset_selected_tile()

        self.repaint()

    def react_to_player_click(self, x, y):
        grid_pos = self.chess_manager.canvas_drawer.grid_click_to_tile(x, y)
        player_moved, player_move = self.chess_manager.react_to_tile_click(grid_pos)
        self.repaint()

        if player_moved:
            move_info = {"move": player_move,
                         "phase": ChessState.cast_chess_phase_to_abstract_phase(self.chess_manager.board.game_status)}
            self.player_move_performed.fire(self, earg=move_info)
