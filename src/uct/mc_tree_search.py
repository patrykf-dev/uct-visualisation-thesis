import src.uct.enums as Enums
import src.uct.node_utils as NodeUtils
import src.uct.uct_calculation as UCT
from src.uct.node import Node


class MonteCarloTreeSearch:
    def __init__(self):
        self.iterations = 0
        self.debug_print_allowed = False

    def find_next_move(self, game_data):
        root = Node.create_root(game_data)
        self.print_debug(game_data.board.get_string_formatted())
        while self.iterations < 500:
            self.print_debug("\n=======Iteration {} =======".format(self.iterations))
            promising_node = self._selection(root)
            self._expansion(promising_node)

            if promising_node.has_children():
                leaf_to_explore = NodeUtils.get_random_child(promising_node)
            else:
                leaf_to_explore = promising_node

            playout_result = self._simulation(leaf_to_explore)
            self._backpropagation(leaf_to_explore, playout_result)

            self.iterations = self.iterations + 1

        best_child = NodeUtils.get_child_with_max_score(root)
        self.print_debug("Best node is {}".format(best_child.id))
        return best_child.game_data

    def _selection(self, node):
        """
        1st stage of MCTS
        Start from root R and select successive child nodes until a leaf node L is reached.
        :param node: node from which to start selection
        :return: UCT-best leaf node
        """
        tmp_node = node
        while tmp_node.has_children() != 0:
            tmp_node = UCT.find_best_child_with_UCT(tmp_node)

        self.print_debug("Selection from {} led to {}".format(node.id, tmp_node.id))
        return tmp_node

    def _expansion(self, node):
        """
        2nd stage of MCTS
        Unless L ends the game, create one (or more) child nodes and choose node C from one of them.
        :param node: node from which to start expanding
        """
        if node.game_data.phase != Enums.GamePhase.IN_PROGRESS:
            self.print_debug("Cannot expand from node {}".format(node.id))

        self.print_debug("Expanding from node {}".format(node.id))
        possible_states = node.game_data.get_all_possible_states()
        for state in possible_states:
            node.add_child(state)

    def _simulation(self, leaf):
        """
        3rd stage of MCTS
        Complete one random playout from node C.
        :param leaf: leaf from which to process a random playout
        """
        tmp_state = leaf.game_data.deep_copy()
        tmp_phase = leaf.game_data.phase
        opponent_win_phase = Enums.get_opponent_win(tmp_state.current_player)

        if tmp_phase == opponent_win_phase:
            # TODO: do we do anything here?
            return tmp_phase
        elif tmp_phase == Enums.GamePhase.DRAW:
            # TODO: do we do anything here?
            return tmp_phase

        self.print_debug("Simulating from node {}...".format(leaf.id))

        while tmp_phase == Enums.GamePhase.IN_PROGRESS:
            tmp_state.random_move()
            tmp_phase = tmp_state.phase

        return tmp_phase

    def _backpropagation(self, leaf, playout_result):
        """
        4th stage of MCTS
        Use the result of the playout to update information in the nodes on the path from C to R.
        :param leaf: leaf from which to start backpropagating
        :param playout_result: result of random playout simulated from :leaf:
        """
        self.print_debug("Backpropagating from node {}".format(leaf.id))

        tmp_node = leaf
        while tmp_node is not None:
            tmp_node.details.visits_count = tmp_node.details.visits_count + 1
            tmp_current_player = tmp_node.game_data.current_player
            if playout_result == Enums.get_player_win(tmp_current_player):
                tmp_node.details.add_score(1)
            tmp_node = tmp_node.parent

    def print_debug(self, log):
        if self.debug_print_allowed:
            print(log)
