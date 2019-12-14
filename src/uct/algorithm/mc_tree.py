from src.uct.algorithm.mc_node import MonteCarloNode
from src.uct.game.base_game_move import BaseGameMove
from src.uct.game.base_game_state import BaseGameState


class MonteCarloTree:
    def __init__(self, game_state: BaseGameState = None, root: MonteCarloNode = None):
        if game_state is not None:
            self.root = MonteCarloNode.create_root()
            self.game_state = game_state
        else:
            self.game_state = None
            self.root = root
        self.data = TreeData()

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
            # Couldn't find the move specified
            self.root.add_child_by_move(move)
            if len(self.root.children) > 1:
                raise RuntimeError("Why wouldn't you find your move?")
            next_root = self.root.children[0]
        self.root = next_root

    def reset_vis_data(self):
        self._reset_vis_data_internal(self.root)

    def _reset_vis_data_internal(self, node: MonteCarloNode):
        node.vis_details.x = -1
        node.vis_details.thread = None
        node.vis_details.mod = 0
        node.vis_details.ancestor = self
        node.vis_details.change = 0
        node.vis_details.shift = 0
        node._left_most_sibling = None
        for child in node.children:
            self._reset_vis_data_internal(child)


class TreeData:
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.max_visits_count = 0

    def update_tree_data(self, node: MonteCarloNode):
        x = node.vis_details.x
        y = node.vis_details.y
        self.max_x = max(x, self.max_x)
        self.min_x = min(x, self.min_x)
        self.max_y = max(y, self.max_y)
        self.min_y = min(y, self.min_y)
        if node.parent is not None:
            self.max_visits_count = max(node.details.visits_count, self.max_visits_count)

    def reset_to_defaults(self):
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.max_visits_count = 0
