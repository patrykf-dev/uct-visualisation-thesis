from itertools import chain
from random import randint
from copy import deepcopy

from src.uct.game.base_game_state import BaseGameState


class ChessState(BaseGameState):
    def __init__(self, board):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        all_possible_moves = []
        for figure in self.board.figures:
            if figure.color != self.board.move_color:
                continue
            possible_moves = figure.check_moves(self.board.figures)
            possible_moves_reduced = self.board.reduce_move_range_when_check(figure, possible_moves)
            if possible_moves_reduced:
                all_possible_moves.append(possible_moves_reduced)
        return list(chain.from_iterable(all_possible_moves))

    def perform_random_move(self):
        all_possible_moves = self.get_all_possible_moves()
        random_number = randint(0, len(all_possible_moves) - 1)
        return all_possible_moves[random_number]

    def deep_copy(self):
        return deepcopy(self.board)

    def apply_moves(self, moves):
        pass
