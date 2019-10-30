import src.uct.algorithm.mc_node_utils as NodeUtils
import src.uct.algorithm.uct_calculation as UCT
import src.uct.algorithm.enums as Enums
from src.uct.algorithm.mc_tree import MonteCarloTree


class MonteCarloTreeSearch:
    def __init__(self, game_state):
        self.iterations = 0
        self.debug_print_allowed = False
        self.tree = MonteCarloTree(game_state)

    def calculate_next_move(self):
        while self.iterations < 1:
            self._print_debug("\n=======Iteration {} =======".format(self.iterations))
            promising_node = self._selection(self.tree.root)
            self._expansion(promising_node)

            if promising_node.has_children():
                leaf_to_explore = NodeUtils.get_random_child(promising_node)
            else:
                leaf_to_explore = promising_node

            playout_result = self._simulation(leaf_to_explore)
            self._backpropagation(leaf_to_explore, playout_result)

            self.iterations = self.iterations + 1

        best_child = NodeUtils.get_child_with_max_score(self.tree.root)
        self._print_debug("Best node is {}".format(best_child.id))

        result_game_state = self.tree.retrieve_node_game_state(best_child)
        result_game_state.switch_current_player()
        result_move = best_child.move
        return result_move, result_game_state

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

        self._print_debug("Selection from {} led to {}".format(node.id, tmp_node.id))
        return tmp_node

    def _expansion(self, node):
        """
        2nd stage of MCTS
        Unless L ends the game, create one (or more) child nodes and choose node C from one of them.
        :param node: node from which to start expanding
        """
        node_state = self.tree.retrieve_node_game_state(node)
        if node_state.phase != Enums.GamePhase.IN_PROGRESS:
            self._print_debug("Cannot expand from node {}".format(node.id))

        self._print_debug("Expanding from node {}".format(node.id))
        possible_moves = node_state.get_all_possible_moves()
        for move in possible_moves:
            node.add_child(move)

    def _simulation(self, leaf):
        """
        3rd stage of MCTS
        Complete one random playout from node C.
        :param leaf: leaf from which to process a random playout
        """
        leaf_state = self.tree.retrieve_node_game_state(leaf)
        tmp_state = leaf_state.deep_copy()
        tmp_phase = leaf_state.phase
        opponent_win_phase = Enums.get_opponent_win(tmp_state.current_player)

        if tmp_phase == opponent_win_phase:
            # TODO: do we do anything here?
            return tmp_phase
        elif tmp_phase == Enums.GamePhase.DRAW:
            # TODO: do we do anything here?
            return tmp_phase

        self._print_debug("Simulating from node {}...".format(leaf.id))

        while tmp_phase == Enums.GamePhase.IN_PROGRESS:
            tmp_state.perform_random_move()
            tmp_phase = tmp_state.phase

        return tmp_phase

    def _backpropagation(self, leaf, playout_result):
        """
        4th stage of MCTS
        Use the result of the playout to update information in the nodes on the path from C to R.
        :param leaf: leaf from which to start backpropagating
        :param playout_result: result of random playout simulated from :leaf:
        """
        self._print_debug("Backpropagating from node {}".format(leaf.id))

        tmp_node = leaf
        while tmp_node != self.tree.root:
            tmp_node.details.mark_visit()
            tmp_current_player = tmp_node.move.player
            if playout_result == Enums.get_player_win(tmp_current_player):
                tmp_node.details.add_score(1)
            tmp_node = tmp_node.parent
        self.tree.root.details.mark_visit()

    def _print_debug(self, log):
        if self.debug_print_allowed:
            print("\tMCTS:" + log)
