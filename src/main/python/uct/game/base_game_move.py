
import abc


class BaseGameMove(abc.ABC):
    """
    Abstract class for move implementation of any game that meets UCT algorithm conditions.
    """
    def __init__(self):
        self.player = 1
        self.description = ""

    @abc.abstractmethod
    def move_equal(self, move) -> bool:
        """
		Args:
			move:  BaseGameMove object

		Returns:
			checks move equality        
		"""
        pass

