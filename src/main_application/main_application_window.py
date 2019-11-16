import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog

import src.main_application.easy_plot_tree as MatplotlibDrawer
from src.main_application.GUI_utils import TREES_PATH, center_window_on_screen
from src.main_application.enums import GameMode, Game
from src.main_application.game_window_creator import create_proper_window
from src.main_application.main_application_window_layout import MainApplicationWindowLayout
from src.serialization.serializator_csv import CsvSerializator
from src.visualisation_algorithm.walkers_algorithm import ImprovedWalkersAlgorithm
from src.visualisation_algorithm_new.walkers_algorithm_new import ImprovedWalkersAlgorithmNew
from src.visualisation_drawing.mc_tree_window import MonteCarloTreeWindow


class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        self.setMinimumWidth(500)
        self.layout = MainApplicationWindowLayout()
        self.setCentralWidget(self.layout.main_widget)
        self.layout.play_button.clicked.connect(self._handle_play_button)
        self.layout.select_tree_path_button.clicked.connect(self._handle_select_tree_path_button)
        self.layout.draw_matplotlib_button.clicked.connect(self._handle_matplotlib_button)
        self.layout.draw_matplotlib_test_button.clicked.connect(self._handle_matplotlib_test_button)
        self.layout.draw_opengl_button.clicked.connect(self._handle_opengl_button)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)

    def _handle_play_button(self):
        game = self.layout.get_chosen_game()
        game_mode = self.layout.get_chosen_game_mode()
        print(f"_handle_play_button {game_mode}")
        w = create_proper_window(self, game, game_mode)
        w.show()

    def _handle_select_tree_path_button(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open csv tree file", TREES_PATH, "Csv files (*.csv)")
        path = self.layout.tree_path_edit.setText(path)
        return path

    def _handle_matplotlib_button(self):
        root = self._get_tree_from_given_path()
        alg = ImprovedWalkersAlgorithm()
        alg.buchheim_algorithm(root)
        MatplotlibDrawer.draw_tree(root)

    def _handle_matplotlib_test_button(self):
        root = self._get_tree_from_given_path()
        alg_new = ImprovedWalkersAlgorithmNew()
        alg_new.buchheim_algorithm(root)
        MatplotlibDrawer.draw_tree(root)

    def _handle_opengl_button(self):
        root = self._get_tree_from_given_path()
        window = MonteCarloTreeWindow(self)
        window.canvas_widget.layout.canvas.use_root_data(root)
        window.show()

    def _get_tree_from_given_path(self):
        path = self.layout.tree_path_edit.text()
        serializator = CsvSerializator()
        root = serializator.get_node_from_path(path)
        return root


def launch_application():
    redefine_exceptions()
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplicationWindow()
    window.show()
    sys.exit(app.exec_())


def redefine_exceptions():
    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "An exception was raised",
                                       f"Exception info: [{t}] [{val}] [{tb}]")
        old_hook(t, val, tb)

    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions


if __name__ == '__main__':
    launch_application()
