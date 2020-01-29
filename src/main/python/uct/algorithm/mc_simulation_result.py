
from uct.game.base_game_state import BaseGameState


class MonteCarloSimulationResult:
    """
    Class is responsible for storing the rewards from the game.
    """
    def __init__(self, tmp_state: BaseGameState):
        self.phase = tmp_state.phase
        self.player1_reward = tmp_state.get_win_score(1)
        self.player2_reward = tmp_state.get_win_score(2)

    def get_reward(self, leaf_player):
        """
		Args:
			leaf_player:  player 1 or 2

		Returns:
			reward of the game        
		"""
        if leaf_player == 1:
            return self.player1_reward
        else:
            return self.player2_reward

