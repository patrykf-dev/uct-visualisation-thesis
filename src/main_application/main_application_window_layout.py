import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit

from src.main_application.GUI_utils import get_non_resizable_label, get_radiobutton, get_button, \
    get_line_edit, get_hint_line_edit, TREES_PATH
from src.main_application.enums import GameMode, Game


class MainApplicationWindowLayout:
    def __init__(self):
        self.main_widget = None
        self.play_button = QPushButton()
        self.draw_opengl_button = QPushButton()
        self.draw_matplotlib_button = QPushButton()
        self.tree_path_edit = QLineEdit()
        self.select_tree_path_button = QPushButton()
        self._create_layout()

    def get_chosen_game(self):
        if self.mancala_button.isChecked():
            return Game.Mancala
        else:
            return Game.Chess

    def get_chosen_game_mode(self):
        if self.pc_vs_pc_button.isChecked():
            return GameMode.PC_VS_PC
        elif self.player_vs_player_button.isChecked():
            return GameMode.PLAYER_VS_PLAYER
        elif self.player_vs_pc_button.isChecked():
            return GameMode.PLAYER_VS_PC
        else:
            return GameMode.PLAYER_VS_PC

    def _create_layout(self):
        self.main_widget = QWidget()
        main_layout = QGridLayout()
        self.main_widget.setLayout(main_layout)
        main_layout.addWidget(self._get_first_row(), 0, 0)
        main_layout.addWidget(self._get_second_row(), 1, 0)

    def _get_first_row(self):
        rc = QWidget()
        main_layout = QGridLayout()
        rc.setObjectName("box")
        rc.setStyleSheet(
            "QWidget#box{background-color: rgb(160, 160, 160); margin:2px; border:2px solid rgb(0, 0, 0);}")
        rc.setLayout(main_layout)

        self._add_left_panel(main_layout)
        self._add_right_panel(main_layout)
        self._add_uct_panel(main_layout)
        self.play_button = get_button("Play", 80, 30)
        main_layout.addWidget(self.play_button, 2, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        return rc

    def _get_second_row(self):
        rc = QWidget()
        main_layout = QGridLayout()
        rc.setObjectName("box")
        rc.setStyleSheet(
            "QWidget#box{background-color: rgb(160, 160, 160); margin:2px; border:2px solid rgb(0, 0, 0);}")
        rc.setLayout(main_layout)
        big_tree_path = os.path.join(TREES_PATH, "example_tree_05.csv")
        self.tree_path_edit = get_hint_line_edit(big_tree_path)
        main_layout.addWidget(self.tree_path_edit, 0, 0)
        self.select_tree_path_button = get_button("Select")
        main_layout.addWidget(self.select_tree_path_button, 0, 1)
        self.draw_opengl_button = get_button("Inspect tree (OpenGL)")
        self.draw_matplotlib_button = get_button("Inspect tree (matplotlib) - old")
        self.draw_matplotlib_test_button = get_button("Inspect tree (matplotlib) - dev")
        main_layout.addWidget(self.draw_opengl_button, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.draw_matplotlib_button, 2, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.draw_matplotlib_test_button, 3, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        return rc

    def _add_left_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("Game"), 0, 0)
        self.chess_button = get_radiobutton("Chess")
        self.chess_button.setChecked(True)
        layout.addWidget(self.chess_button, 1, 0)
        self.mancala_button = get_radiobutton("Mancala")
        layout.addWidget(self.mancala_button, 2, 0)
        main_layout.addWidget(new_widget, 0, 0, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def _add_right_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("Mode"), 0, 0)
        self.player_vs_player_button = get_radiobutton("Player vs player")
        self.player_vs_pc_button = get_radiobutton("Player vs PC")
        self.pc_vs_pc_button = get_radiobutton("PC vs PC")
        self.player_vs_pc_button.setChecked(True)
        layout.addWidget(self.player_vs_player_button, 1, 0)
        layout.addWidget(self.player_vs_pc_button, 2, 0)
        layout.addWidget(self.pc_vs_pc_button, 3, 0)
        main_layout.addWidget(new_widget, 0, 1, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def _add_uct_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("UCT parameters"), 0, 0)
        layout.addWidget(get_non_resizable_label("Iterations before move"), 1, 0)
        layout.addWidget(get_non_resizable_label("Max time for move"), 2, 0)
        layout.addWidget(get_line_edit(), 1, 1)
        layout.addWidget(get_line_edit(), 2, 1)
        main_layout.addWidget(new_widget, 1, 0, 1, 2)
