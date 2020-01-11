from PyQt5.QtWidgets import QMainWindow, QGridLayout
from PyQt5 import QtCore

from main_application.GUI_utils import get_button
from main_application.game_visualization_window import GameVisualizationWindow
from main_application.gui_settings import DisplaySettings
from main_application.mc_window_manager import MonteCarloWindowManager


class MachineVsMachineWindow(GameVisualizationWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings):
        self.main_layout = QGridLayout()
        self.next_move_button = get_button("Make next move")
        self.next_move_button.clicked.connect(self.handle_next_move_button)
        super(MachineVsMachineWindow, self).__init__(parent, manager, display_settings, self.main_layout)
        self.game_layout.addWidget(self.next_move_button, 3, 0, alignment=QtCore.Qt.AlignCenter)

    def handle_next_move_button(self, sender):
        if not self.manager.canvas.game_ended:
            self.manager.perform_algorithm_move()
        if self.manager.canvas.game_ended:
            self.next_move_button.setEnabled(False)