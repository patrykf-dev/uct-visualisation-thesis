from src.uct.node import Node


class MonteCarloTree:
    def __init__(self, game_state):
        self.root = Node.create_root()
        self.game_state = game_state

    def retrieve_node_game_state(self, node):
        tmp_node = node
        moves = []
        while tmp_node != self.root:
            moves.append(tmp_node.move)
            tmp_node = tmp_node.parent

        rc = self.game_state.deep_copy()
        rc.apply_moves(moves)
        return rc
