import os

from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QImage, QBrush
from PyQt5.QtWidgets import QWidget
from axel import Event

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_game_manager import ChessGameManager
from src.main_application.enums import GameMode
from src.uct.algorithm.mc_game_manager import MonteCarloGameManager


class ChessCanvas(QWidget):
    def __init__(self, game_mode: GameMode):
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
        self.game_mode = game_mode
        self.on_update_tree = Event(self)

        self.painter = None

        game_state = ChessState(self.game_manager.board)
        self.monte_carlo_manager = MonteCarloGameManager(game_state)

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        self._draw_board(QPainter(self))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        x = event.x()
        y = event.y()
        self._react_to_player_click(x, y)

    def _react_to_player_click(self, x, y):
        grid_pos = self._grid_click_to_tile(x, y)
        player_moved, player_move = self.game_manager.react_to_tile_click(grid_pos)
        self.repaint()

        if self.game_mode == GameMode.PLAYER_VS_PC and player_moved:
            self.game_manager.deselect_last_moved()
            self.monte_carlo_manager.notify_move_performed(player_move)
            self._simulate_opponent_move()

    def _simulate_opponent_move(self):
        move = self.monte_carlo_manager.calculate_next_move(max_iterations=60, max_moves_per_simulation=10)
        print(f"Algorithm decided to go {move.position_from} -> {move.position_to} for player {move.player}")
        self.game_manager.deselect_king()
        self.game_manager.board.perform_legal_move(move)
        self.game_manager.reset_selected_tile()
        self.on_update_tree(self.monte_carlo_manager.tree.root)
        self.repaint()

    def _grid_click_to_tile(self, x, y):
        """
        :param pos: GUI order (x, y)
        :return: GUI order
        """
        if y == 0:
            y = 1
        return (x // self.TILE_WIDTH, (self.HEIGHT - y) // self.TILE_HEIGHT)[::-1]

    def _tile_to_grid(self, positions):
        """
        :param positions: matrix order (y, x)
        :return: returns GUI order
        """
        return [(x[1] * self.TILE_WIDTH, x[0] * self.TILE_HEIGHT) for x in positions]

    def _draw_board(self, painter):
        font = painter.font()
        font.setPixelSize(14)
        painter.setFont(font)
        pen = painter.pen()
        pen.setColor(QColor(255, 255, 255, 255))
        painter.setPen(pen)
        for i, row in enumerate(self.game_manager.board_gui.grid):
            for j, tile in enumerate(row):
                painter.fillRect(tile.start_position[0], tile.start_position[1],
                                 tile.tile_width, tile.tile_height,
                                 QColor(tile.color[0], tile.color[1], tile.color[2], 255))
                tile_figure = self.game_manager.board.figures.get_figure_at((i, j))
                tile_text = f"{(i, j)}"
                painter.drawText(tile.start_position[0], tile.start_position[1], 100, 100, 0, tile_text)
                self._draw_figure(tile_figure, tile.start_position, painter)

        self._draw_moves(painter)

    def _draw_figure(self, figure, tile_pos, painter):
        if figure:
            path = os.path.join(self.ICONS_FOLDER, figure.image_file)
            image = QImage(path)
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap.detach()
            point = QRect(tile_pos[0], tile_pos[1], self.TILE_WIDTH, self.TILE_HEIGHT)
            painter.drawPixmap(point, pixmap)

    def _draw_moves(self, painter):
        if self.game_manager.selected_tile:
            if self.game_manager.board.possible_moves:
                moves_projected = self._tile_to_grid(x.position_to for x in self.game_manager.board.possible_moves)
                self._draw_circles(moves_projected, painter)

    def _draw_circles(self, moves_projected, painter):
        prev_pen = painter.pen()
        painter.setPen(Qt.NoPen)
        brush = QBrush(QColor(0, 180, 100, 255), Qt.SolidPattern)
        for move in moves_projected:
            painter.setBrush(brush)
            x = move[0] + self.TILE_WIDTH // 2
            y = self.HEIGHT - move[1] - self.TILE_HEIGHT // 2
            painter.drawEllipse(QPoint(x, y), 15, 15)
        painter.setPen(prev_pen)
