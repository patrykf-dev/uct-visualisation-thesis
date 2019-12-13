from PyQt5.QtWidgets import QMainWindow, QGridLayout

from src.main_application.GUI_utils import get_button
from src.main_application.game_visualization_window import GameVisualizationWindow
from src.main_application.gui_settings import DisplaySettings
from src.main_application.mc_window_manager import MonteCarloWindowManager


class MachineVsMachineWindow(GameVisualizationWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings):
        self.main_layout = QGridLayout()
        self.next_move_button = get_button("Make next move")
        self.next_move_button.clicked.connect(self.handle_next_move_button)
        super(MachineVsMachineWindow, self).__init__(parent, manager, display_settings, self.main_layout)
        self.main_layout.addWidget(self.next_move_button, 2, 0)

    def handle_next_move_button(self, sender):
        self.manager.perform_algorithm_move()
