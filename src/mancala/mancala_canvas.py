from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from src.main_application.enums import GameMode
from src.main_application.game_canvas import GameCanvas
from src.mancala.mancala_board_drawer import MancalaBoardDrawer
from src.mancala.mancala_board import MancalaBoard


class MancalaCanvas(GameCanvas):
    def __init__(self, game_mode: GameMode):
        super().__init__(game_mode)
        self.board_drawer = MancalaBoardDrawer(self.WIDTH, self.HEIGHT)
        self.board = MancalaBoard()

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.board_drawer.draw_board(painter, self.board)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        pos = event.pos()
        player_moved, moved_index = self.board_drawer.detect_click(pos.x(), pos.y())
        if player_moved:
            self.board.perform_move(moved_index)
        self.repaint()


