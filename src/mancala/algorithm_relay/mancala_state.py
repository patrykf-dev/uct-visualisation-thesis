import src.utils.random_utils as RandomUtils
from src.mancala.mancala_board import MancalaBoard
from src.uct.algorithm.enums import GamePhase
from src.uct.game.base_game_state import BaseGameState


class MancalaState(BaseGameState):
    def __init__(self, board: MancalaBoard):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        return self.board.find_all_moves()

    def perform_random_move(self):
        all_possible_moves = self.get_all_possible_moves()
        random_number = RandomUtils.get_random_int(0, len(all_possible_moves))
        move = all_possible_moves[random_number]
        self.board.perform_move(move)
        self.switch_current_player()
        self.phase = self.board.phase

    def apply_moves(self, moves):
        for move in moves:
            self.board.perform_move(move)
        self.phase = self.board.phase

    def get_win_score(self, player):
        max_score_diff = 48
        diff = self.board.get_win_score(player)
        return diff / max_score_diff

    def deep_copy(self):
        new_board = self.board.deep_copy()
        rc = MancalaState(new_board)
        rc.phase = self.phase
        rc.current_player = self.board.current_player
        return rc

    def generate_description(self):
        status = str(self.phase).split(".")[1]
        return f"{status}, player1 value: {self.board.get_win_score(1)}, player2 value: {self.board.get_win_score(2)}"
