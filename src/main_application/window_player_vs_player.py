from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen
from src.main_application.mc_window_manager import MonteCarloWindowManager


class PlayerVsPlayerWindow(QMainWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager):
        super(PlayerVsPlayerWindow, self).__init__(parent)
        self.manager = manager
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.manager.canvas)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
