import src.uct.algorithm.enums as Enums
import src.uct.algorithm.mc_node_utils as NodeUtils
import src.uct.algorithm.uct_calculation as UCT
from src.uct.algorithm.mc_simulation_result import MonteCarloSimulationResult
from src.uct.algorithm.mc_tree import MonteCarloTree
from src.uct.game.base_game_move import BaseGameMove
from src.uct.game.base_game_state import BaseGameState


class MonteCarloTreeSearch:
    def __init__(self, tree: MonteCarloTree, max_iterations, max_moves_per_simulation):
        self.iterations = 0
        self.tree = tree
        self.debug_print_allowed = False
        self.max_iterations = max_iterations
        self.max_moves_per_simulation = max_moves_per_simulation

    def calculate_next_move(self) -> (BaseGameMove, BaseGameState):
        while self.iterations < self.max_iterations:
            self._print_debug("\n=======Iteration {} =======".format(self.iterations))
            promising_node = self._selection(self.tree.root)
            self._expansion(promising_node)

            if promising_node.has_children():
                leaf_to_explore = NodeUtils.get_random_child(promising_node)
            else:
                leaf_to_explore = promising_node

            simulation_result = self._simulation(leaf_to_explore)
            self._backpropagation(leaf_to_explore, simulation_result)
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
            node.add_child_by_move(move)

    def _simulation(self, leaf) -> MonteCarloSimulationResult:
        """
        3rd stage of MCTS
        Complete one random playout from node C.
        :param leaf: leaf from which to process a random playout
        """
        leaf_state = self.tree.retrieve_node_game_state(leaf)
        tmp_state = leaf_state.deep_copy()
        tmp_phase = leaf_state.phase

        self._print_debug("Simulating from node {}...".format(leaf.id))

        moves_counter = 0
        count_formatted = f"#{str(self.iterations).ljust(4)}"
        while tmp_phase == Enums.GamePhase.IN_PROGRESS:
            tmp_state.perform_random_move()
            tmp_phase = tmp_state.phase
            moves_counter = moves_counter + 1
            if moves_counter >= self.max_moves_per_simulation:
                print(
                    f"{count_formatted}: node id {leaf.id}, moves performed {moves_counter}, {tmp_state.generate_description()}")
                break

        if tmp_phase != Enums.GamePhase.IN_PROGRESS:
            print(
                f"{count_formatted}: node id {leaf.id}, moves performed {moves_counter}, {tmp_state.generate_description()}")

        return MonteCarloSimulationResult(tmp_state)

    def _backpropagation(self, leaf, simulation_result: MonteCarloSimulationResult):
        """
        4th stage of MCTS
        Use the result of the playout to update information in the nodes on the path from C to R.
        :param leaf: leaf from which to start backpropagating
        :param simulation_result: result of random simulation simulated from :leaf:
        """
        self._print_debug("Backpropagating from node {}".format(leaf.id))

        leaf_state = self.tree.retrieve_node_game_state(leaf)
        leaf_player = leaf_state.current_player
        if simulation_result.phase == Enums.get_player_win(leaf_player):
            reward = 1
        elif simulation_result.phase == Enums.GamePhase.DRAW:
            reward = 0.5
        else:
            reward = simulation_result.get_reward(leaf_player)

        tmp_node = leaf
        while tmp_node != self.tree.root:
            tmp_node.details.mark_visit()
            tmp_current_player = tmp_node.move.player
            if leaf_player == tmp_current_player:
                tmp_node.details.add_score(reward)
            tmp_node = tmp_node.parent
        self.tree.root.details.mark_visit()

    def _print_debug(self, log):
        if self.debug_print_allowed:
            print("\tMCTS:" + log)
