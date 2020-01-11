import abc

from uct.algorithm.enums import GamePhase


class BaseGameState(abc.ABC):
    def __init__(self):
        self.phase = GamePhase.IN_PROGRESS
        self.current_player = 1

    @abc.abstractmethod
    def get_all_possible_moves(self):
        pass

    @abc.abstractmethod
    def perform_random_move(self):
        pass

    @abc.abstractmethod
    def apply_moves(self, moves):
        pass

    @abc.abstractmethod
    def get_win_score(self, player):
        pass

    @abc.abstractmethod
    def deep_copy(self):
        pass

    @abc.abstractmethod
    def generate_description(self):
        pass

    def switch_current_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
