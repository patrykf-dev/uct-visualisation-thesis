
import copy

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from main_application.game_canvas import GameCanvas
from mancala.algorithm_relay.mancala_move import MancalaMove
from mancala.mancala_board import MancalaBoard
from mancala.mancala_board_drawer import MancalaBoardDrawer
from uct.algorithm.enums import GamePhase


class MancalaCanvas(GameCanvas):
    """
    Class represents mancala GUI.
    """
    def __init__(self):
        super().__init__()
        self.board_drawer = MancalaBoardDrawer(self.WIDTH, self.HEIGHT)
        self.moves_sequence = []
        self.board = MancalaBoard()

    def paintEvent(self, event: QtGui.QPaintEvent):
        """
        Repaints game area. Overrides the base class.

		Args:
			event:  QtGui.QPaintEvent object, event that caused the repaint

		Returns:
			None        
		"""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.board_drawer.draw_board(painter, self.board)

    def mousePressEvent(self, event):
        """
        Handler to player's click event. Checks if player can move - if a valid move was chosen, it is executed then.
        Overrides the base class.

		Args:
			event:  QtGui.QMouseEvent with information about click

		Returns:
			None        
		"""
        if not self.player_can_click:
            return
        super().mousePressEvent(event)
        pos = event.pos()
        player_moved, moved_index = self.board_drawer.detect_click(pos.x(), pos.y())
        if not player_moved and self.board_drawer.selected_hole_index != -1:
            board_index = self.board_drawer.draw_index_to_board_index(self.board_drawer.selected_hole_index)
            if not self.board.is_hole_valid(board_index):
                self.board_drawer.selected_hole_index = -1
        extra_turn = False
        if player_moved:
            old_board_values = copy.deepcopy(self.board.board_values)
            extra_turn = self.board.perform_move_internal(moved_index, self.board.current_player)
            self.board_drawer.update_stones_positions(self.board, old_board_values)
            self.moves_sequence.append(moved_index)
        self.repaint()

        if not extra_turn and player_moved or self.board.phase != GamePhase.IN_PROGRESS:
            player = 1 if self.board.current_player == 2 else 2
            player_move = MancalaMove(copy.deepcopy(self.moves_sequence), player)
            self.moves_sequence.clear()
            move_info = {"move": player_move, "phase": self.board.phase}
            self.player_move_performed.fire(self, earg=move_info)

    def perform_algorithm_move(self, move: MancalaMove):
        """
        Performs PC's move and causes a game area repaint.

		Args:
			move:  MancalaMove object

		Returns:
			None        
		"""
        super().perform_algorithm_move(move)
        old_board_values = copy.deepcopy(self.board.board_values)
        self.board.perform_move(move)
        self.board_drawer.update_stones_positions(self.board, old_board_values)
        self.repaint()

