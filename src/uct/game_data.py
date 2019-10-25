from abc import ABC

from src.uct.enums import GamePhase


class GameData(ABC):
    def __init__(self):
        self.phase = GamePhase.IN_PROGRESS
        self.current_player = 1

    def get_all_possible_states(self):
        pass

    def random_move(self):
        pass

    def deep_copy(self):
        pass

    def switch_current_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
