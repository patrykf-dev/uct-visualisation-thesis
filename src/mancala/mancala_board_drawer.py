import os
import random
from math import sqrt

from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QPainter, QImage, QColor, QFontMetrics, QBrush

from src.mancala.mancala_board import MancalaBoard


class MancalaBoardDrawer:
    """
    Class is responsible for mancala drawing: board, stones, holes and points.
    """
    def __init__(self, canvas_width, canvas_height):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.top_padding = 240
        self.left_padding = 37
        self.hole_padding = 10
        self.images_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.hole_radius = 25
        self.stone_radius = 4
        self.selected_hole_index = -1
        self.hole_centers = []
        self.stones_centers = []
        self.initial_draw = True
        self.store1_rectangle = None
        self.store2_rectangle = None

    def draw_board(self, painter: QPainter, board: MancalaBoard):
        """
        Draws board, stones, holes and points.
        :param painter: QPainter object from PyQt library that enables drawing e.g. rectangles
        :param board: MancalaBoard object with game data
        :return: None
        """
        self.fill_background(painter)
        self.draw_holes(painter)
        self.draw_stores(painter)
        self.draw_numbers(painter, board)

        self.draw_stones(painter, board)

        if self.initial_draw:
            self.initial_draw = False

    def fill_background(self, painter: QPainter):
        """
        Fills game area background with gray color (160, 160, 160).
        :param painter: QPainter object
        :return: None
        """
        background = QRect(0, 0, self.canvas_width, self.canvas_height)
        painter.fillRect(background, QColor(160, 160, 160))

    def draw_holes(self, painter: QPainter):
        """
        Draws holes using png images.
        :param painter: QPainter object
        :return: None
        """
        pixmap = QtGui.QPixmap.fromImage(QImage(os.path.join(self.images_folder, "hole.png")))
        pixmap_selected = QtGui.QPixmap.fromImage(QImage(os.path.join(self.images_folder, "hole_selected.png")))
        pixmap.detach()
        pixmap_selected.detach()
        start_x = 3 * self.hole_radius + self.hole_padding + self.left_padding
        x = start_x
        y = self.top_padding + 3 * self.hole_radius
        for i in range(12):
            if self.initial_draw:
                self.hole_centers.append((x + self.hole_radius, y + self.hole_radius))

            point = QRect(x, y, self.hole_radius * 2, self.hole_radius * 2)
            if i == self.selected_hole_index:
                painter.drawPixmap(point, pixmap_selected)
            else:
                painter.drawPixmap(point, pixmap)

            x += 2 * self.hole_radius + self.hole_padding
            if i == 5:
                x = start_x
                y = self.top_padding

    def draw_stores(self, painter: QPainter):
        """
        Draws stores (hole-bases) using png image.
        :param painter: QPainter object
        :return: None
        """
        path = os.path.join(self.images_folder, "store.png")
        image = QImage(path)
        pixmap = QtGui.QPixmap.fromImage(image)
        pixmap.detach()
        stores_x = self.left_padding
        stores_y = self.top_padding
        self.store1_rectangle = QRect(stores_x, stores_y, self.hole_radius * 3, self.hole_radius * 5)
        painter.drawPixmap(self.store1_rectangle, pixmap)
        self.store2_rectangle = QRect(15 * self.hole_radius + 7 * self.hole_padding + stores_x, stores_y,
                      self.hole_radius * 3, self.hole_radius * 5)
        painter.drawPixmap(self.store2_rectangle, pixmap)

    def draw_numbers(self, painter: QPainter, board: MancalaBoard):
        """
        Draws numbers representing points/stones in each hole.
        :param painter: QPainter object
        :param board: MancalaBoard object
        :return: None
        """
        font = painter.font()
        font.setPixelSize(30)
        font.setFamily("Consolas")
        font_height = QFontMetrics(font).height()
        painter.setFont(font)
        pen = painter.pen()
        pen.setColor(QColor(0, 0, 0, 255))
        painter.setPen(pen)
        start_x = 3 * self.hole_radius + self.hole_padding

        x = start_x + self.left_padding
        y = self.top_padding + 5 * self.hole_radius
        for i in range(6):
            self._draw_number(board.board_values[i], 2 * self.hole_radius, font_height, painter, x, y)
            x += 2 * self.hole_radius + self.hole_padding

        x = start_x + 12 * self.hole_radius + 6 * self.hole_padding + self.left_padding
        self._draw_number(board.board_values[6], 3 * self.hole_radius, font_height, painter, x, y)

        x = start_x + 10 * self.hole_radius + 5 * self.hole_padding + self.left_padding
        y = self.top_padding - font_height
        for i in range(6):
            self._draw_number(board.board_values[i + 7], 2 * self.hole_radius, font_height, painter, x, y)
            x -= 2 * self.hole_radius + self.hole_padding

        x = start_x - self.hole_radius * 3 - self.hole_padding + self.left_padding
        self._draw_number(board.board_values[13], 3 * self.hole_radius, font_height, painter, x, y)

    def _draw_number(self, value, font_width, font_height, painter, x, y):
        number = str(value)
        number_place = QRect(x, y, font_width, font_height)
        painter.drawText(number_place, Qt.AlignCenter | Qt.AlignTop, number)

    def detect_click(self, x, y):
        """
        Given x, y coordinates tells if
        :param x: x-coordinate of the game area
        :param y: y-coordinate of the game area
        :return: tuple of 2 values: bool informing if the coordinates correspond to a currently moving player's hole and
                 index of selected hole (-1 if no hole was selected)
        """
        for i in range(len(self.hole_centers)):
            x_dist = x - self.hole_centers[i][0]
            y_dist = y - self.hole_centers[i][1]
            if sqrt(x_dist * x_dist + y_dist * y_dist) <= self.hole_radius:
                if self.selected_hole_index == i:
                    self.selected_hole_index = -1
                    self.stones_centers = []
                    return True, self.draw_index_to_board_index(i)
                else:
                    self.selected_hole_index = i
                    return False, -1
        self.selected_hole_index = -1
        return False, -1

    def draw_index_to_board_index(self, i):
        """
        Transforms drawing index to board index.
        :param i: given hole drawing index
        :return: hole board index
        """
        if i < 6:
            return i
        else:
            return 18 - i

    def generate_stones_centers(self, board: MancalaBoard):
        """
        Generates stones' position inside holes. Stores list of values in 'stones_centers' variable.
        :param board: MancalaBoard object
        :return: None
        """
        max_span = self.hole_radius - self.stone_radius - 2

        for i in range(len(self.hole_centers)):
            board_index = self.draw_index_to_board_index(i)
            for j in range(board.board_values[board_index]):
                hole_x = self.hole_centers[i][0]
                hole_y = self.hole_centers[i][1]
                x_diff = random.uniform(-max_span, max_span)
                max_y = int(sqrt(abs(max_span * max_span - x_diff * x_diff)))
                y_diff = random.uniform(-max_y, max_y)
                x = hole_x + x_diff
                y = hole_y + y_diff
                self.stones_centers.append((x, y))

    def generate_store_stones_centers(self, board: MancalaBoard):
        """
        Generates stones' position inside stores. Stores list of values in 'stones_centers' variable.
        :param board: MancalaBoard object
        :return: None
        """
        padding = 20
        store = self.store2_rectangle
        for i in range(board.board_values[6]):
            random_x = random.uniform(store.left() + padding, store.right() - padding)
            random_y = random.uniform(store.top() + padding, store.bottom() - padding)
            self.stones_centers.append((random_x, random_y))
        store = self.store1_rectangle
        for i in range(board.board_values[13]):
            random_x = random.uniform(store.left() + padding, store.right() - padding)
            random_y = random.uniform(store.top() + padding, store.bottom() - padding)
            self.stones_centers.append((random_x, random_y))

    def draw_stones(self, painter, board: MancalaBoard):
        """
        Draws small green stones on the board.
        :param painter: QPainter object
        :param board: MancalaBoard object
        :return: None
        """
        if len(self.stones_centers) == 0:
            self.generate_stones_centers(board)
            self.generate_store_stones_centers(board)

        brush = QBrush(QColor(0, 180, 100, 150), Qt.SolidPattern)
        painter.setBrush(brush)
        painter.setRenderHint(QPainter.Antialiasing, True)
        for center in self.stones_centers:
            painter.drawEllipse(QPoint(*center), self.stone_radius * 2, self.stone_radius * 2)
