
import utils.random_utils as RandomUtils
from mancala.mancala_board import MancalaBoard
from uct.algorithm.enums import GamePhase
from uct.game.base_game_state import BaseGameState


class MancalaState(BaseGameState):
    """
    Class is implementing BaseGameState class methods in relation to mancala game.
    """
    def __init__(self, board: MancalaBoard):
        super().__init__()
        self.board = board

    def get_all_possible_moves(self):
        """
		Returns:
			All possible moves of currently moving player. List of MancalaMove objects.        
		"""
        return self.board.find_all_moves()

    def perform_random_move(self):
        """
        Function chooses on of the all possible moves of currently moving player and performs it, changing the current
        player afterwards. Game phase is saved after the performed move.

		Returns:
			None        
		"""
        all_possible_moves = self.get_all_possible_moves()
        random_number = RandomUtils.get_random_int(0, len(all_possible_moves))
        move = all_possible_moves[random_number]
        self.board.perform_move(move[0])
        self.switch_current_player()
        self.phase = self.board.phase

    def apply_moves(self, moves):
        """
        Applies moves from the given list and saves the current game phase.

		Args:
			moves:  list of MancalaMove objects

		Returns:
			None        
		"""
        for move in moves:
            self.board.perform_move(move)
        self.phase = self.board.phase

    def get_win_score(self, player):
        """
        Function evaluates score for a player's move. It is reserved for situations when after the move game is still
        in progress.
        Linear function is used: y = 0.00625x + 0.5.
        diff - difference between figures' values on board. Range: [-48; 48]

		Args:
			player:  number 1 (white player) or 2 (black player)

		Returns:
			value from range [0.2; 0.8] (middle value is 0.5 - treated like a draw)        
		"""
        max_score_diff = 48
        diff = self.board.get_win_score(player)
        a = 0.6 / (max_score_diff * 2)
        diff_normalized = a * diff + 0.5
        return diff_normalized

    def deep_copy(self):
        """
		Returns:
			Deep copy of MancalaState object.        
		"""
        new_board = self.board.deep_copy()
        rc = MancalaState(new_board)
        rc.phase = self.phase
        rc.current_player = self.board.current_player
        return rc

