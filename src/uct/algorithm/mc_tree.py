from src.uct.algorithm.mc_node import MonteCarloNode
from src.uct.game.base_game_move import BaseGameMove
from src.uct.game.base_game_state import BaseGameState


class MonteCarloTree:
    def __init__(self, game_state: BaseGameState):
        self.root = MonteCarloNode.create_root()
        self.game_state = game_state

    def retrieve_node_game_state(self, node: MonteCarloNode):
        tmp_node = node
        moves = []
        while tmp_node != self.root:
            moves.append(tmp_node.move)
            tmp_node = tmp_node.parent

        rc = self.game_state.deep_copy()
        rc.apply_moves(moves[::-1])
        return rc

    def perform_move_on_root(self, move: BaseGameMove):
        next_root = None
        for child in self.root.children:
            if move.move_equal(child.move):
                next_root = child
                break

        if next_root is None:
            raise RuntimeError("Couldn't find the move specified")

        self.root = next_root
