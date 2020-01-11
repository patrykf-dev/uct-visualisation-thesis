from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox
from PyQt5 import QtCore

from main_application.GUI_utils import amend_window_position_on_screen, get_button, get_non_resizable_label, \
    LARGE_FONT_BOLD, show_dialog
from main_application.mc_window_manager import MonteCarloWindowManager
from uct.algorithm.enums import GamePhase
from utils.custom_event import CustomEvent


class GameWindow(QMainWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, main_layout: QGridLayout):
        super(GameWindow, self).__init__(parent)
        self.parent = parent
        self.manager = manager
        self.main_widget = QWidget()
        self._create_game_layout()
        main_layout.addWidget(self.game_widget, 1, 0, alignment=QtCore.Qt.AlignTop)
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)
        self.on_close_request = CustomEvent()

        self.manager.canvas.player_move_performed += self.change_game_status_label
        self.manager.on_update_tree += self.change_game_status_label

    def _create_game_layout(self):
        self.game_layout = QGridLayout()
        # self.game_layout.setContentsMargins(0, 20, 20, 20)
        self.game_layout.setSpacing(20)
        self.game_widget = QWidget()
        self.game_widget.setLayout(self.game_layout)
        self.start_over_button = get_button("Start over")
        self.start_over_button.clicked.connect(self._handle_start_over_button)
        self.game_status_label = get_non_resizable_label("Game in progress")
        self.game_layout.addWidget(self.manager.canvas, 0, 0)
        self.game_layout.addWidget(self.game_status_label, 1, 0, alignment=QtCore.Qt.AlignCenter)
        self.game_layout.addWidget(self.start_over_button, 2, 0, alignment=QtCore.Qt.AlignCenter)

    def _handle_start_over_button(self):
        answer = show_dialog("Do you want to restart the game?")
        if answer == QMessageBox.Ok:
            game_window_properties = {"game": self.manager.game, "game_mode": self.manager.game_mode,
                                      "settings": self.manager.mc_manager.settings, "display_settings": None}
            self.on_close_request.fire(self, earg=game_window_properties)
            self.close()

    def update_game_status_label(self, game_status):
        if game_status == GamePhase.IN_PROGRESS or self.game_status_label.text() != "Game in progress":
            return
        else:
            self.game_status_label.setFont(LARGE_FONT_BOLD)
            if game_status == GamePhase.PLAYER1_WON:
                label_text = "Player 1 WINS"
            elif game_status == GamePhase.PLAYER2_WON:
                label_text = "Player 2 WINS"
            elif game_status == GamePhase.DRAW:
                label_text = "DRAW"
        self.game_status_label.setText(label_text)

    def change_game_status_label(self, sender, move_info):
        self.update_game_status_label(move_info['phase'])

    def showEvent(self, event):
        super().showEvent(event)
        amend_window_position_on_screen(self)
