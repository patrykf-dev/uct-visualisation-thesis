
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from chess.chess_game_manager import ChessGameManager
from main_application.game_canvas import GameCanvas
from chess.algorithm_relay.chess_state import ChessState


class ChessCanvas(GameCanvas):
    """
    Class represents chess GUI.
    """
    def __init__(self):
        super().__init__()
        self.chess_manager = ChessGameManager(self.WIDTH, self.HEIGHT)

    def paintEvent(self, event: QtGui.QPaintEvent):
        """
        Repaints board. Overrides the base class.

		Args:
			event:  QtGui.QPaintEvent object, event that caused the repaint

		Returns:
			None        
		"""
        super().paintEvent(event)
        self.chess_manager.canvas_drawer.draw_board(QPainter(self))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """
        Handler to player's click event. Overrides the base class.

		Args:
			event:  QtGui.QMouseEvent with information about click

		Returns:
			None        
		"""
        if not self.player_can_click:
            return
        super().mousePressEvent(event)
        x = event.x()
        y = event.y()
        self.react_to_player_click(x, y)

    def perform_algorithm_move(self, move):
        """
        Performs PC's move and causes a board repaint.

		Args:
			move:  ChessMove object

		Returns:
			None        
		"""
        self.chess_manager.deselect_last_moved()
        self.chess_manager.deselect_king()
        self.chess_manager.board.perform_legal_move(move)
        self.chess_manager.reset_selected_tile()

        self.repaint()

    def react_to_player_click(self, x, y):
        """
        Reacts to player's click on chessboard based on its coordinates.
        If a move was made - it notifies the move handler.

		Args:
			x:  x-coordinate of a click
			y:  y-coordinate of a click

		Returns:
			None        
		"""
        grid_pos = self.chess_manager.canvas_drawer.grid_click_to_tile(x, y)
        player_moved, player_move = self.chess_manager.react_to_tile_click(grid_pos)
        self.repaint()

        if player_moved:
            move_info = {"move": player_move,
                         "phase": ChessState.cast_chess_phase_to_abstract_phase(self.chess_manager.board.game_status)}
            self.player_move_performed.fire(self, earg=move_info)


