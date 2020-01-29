from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from main_application.GUI_utils import get_button
from main_application.game_visualization_window import GameVisualizationWindow
from main_application.gui_settings import DisplaySettings
from main_application.mc_window_manager import MonteCarloWindowManager


class MachineVsMachineWindow(GameVisualizationWindow):
    """
    Class responsible for PC vs PC game window creation. It expands its parent by "Make next move" button,
    which allows user to push the play forward, because in this mode user cannot click on canvas to make moves by itself.
    """
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings):
        self.main_layout = QGridLayout()
        self.next_move_button = get_button("Make next move")
        self.next_move_button.clicked.connect(self.handle_next_move_button)
        super(MachineVsMachineWindow, self).__init__(parent, manager, display_settings, self.main_layout)
        self.game_layout.addWidget(self.next_move_button, 3, 0, alignment=QtCore.Qt.AlignCenter)

    def handle_next_move_button(self, sender):
        if not self.manager.canvas.game_ended:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.manager.perform_algorithm_move()
            QApplication.restoreOverrideCursor()
        if self.manager.canvas.game_ended:
            self.next_move_button.setEnabled(False)
