import src.uct.algorithm.enums as Enums
import src.utils.random_utils as RandomUtils
from src.tictactoe.ttt_move import TicTacToeMove
from src.uct.game.base_game_state import BaseGameState


class TicTacToeState(BaseGameState):
    def __init__(self, board):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        positions = self.board.get_empty_positions()
        rc = [None] * len(positions)
        for i in range(len(positions)):
            pos = positions[i]
            move = TicTacToeMove(pos[0], pos[1])
            move.player = Enums.get_opponent(self.current_player)
            rc[i] = move
        return rc

    def perform_random_move(self):
        positions = self.board.get_empty_positions()
        random_pos_index = RandomUtils.get_random_int(0, len(positions))
        pos = positions[random_pos_index]
        self.switch_current_player()
        self.phase = self.board.perform_move(self.current_player, pos[0], pos[1])

    def deep_copy(self):
        rc = TicTacToeState(None)
        rc.phase = self.phase
        rc.current_player = self.current_player
        rc.board = self.board.deep_copy()
        return rc

    def apply_moves(self, moves):
        final_phase = self.phase
        for move in moves:
            final_phase = self.board.perform_move(move.player, move.x, move.y)
        self.phase = final_phase
