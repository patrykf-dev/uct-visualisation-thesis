import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from main_application.GUI_utils import TREES_PATH, amend_window_position_on_screen, show_eror_dialog
from main_application.game_window_creator import create_proper_window
from main_application.main_application_window_layout import MainApplicationWindowLayout
from main_application.mc_tree_window import MonteCarloTreeWindow
from main_application.utils import extract_serializable_files_from


class MainApplicationWindow(QMainWindow):
    """
    CLass is responsible for displaying the main window of the application.
    """

    def __init__(self):
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        self.setMinimumWidth(500)
        self.setWindowTitle('UCT Visualizer')
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "tree_icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.layout = MainApplicationWindowLayout()
        self.setCentralWidget(self.layout.main_widget)
        self.layout.play_button.clicked.connect(self._handle_play_button)
        self.layout.select_tree_path_button_files.clicked.connect(self._handle_select_tree_path_button_files)
        self.layout.select_tree_path_button_directories.clicked.connect(self._handle_select_tree_path_button_directories)
        self.layout.draw_opengl_button.clicked.connect(self._handle_opengl_button)

    def showEvent(self, event):
        super().showEvent(event)
        amend_window_position_on_screen(self)

    def _handle_play_button(self):
        """
        Handler for button, that initiates the game.
        It displays the game and visualization window.
        """
        game = self.layout.get_chosen_game()
        game_mode = self.layout.get_chosen_game_mode()
        mc_settings, display_settings = self.layout.get_settings()
        if mc_settings is None or display_settings is None:
            return

        validation_string = mc_settings.validate()
        if validation_string != "":
            show_eror_dialog(validation_string)
            return

        window = create_proper_window(self, game, game_mode, mc_settings, display_settings)
        window.on_close_request += self._handle_close_request
        window.show()

    def _handle_close_request(self, sender, earg):
        window = create_proper_window(self, earg["game"], earg["game_mode"], earg["settings"], earg["display_settings"])
        window.on_close_request += self._handle_close_request
        window.show()

    def _handle_select_tree_path_button_files(self):
        """
        Handles button that enables user to load his own trees from file system.
        When one file is chosen, its name will appear in the edit line.
        When multiple files were chosen, the user will see "Multiple files chosen" in the edit line.
        """
        paths, _ = QFileDialog.getOpenFileNames(self, "Open a tree file", TREES_PATH,
                                                "Tree files (*.csv *.tree)")
        if len(paths) == 1:
            self.layout.tree_path_edit.setText(paths[0])
        elif len(paths) > 1:
            self.layout.tree_path_edit.setText(f"Files chosen: {len(paths)}")
        if paths:
            self.layout.chosen_trees_paths = paths

    def _handle_select_tree_path_button_directories(self):
        """
        Handles button that enables user to load his own trees from file system.
        All trees from the selected directory (non recursively) will be loaded to the application.
        User can choose a directory, and its path will be shown on the textfield.
        """
        path = QFileDialog.getExistingDirectory(self, "Open a directory with tree files", TREES_PATH, QFileDialog.ShowDirsOnly)
        if not path:
            return
        files = extract_serializable_files_from(path)
        if len(files) == 0:
            show_eror_dialog(f"No tree files found inside {path}")
            return
        paths = list(map(lambda filename: os.path.join(path, filename), files))

        self.layout.tree_path_edit.setText(path)
        self.layout.chosen_trees_paths = paths

    def _handle_opengl_button(self):
        """
        Displays the window with a UCT tree visualization.
        """
        if not self.layout.chosen_trees_paths:
            show_eror_dialog(f"Please choose a valid path!")
            return
        _, display_settings = self.layout.get_settings()
        window = MonteCarloTreeWindow(self, display_settings=display_settings,
                                      trees_paths=self.layout.chosen_trees_paths)
        window.show()
