from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_canvas import ChessCanvas
from src.main_application.GUI_utils import center_window_on_screen, get_button, get_non_resizable_label, \
    LARGE_FONT_BOLD, show_dialog
from src.main_application.enums import Game
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.uct.algorithm.enums import GamePhase
from src.utils.custom_event import CustomEvent


class GameWindow(QMainWindow):
    def __init__(self, parent: QMainWindow, manager: MonteCarloWindowManager, main_layout: QGridLayout):
        super(GameWindow, self).__init__(parent)
        self.parent = parent
        self.manager = manager
        self.main_widget = QWidget()
        self._create_game_layout()
        main_layout.addWidget(self.game_widget, 0, 0, 2, 1)
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)
        self.on_close_request = CustomEvent()

        self.manager.canvas.player_move_performed += self.change_game_status_label
        self.manager.on_update_tree += self.change_game_status_label

    def _create_game_layout(self):
        game_layout = QGridLayout()
        self.game_widget = QWidget()
        self.game_widget.setLayout(game_layout)
        self.start_over_button = get_button("Start over")
        self.start_over_button.clicked.connect(self._handle_start_over_button)
        self.game_status_label = get_non_resizable_label("Game in progress")
        game_layout.addWidget(self.manager.canvas, 0, 0)
        game_layout.addWidget(self.game_status_label, 1, 0)
        game_layout.addWidget(self.start_over_button, 2, 0)

    def _handle_start_over_button(self):
        answer = show_dialog("Do you want to restart the game?")
        if answer == QMessageBox.Ok:
            game_window_properties = {"game": self.manager.game, "game_mode": self.manager.game_mode,
                                      "settings": self.manager.mc_manager.settings, "display_settings": None}
            self.on_close_request.fire(self, earg=game_window_properties)
            self.close()

    def update_game_status_label(self, game_status):
        if game_status == GamePhase.IN_PROGRESS:
            label_text = "Game in progress"
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
        center_window_on_screen(self)
