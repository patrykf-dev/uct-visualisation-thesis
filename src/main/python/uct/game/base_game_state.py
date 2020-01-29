
import abc

from uct.algorithm.enums import GamePhase


class BaseGameState(abc.ABC):
    """
    Abstract class for state implementation and manipulation of any game that meets UCT algorithm conditions.
    """
    def __init__(self):
        self.phase = GamePhase.IN_PROGRESS
        self.current_player = 1

    @abc.abstractmethod
    def get_all_possible_moves(self):
        """
		Returns:
			all possible moves of currently moving player        
		"""
        pass

    @abc.abstractmethod
    def perform_random_move(self):
        """
        Performs move selected randomly.
        """
        pass

    @abc.abstractmethod
    def apply_moves(self, moves):
        """
        Apply all moves in the queue.

		Args:
			moves:  list of moves implementing BaseGameMove

		"""
        pass

    @abc.abstractmethod
    def get_win_score(self, player):
        """
		Args:
			player:  player number

		Returns:
			score of given player        
		"""
        pass

    @abc.abstractmethod
    def deep_copy(self):
        """
		Returns:
			deep copy of the state        
		"""
        pass

    def switch_current_player(self):
        """
        Switches turn between two players.

		Returns:
			None        
		"""
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

