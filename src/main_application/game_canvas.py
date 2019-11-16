from PyQt5.QtWidgets import QWidget
from axel import Event

from src.main_application.enums import GameMode


class GameCanvas(QWidget):
    def __init__(self, game_mode: GameMode):
        super().__init__()
        self.WIDTH = 600
        self.HEIGHT = 600
        self.on_update_tree = Event(self)
        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.setMaximumSize(self.WIDTH, self.HEIGHT)
        self.game_mode = game_mode

    def perform_player_move(self):
        if self.game_mode == GameMode.PLAYER_VS_PC:
            self.perform_algorithm_move()

    def perform_algorithm_move(self):
        pass
