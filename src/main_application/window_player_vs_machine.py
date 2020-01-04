from src.main_application.game_visualization_window import GameVisualizationWindow
from PyQt5.QtWidgets import QMainWindow, QGridLayout

from src.main_application.gui_settings import DisplaySettings
from src.main_application.mc_window_manager import MonteCarloWindowManager


class PlayerVsMachineWindow(GameVisualizationWindow):
    """
    Class responsible for player vs PC game window creation.
    """

    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, display_settings: DisplaySettings):
        self.main_layout = QGridLayout()
        super(PlayerVsMachineWindow, self).__init__(parent, manager, display_settings, self.main_layout)
