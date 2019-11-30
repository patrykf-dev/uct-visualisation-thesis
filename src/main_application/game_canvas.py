from PyQt5.QtWidgets import QWidget

from src.uct.game.base_game_move import BaseGameMove
from src.utils.CustomEvent import CustomEvent


class GameCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.WIDTH = 600
        self.HEIGHT = 600
        self.player_move_performed = CustomEvent()
        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.setMaximumSize(self.WIDTH, self.HEIGHT)

    # def perform_player_move(self):
    #     if self.game_mode == GameMode.PLAYER_VS_PC:
    #         self.perform_algorithm_move()

    def perform_algorithm_move(self, move: BaseGameMove):
        pass
