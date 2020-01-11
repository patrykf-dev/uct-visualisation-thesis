from PyQt5.QtWidgets import QMainWindow, QGridLayout

from main_application.game_window import GameWindow
from main_application.mc_window_manager import MonteCarloWindowManager


class PlayerVsPlayerWindow(GameWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager):
        self.main_layout = QGridLayout()
        super(PlayerVsPlayerWindow, self).__init__(parent, manager, self.main_layout)
