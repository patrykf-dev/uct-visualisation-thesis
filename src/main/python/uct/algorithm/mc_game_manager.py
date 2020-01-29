
from main_application.gui_settings import MonteCarloSettings
from uct.algorithm.mc_tree import MonteCarloTree
from uct.algorithm.mc_tree_search import MonteCarloTreeSearch
from uct.game.base_game_move import BaseGameMove
from uct.game.base_game_state import BaseGameState
from utils.custom_event import CustomEvent


class MonteCarloGameManager:
    """
    CLass is responsible for performing UCT algorithm moves and keeping information about game state and settings.
    """
    def __init__(self, game_state: BaseGameState, settings: MonteCarloSettings):
        self.current_state = game_state
        self.tree = MonteCarloTree(self.current_state)
        self.settings = settings
        self.first_move = True
        self.previous_move_calculated = None
        self.chosen_node = None
        self.iteration_performed = CustomEvent()

    def notify_move_performed(self, move: BaseGameMove):
        """
        Updates tree's nodes after player's move. It this is not the first move, it firstly updates the information
        after last algorithm's move to keep consistency.

		Args:
			move:  BaseGameMove object

		Returns:
			None        
		"""
        if self.first_move:
            self.first_move = False
            return
        else:
            self.tree.perform_move_on_root(self.previous_move_calculated)
            self.tree.perform_move_on_root(move)
            self.previous_move_calculated = None

    def perform_previous_move(self):
        """
        Updates tree's nodes after last algorithm's move.

		Returns:
			None        
		"""
        self.tree.perform_move_on_root(self.previous_move_calculated)
        self.previous_move_calculated = None

    def calculate_next_move(self):
        """
        Calculates algorithm's move with UCT algorithm.
        Information about chosen move is stored after execution.

		Returns:
			calculated move, BaseGameMove object        
		"""
        mcts = MonteCarloTreeSearch(self.tree, self.settings)
        mcts.iteration_performed += self._handle_iteration_performed
        move, state, best_node = mcts.calculate_next_move()
        self.chosen_node = best_node
        self.previous_move_calculated = move
        return move

    def _handle_iteration_performed(self, sender, earg):
        self.iteration_performed.fire(self, earg)

