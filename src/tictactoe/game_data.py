from src.uct.game_data import GameData
import src.uct.random_utils as RandomUtils
from src.tictactoe.board import TicTacToeBoard


class TicTacToeGameData(GameData):
    def __init__(self, board):
        super().__init__()
        self.board = board

    def get_all_possible_states(self):
        positions = self.board.get_empty_positions()
        rc = []
        for position in positions:
            new_board = self.board.deep_copy()
            new_state = TicTacToeGameData(new_board)
            new_state.current_player = self.current_player
            new_state.switch_current_player()
            new_board.perform_move(new_state.current_player, position[0], position[1])
            new_state.phase = new_board.check_status()
            rc.append(new_state)
        return rc

    def random_move(self):
        positions = self.board.get_empty_positions()
        random_pos_index = RandomUtils.get_random_int(0, positions.size)
        pos = positions[random_pos_index]
        self.switch_current_player()
        self.board.perform_move(self.current_player, pos[0], pos[1])
        self.phase = self.board.check_status()

    def deep_copy(self):
        rc = TicTacToeGameData(None)
        rc.phase = self.phase
        rc.current_player = self.current_player
        rc.board = self.board.deep_copy()
        return rc
