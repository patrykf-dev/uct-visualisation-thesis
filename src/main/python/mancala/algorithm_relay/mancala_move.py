
from uct.game.base_game_move import BaseGameMove


class MancalaMove(BaseGameMove):
    """
    Class is implementing BaseGameMove class methods in relation to mancala game.
    """
    def __init__(self, moves_sequence: list, player):
        super().__init__()
        self.moves_sequence = moves_sequence
        self.player = player

    def move_equal(self, move) -> bool:
        """
		Args:
			move:  MancalaMove object

		Returns:
			bool, tells whether the moves are equal when it comes to holes chosen (checking move-sequences as well)        
		"""
        self_length = len(self.moves_sequence)
        if self_length != len(move.moves_sequence):
            return False

        for i in range(self_length):
            if self.moves_sequence[i] != move.moves_sequence[i]:
                return False
        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.moves_sequence}{self.player}"

