
from enum import Enum


class GamePhase(Enum):
    IN_PROGRESS = 1,
    PLAYER1_WON = 2,
    PLAYER2_WON = 3,
    DRAW = 4


def get_player_win(player):
    """
		Args:
			player:  player number, 1 or 2

		Returns:
			GamePhase.PLAYER1_WON for player 1, GamePhase.PLAYER2_WON for player 2. Raises exception for other numbers.    
		"""
    if player == 1:
        return GamePhase.PLAYER1_WON
    elif player == 2:
        return GamePhase.PLAYER2_WON
    else:
        raise Exception("Unknown player index")

