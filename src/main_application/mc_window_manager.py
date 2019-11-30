import traceback

from src.main_application.enums import GameMode
from src.main_application.game_canvas import GameCanvas
from src.uct.algorithm.mc_game_manager import MonteCarloGameManager
from src.uct.game.base_game_state import BaseGameState
from src.utils.CustomEvent import CustomEvent


class MonteCarloWindowManager:
    def __init__(self, canvas: GameCanvas, game_mode: GameMode, start_state: BaseGameState):
        self.canvas = canvas
        self.game_mode = game_mode
        self.mc_manager = MonteCarloGameManager(start_state)
        self.on_update_tree = CustomEvent()

        self.canvas.player_move_performed += self._handle_player_move_performed

    def perform_algorithm_move(self):
        try:
            alg_move = self.mc_manager.calculate_next_move(max_iterations=50, max_moves_per_simulation=10)
            self.canvas.perform_algorithm_move(alg_move)
            self.on_update_tree.fire(self, earg=self.mc_manager.tree.root)
        except Exception:
            print(traceback.format_exc())

        if self.game_mode == GameMode.PC_VS_PC:
            self.mc_manager.perform_previous_move()

    def _handle_player_move_performed(self, sender, move):
        print(f"Player move performed in {self.game_mode}!")
        if self.game_mode == GameMode.PLAYER_VS_PC:
            self.mc_manager.notify_move_performed(move)
            self.perform_algorithm_move()
