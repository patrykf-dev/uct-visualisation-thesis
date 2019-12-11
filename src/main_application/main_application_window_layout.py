import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout

from src.main_application.GUI_utils import get_non_resizable_label, get_radiobutton, get_button, \
    get_line_edit, get_hint_line_edit, TREES_PATH, get_checkbox, gray_out_radiobutton_text, show_eror_dialog, get_box_background_stylesheet
from src.main_application.enums import GameMode, Game
from src.main_application.gui_settings import MonteCarloSettings, DisplaySettings


class MainApplicationWindowLayout:
    def __init__(self):
        self.main_widget = QWidget()
        self.play_button = get_button("Play", 80, 30)
        self.draw_opengl_button = get_button("Inspect tree")
        self.tree_path_edit = get_hint_line_edit(os.path.join(TREES_PATH, "example_tree_05.csv"))
        self.chosen_trees_paths = [os.path.join(TREES_PATH, "example_tree_05.csv")]
        self.select_tree_path_button = get_button("Select")
        self.chess_button = get_radiobutton("Chess")
        self.mancala_button = get_radiobutton("Mancala")
        self.player_vs_player_button = get_radiobutton("Player vs player")
        self.player_vs_pc_button = get_radiobutton("Player vs PC")
        self.pc_vs_pc_button = get_radiobutton("PC vs PC")
        self.limit_moves_check = get_checkbox("Limit moves in playouts")
        self.player_vs_player_button = get_radiobutton("Player vs player")
        self.player_vs_pc_button = get_radiobutton("Player vs PC")
        self.max_iterations_edit = get_line_edit()
        self.max_time_edit = get_line_edit()
        self.max_moves_edit = get_line_edit()
        self.max_iterations_button = get_radiobutton("Max iterations before move")
        self.max_time_button = get_radiobutton("Max time for move (ms)")
        self.animate_check = get_checkbox("Animate tree growth")
        self._create_layout()
        self._set_events()
        self._load_defaults()

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

    def get_settings(self) -> (MonteCarloSettings, DisplaySettings):
        mc_settings = MonteCarloSettings()
        mc_settings.limit_moves = self.limit_moves_check.isChecked()
        mc_settings.limit_iterations = self.max_iterations_button.isChecked()
        try:
            mc_settings.max_iterations = int(self.max_iterations_edit.text())
            mc_settings.max_time = int(self.max_time_edit.text())
            mc_settings.max_moves_per_iteration = int(self.max_moves_edit.text())
        except ValueError:
            show_eror_dialog("Non numeric values passed.")
            return None

        display_settings = DisplaySettings()
        display_settings.animate = self.animate_check.isChecked()
        return mc_settings, display_settings

    def _set_events(self):
        self.limit_moves_check.toggled.connect(self._react_to_moves_limit_click)
        self.max_iterations_button.toggled.connect(self._react_to_limit_button_click)
        self.max_time_button.toggled.connect(self._react_to_limit_button_click)
        self.animate_check.toggled.connect(self._react_to_animate_button_click)

    def _load_defaults(self):
        self.mancala_button.setChecked(True)
        self.player_vs_pc_button.setChecked(True)

        settings = MonteCarloSettings()
        self.limit_moves_check.setChecked(settings.limit_moves)
        self.max_iterations_edit.setText(str(settings.max_iterations))
        self.max_time_edit.setText(str(settings.max_time))
        self.max_moves_edit.setText(str(settings.max_moves_per_iteration))
        self.max_iterations_button.setChecked(settings.limit_iterations)
        self.max_time_button.setChecked(not settings.limit_iterations)

    def _create_layout(self):
        main_layout = QGridLayout()
        self.main_widget.setLayout(main_layout)
        main_layout.addWidget(self._get_first_row(), 0, 0)
        main_layout.addWidget(self._get_second_row(), 1, 0)

    def _get_first_row(self):
        rc = QWidget()
        main_layout = QGridLayout()
        rc.setObjectName("box")
        rc.setStyleSheet(get_box_background_stylesheet())
        rc.setLayout(main_layout)

        self._add_left_panel(main_layout)
        self._add_right_panel(main_layout)
        self._add_uct_panel(main_layout)
        self._add_display_settings_panel(main_layout)
        main_layout.addWidget(self.play_button, 3, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        return rc

    def _get_second_row(self):
        rc = QWidget()
        main_layout = QGridLayout()
        rc.setObjectName("box")
        rc.setStyleSheet(get_box_background_stylesheet())
        rc.setLayout(main_layout)
        main_layout.addWidget(self.tree_path_edit, 0, 0)
        main_layout.addWidget(self.select_tree_path_button, 0, 1)
        main_layout.addWidget(self.draw_opengl_button, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        return rc

    def _add_left_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("Game"), 0, 0)
        layout.addWidget(self.chess_button, 1, 0)
        layout.addWidget(self.mancala_button, 2, 0)
        main_layout.addWidget(new_widget, 0, 0, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def _add_right_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("Mode"), 0, 0)
        layout.addWidget(self.player_vs_player_button, 1, 0)
        layout.addWidget(self.player_vs_pc_button, 2, 0)
        layout.addWidget(self.pc_vs_pc_button, 3, 0)
        main_layout.addWidget(new_widget, 0, 1, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def _add_uct_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("UCT parameters"), 0, 0)
        layout.addWidget(self.max_iterations_button, 1, 0)
        layout.addWidget(self.max_time_button, 2, 0)
        layout.addWidget(self.limit_moves_check, 3, 0, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.max_iterations_edit, 1, 1)
        layout.addWidget(self.max_time_edit, 2, 1)
        layout.addWidget(self.max_moves_edit, 3, 1)
        main_layout.addWidget(new_widget, 1, 0, 1, 2)

    def _add_display_settings_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(get_non_resizable_label("Display settings"), 0, 0, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(self.animate_check, 1, 0, alignment=QtCore.Qt.AlignLeft)
        main_layout.addWidget(new_widget, 2, 0, 1, 2)

    def _react_to_moves_limit_click(self):
        if self.limit_moves_check.isChecked():
            self.max_moves_edit.setEnabled(True)
        else:
            self.max_moves_edit.setEnabled(False)

    def _react_to_limit_button_click(self):
        if self.max_iterations_button.isChecked():
            self.max_iterations_edit.setEnabled(True)
            self.max_time_edit.setEnabled(False)
            gray_out_radiobutton_text(self.max_time_button, True)
            gray_out_radiobutton_text(self.max_iterations_button, False)
            self._add_warning_to_animation_check(False)
        else:
            self.max_iterations_edit.setEnabled(False)
            self.max_time_edit.setEnabled(True)
            gray_out_radiobutton_text(self.max_time_button, False)
            gray_out_radiobutton_text(self.max_iterations_button, True)
            self._add_warning_to_animation_check(self.animate_check.isChecked())

    def _react_to_animate_button_click(self):
        if self.max_time_button.isChecked() and self.animate_check.isChecked():
            self._add_warning_to_animation_check(True)
        else:
            self._add_warning_to_animation_check(False)

    def _add_warning_to_animation_check(self, warning):
        if warning:
            self.animate_check.setText("Animate tree growth (reducing algorithm's performance)")
        else:
            self.animate_check.setText("Animate tree growth")
