import os
import re
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from src.main_application.GUI_utils import TREES_PATH, center_window_on_screen, show_eror_dialog
from src.main_application.game_window_creator import create_proper_window
from src.main_application.main_application_window_layout import MainApplicationWindowLayout
from src.main_application.mc_tree_window import MonteCarloTreeWindow
from src.main_application.sequence_utils import MonteCarloNodeSequenceInfo
from src.serialization.serializator_binary import BinarySerializator
from src.serialization.serializator_csv import CsvSerializator


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
        self.layout.select_tree_path_button.clicked.connect(self._handle_select_tree_path_button)
        self.layout.draw_opengl_button.clicked.connect(self._handle_opengl_button)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)

    def _handle_play_button(self):
        """
        Handler for button, that initiates the game.
        It displays the game and visualization window.
        """
        game = self.layout.get_chosen_game()
        game_mode = self.layout.get_chosen_game_mode()
        ms_settings, display_settings = self.layout.get_settings()
        if ms_settings is None or display_settings is None:
            return

        validation_string = ms_settings.validate()
        if validation_string != "":
            show_eror_dialog(validation_string)
            return

        window = create_proper_window(self, game, game_mode, ms_settings, display_settings)
        window.on_close_request += self._handle_close_request
        window.show()

    def _handle_close_request(self, sender, earg):
        window = create_proper_window(self, earg["game"], earg["game_mode"], earg["settings"], earg["display_settings"])
        window.on_close_request += self._handle_close_request
        window.show()

    def _handle_select_tree_path_button(self):
        """
        Handles button that enables user to load his own trees from file system.
        When one file is chosen, its name will appear in the edit line.
        When multiple files were chosen, the user will see "Multiple files chosen" in the edit line.
        """
        paths, _ = QFileDialog.getOpenFileNames(self, "Open a tree file", TREES_PATH,
                                                "Csv files (*.csv) | Tree files (*.tree)")
        if len(paths) == 1:
            self.layout.tree_path_edit.setText(paths[0])
        elif len(paths) > 1:
            self.layout.tree_path_edit.setText("Multiple files chosen")
        if paths:
            self.layout.chosen_trees_paths = paths

    def _handle_opengl_button(self):
        """
        Displays the window with a UCT tree visualization.
        """
        trees_info = self._get_trees_from_given_path()
        window = MonteCarloTreeWindow(self, trees_info=trees_info)
        window.show()

    def _retrieve_filename_from_path(self, path):
        split_strings = re.split('/', path)
        final_split_strings = []
        for split_string in split_strings:
            final_split_strings.extend(re.split(r'\\', split_string))
        return final_split_strings[-1]

    def _get_trees_from_given_path(self):
        """
        Runs serializer to parse the trees from the given files.
        Returns list of MonteCarloNodeSequenceInfo objects - contains: root node, filename
        """
        trees_info = []
        if self.layout.chosen_trees_paths[0].endswith(".csv"):
            serializator = CsvSerializator()
        else:
            serializator = BinarySerializator()
        counter = 0
        for tree_path in self.layout.chosen_trees_paths:
            print(counter)
            counter += 1
            tree = serializator.get_node_from_path(tree_path)
            filename = self._retrieve_filename_from_path(tree_path)
            trees_info.append(MonteCarloNodeSequenceInfo(tree, filename))
        return trees_info


def launch_application():
    """
    Main program function.
    Shows menu window.
    """
    redefine_exceptions()
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplicationWindow()
    window.show()
    sys.exit(app.exec_())


def redefine_exceptions():
    """
    Catches critical exceptions and displays them in message box.
    """

    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "An exception was raised",
                                       f"Exception info: [{t}] [{val}] [{tb}]")
        old_hook(t, val, tb)

    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions


if __name__ == '__main__':
    launch_application()
