
import os

from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QColor, QImage, QBrush

from main_application.resources_container import ResourcesContainer


class ChessCanvasDrawer:
    """
    Class is responsible for drawing chessboard: figures, tiles and possible moves.
    """
    def __init__(self, width, height, chess_manager):
        self.tiles_count = 8
        self.height = height
        self.chess_manager = chess_manager
        self.tile_width = int(width / self.tiles_count)
        self.tile_height = int(height / self.tiles_count)
        self.icons_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")

    def grid_click_to_tile(self, x, y):
        """
        Transforms mouse click coordinates to tile number.
        Example: click (85, 15) -> tile (7, 1) for height and width = 75

		Args:
			x:  x-coordinate of a mouse click
			y:  y-coordinate of a mouse click

		Returns:
			tuple describing a chessboard's tile        
		"""
        if y == 0:
            y = 1
        return (x // self.tile_width, (self.height - y) // self.tile_height)[::-1]

    def _tile_to_grid(self, positions):
        return [(x[1] * self.tile_width, x[0] * self.tile_height) for x in positions]

    def draw_board(self, painter):
        """
        Draws figures, tiles and possible moves.

		Args:
			painter:  QPainter object from PyQt library that enables drawing e.g. rectangles

		Returns:
			None        
		"""
        font = painter.font()
        font.setPixelSize(14)
        painter.setFont(font)
        pen = painter.pen()
        pen.setColor(QColor(255, 255, 255, 255))
        painter.setPen(pen)
        for i, row in enumerate(self.chess_manager.board_gui.grid):
            for j, tile in enumerate(row):
                painter.fillRect(tile.start_position[0], tile.start_position[1],
                                 tile.tile_width, tile.tile_height,
                                 QColor(tile.color[0], tile.color[1], tile.color[2], 255))
                tile_figure = self.chess_manager.board.figures.get_figure_at((i, j))
                self._draw_figure(tile_figure, tile.start_position, painter)

        self._draw_moves(painter)

    def _draw_figure(self, figure, tile_pos, painter):
        if figure:
            path = ResourcesContainer.inst.get_resource_path(figure.image_file)
            image = QImage(path)
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap.detach()
            point = QRect(tile_pos[0], tile_pos[1], self.tile_width, self.tile_height)
            painter.drawPixmap(point, pixmap)

    def _draw_moves(self, painter):
        if self.chess_manager.selected_tile:
            if self.chess_manager.board.possible_moves:
                moves_projected = self._tile_to_grid(x.position_to for x in self.chess_manager.board.possible_moves)
                self._draw_circles(moves_projected, painter)

    def _draw_circles(self, moves_projected, painter):
        prev_pen = painter.pen()
        painter.setPen(Qt.NoPen)
        brush = QBrush(QColor(0, 180, 100, 255), Qt.SolidPattern)
        for move in moves_projected:
            painter.setBrush(brush)
            x = move[0] + self.tile_width // 2
            y = self.height - move[1] - self.tile_height // 2
            painter.drawEllipse(QPoint(x, y), 15, 15)
        painter.setPen(prev_pen)

