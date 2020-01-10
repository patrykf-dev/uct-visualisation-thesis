import time

import src.uct.algorithm.enums as Enums
import src.uct.algorithm.mc_node_utils as NodeUtils
import src.uct.algorithm.uct_calculation as UCT
from src.main_application.gui_settings import MonteCarloSettings
from src.uct.algorithm.mc_node import MonteCarloNode
from src.uct.algorithm.mc_simulation_result import MonteCarloSimulationResult
from src.uct.algorithm.mc_tree import MonteCarloTree
from src.uct.game.base_game_move import BaseGameMove
from src.uct.game.base_game_state import BaseGameState
from src.utils.custom_event import CustomEvent


class MonteCarloTreeSearch:
    """
    Class responsible for executing four steps of the Monte Carlo Tree Search method in an iterative way.
    """
    def __init__(self, tree: MonteCarloTree, settings: MonteCarloSettings):
        self.tree = tree
        self.debug_print_allowed = False
        self.settings = settings
        self.iteration_performed = CustomEvent()
        self.iterations = 0

    def calculate_next_move(self) -> (BaseGameMove, BaseGameState, MonteCarloNode):
        """
        Depending on the user settings, function calculates the best move for a computer using UCT algorithm.\
        It is calculated by limiting maximum iterations number or by the given time limit.
        The calculation process covers 4 phases: selection, expansion, simulation and backpropagation.
        :return: tuple of (BaseGameMove, BaseGameState, MonteCarloNode) of the chosen move
        """
        if self.settings.limit_iterations:
            return self._calculate_next_move_iterations_limited()
        else:
            return self._calculate_next_move_time_limited()

    def _calculate_next_move_iterations_limited(self):
        """
        Calculates the best move for a computer using UCT algorithm for a given number of iterations.
        After the calculation an event that signalizes the end of iteration is triggered.
        :return: tuple of (BaseGameMove, BaseGameState, MonteCarloNode) of the chosen move
        """
        while self.iterations < self.settings.max_iterations:
            self._perform_iteration()
            self.iteration_performed.fire(self, self.iterations / self.settings.max_iterations)
        return self._select_result_node()

    def _calculate_next_move_time_limited(self):
        """
        Calculates the best move for a computer using UCT algorithm for a given amount of time.
        After the calculation an event that signalizes the end of iteration is triggered.
        When the time is over during calculation, the last iteration is calculated to the end.
        :return: tuple of (BaseGameMove, BaseGameState, MonteCarloNode) of the chosen move
        """
        start_time = time.time()
        elapsed_time_ms = 0
        max_time = self.settings.get_internal_time()
        progress_fraction = 0
        while elapsed_time_ms < max_time:
            self._perform_iteration()
            elapsed_time_ms = (time.time() - start_time) * 1000
            progress_fraction = elapsed_time_ms / max_time
            self.iteration_performed.fire(self, progress_fraction)
        if progress_fraction != 1:
            self.iteration_performed.fire(self, 1)
        return self._select_result_node()

    def _perform_iteration(self):
        """
        Performs single UCT algorithm iteration.
        Execution consists of four steps: selection, expansion, simulation and backpropagation.
        :return: None
        """
        promising_node = self._selection(self.tree.root)
        self._expansion(promising_node)

        if promising_node.has_children():
            leaf_to_explore = NodeUtils.get_random_child(promising_node)
        else:
            leaf_to_explore = promising_node

        simulation_result = self._simulation(leaf_to_explore)
        self._backpropagation(leaf_to_explore, simulation_result)

        self.iterations += 1

    def _select_result_node(self):
        """
        Selects the best UCT node and retrieves game state of that node. The turn is switched afterwards in the
        resulting game state.
        :return: tuple of (BaseGameMove, BaseGameState, MonteCarloNode) of the chosen move
        """
        best_child = NodeUtils.get_child_with_max_score(self.tree.root)
        self._print_debug("Best node is {}".format(best_child.id))

        result_game_state = self.tree.retrieve_node_game_state(best_child)
        result_game_state.switch_current_player()
        result_move = best_child.move
        return result_move, result_game_state, best_child

    def _selection(self, node):
        """
        Executes 1st stage of MCTS.
        Starts from root R and selects successive child nodes until a leaf node L is reached.
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
        Executes 2nd stage of MCTS.
        Unless L ends the game, creates one (or more) child nodes and chooses node C from one of them.
        :param node: node from which to start expanding
        :return: None
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
        Executes 3rd stage of MCTS.
        Complete a random playout from node C.
        :param leaf: leaf from which to process a random playout
        :return: None
        """
        leaf_state = self.tree.retrieve_node_game_state(leaf)
        tmp_state = leaf_state.deep_copy()
        tmp_phase = leaf_state.phase

        self._print_debug("Simulating from node {}...".format(leaf.id))

        moves_counter = 0
        while tmp_phase == Enums.GamePhase.IN_PROGRESS:
            tmp_state.perform_random_move()
            tmp_phase = tmp_state.phase
            moves_counter = moves_counter + 1
            if self.settings.limit_moves and moves_counter >= self.settings.max_moves_per_iteration:
                break
        return MonteCarloSimulationResult(tmp_state)

    def _backpropagation(self, leaf, simulation_result: MonteCarloSimulationResult):
        """
        Executes 4th stage of MCTS.
        Uses the result of the playout to update information in the nodes on the path from C to R.
        :param leaf: leaf from which to start backpropagating
        :param simulation_result: result of random simulation simulated from :leaf:
        :return: None
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
