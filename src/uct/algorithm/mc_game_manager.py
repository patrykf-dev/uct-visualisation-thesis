from src.uct.algorithm.mc_tree import MonteCarloTree
from src.uct.algorithm.mc_tree_search import MonteCarloTreeSearch
from src.uct.game.base_game_move import BaseGameMove
from src.uct.game.base_game_state import BaseGameState


class MonteCarloGameManager:
    def __init__(self, game_state: BaseGameState):
        self.current_state = game_state
        self.tree = MonteCarloTree(self.current_state)
        self.first_move = True
        self.previous_move_calculated = None

    def notify_move_performed(self, move: BaseGameMove):
        if self.first_move:
            self.first_move = False
            return
        else:
            self.tree.perform_move_on_root(self.previous_move_calculated)
            self.tree.perform_move_on_root(move)
            self.previous_move_calculated = None

    def perform_previous_move(self):
        self.tree.perform_move_on_root(self.previous_move_calculated)
        self.previous_move_calculated = None

    def calculate_next_move(self, max_iterations=40, max_moves_per_simulation=40):
        mcts = MonteCarloTreeSearch(self.tree, max_iterations, max_moves_per_simulation)
        move, state = mcts.calculate_next_move()
        self.previous_move_calculated = move
        return move
