from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen, get_button, get_non_resizable_label
from src.main_application.mc_window_manager import MonteCarloWindowManager


class GameWindow(QMainWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, main_layout: QGridLayout):
        super(GameWindow, self).__init__(parent)
        self.manager = manager
        self.main_widget = QWidget()
        self._create_game_layout()
        main_layout.addWidget(self.game_widget, 0, 0, 2, 1)
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)

    def _create_game_layout(self):
        game_layout = QGridLayout()
        self.game_widget = QWidget()
        self.game_widget.setLayout(game_layout)
        self.start_over_button = get_button("Start over")
        self.start_over_button.clicked.connect(self.handle_start_over_button)
        self.game_status_label = get_non_resizable_label("Game status: ")
        game_layout.addWidget(self.manager.canvas, 0, 0)
        game_layout.addWidget(self.game_status_label, 1, 0)
        game_layout.addWidget(self.start_over_button, 2, 0)

    def handle_start_over_button(self):
        print("Starting over")

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
