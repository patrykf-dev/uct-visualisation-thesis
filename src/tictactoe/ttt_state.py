import src.uct.random_utils as RandomUtils
from src.uct.base_game_state import BaseGameState
from src.tictactoe.ttt_move import TicTacToeMove
import src.uct.enums as Enums


class TicTacToeState(BaseGameState):
    def __init__(self, board):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        positions = self.board.get_empty_positions()
        rc = []
        for position in positions:
            move = TicTacToeMove(position[0], position[1])
            move.player = Enums.get_opponent(self.current_player)
            rc.append(move)
        return rc

    def perform_random_move(self):
        positions = self.board.get_empty_positions()
        random_pos_index = RandomUtils.get_random_int(0, len(positions))
        pos = positions[random_pos_index]
        self.switch_current_player()
        self.board.perform_move(self.current_player, pos[0], pos[1])
        self.phase = self.board.check_status()

    def deep_copy(self):
        rc = TicTacToeState(None)
        rc.phase = self.phase
        rc.current_player = self.current_player
        rc.board = self.board.deep_copy()
        return rc

    def apply_moves(self, moves):
        for move in moves:
            self.board.perform_move(move.player, move.x, move.y)
        self.phase = self.board.check_status()
