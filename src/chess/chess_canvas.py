import os

from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtWidgets import QWidget

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_game_manager import ChessGameManager
from src.uct.algorithm.mc_game_manager import MonteCarloGameManager


class ChessCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.WIDTH = 600
        self.HEIGHT = 600
        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.setMaximumSize(self.WIDTH, self.HEIGHT)
        self.TILE_NUMBER = 8
        self.TILE_WIDTH = int(self.WIDTH / self.TILE_NUMBER)
        self.TILE_HEIGHT = int(self.HEIGHT / self.TILE_NUMBER)
        self.ICONS_FOLDER = os.path.join(os.path.realpath(__file__), "..", "icons")
        self.game_manager = ChessGameManager(self.TILE_NUMBER, self.TILE_WIDTH, self.TILE_HEIGHT)

        self.painter = None

        game_state = ChessState(self.game_manager.board)
        self.monte_carlo_manager = MonteCarloGameManager(game_state)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)
        self.draw_board(QPainter(self))

    def draw_board(self, painter):
        for i, row in enumerate(self.game_manager.board_gui.grid):
            for j, tile in enumerate(row):
                painter.fillRect(tile.start_position[0], tile.start_position[1],
                                 tile.tile_width, tile.tile_height,
                                 QColor(tile.color[0], tile.color[1], tile.color[2], 255))
                tile_figure = self.game_manager.board.figures.get_figure_at((i, j))
                if tile_figure:
                    self.draw_figure(tile_figure, tile.start_position, painter)
                # tile_text_surface = self.TILES_FONT.render(f"{i}, {j}", False, (255, 255, 255))
                # self.screen.blit(tile_text_surface, tile.start_position)

    def draw_figure(self, figure, tile_pos, painter):
        if figure:
            path = os.path.join(self.ICONS_FOLDER, figure.image_file)
            image = QImage(path)
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap.detach()
            point = QRect(tile_pos[0], tile_pos[1], self.TILE_WIDTH, self.TILE_HEIGHT)
            painter.drawPixmap(point, pixmap)
