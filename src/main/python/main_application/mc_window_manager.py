from chess.algorithm_relay.chess_state import ChessState
from main_application.enums import GameMode, Game
from main_application.game_canvas import GameCanvas
from main_application.gui_settings import MonteCarloSettings
from uct.algorithm.enums import GamePhase
from uct.algorithm.mc_game_manager import MonteCarloGameManager
from uct.game.base_game_state import BaseGameState
from utils.custom_event import CustomEvent


class MonteCarloWindowManager:
    def __init__(self, canvas: GameCanvas, game_mode: GameMode, start_state: BaseGameState,
                 settings: MonteCarloSettings, game: Game):
        self.canvas = canvas
        self.game_mode = game_mode
        self.mc_manager = MonteCarloGameManager(start_state, settings)
        self.on_update_tree = CustomEvent()
        self.game = game

        self.canvas.player_move_performed += self._handle_player_move_performed
        self.on_update_tree += self._handle_machine_move_performed

    def perform_algorithm_move(self):
        alg_move = self.mc_manager.calculate_next_move()
        self.canvas.perform_algorithm_move(alg_move)
        if self.game == Game.Chess:
            phase = ChessState.cast_chess_phase_to_abstract_phase(self.canvas.chess_manager.board.game_status)
        elif self.game == Game.Mancala:
            phase = self.canvas.board.phase
        move_info = {"phase": phase, "node": self.mc_manager.chosen_node}
        self.on_update_tree.fire(self, earg=move_info)

        if self.game_mode == GameMode.PC_VS_PC:
            self.mc_manager.perform_previous_move()

    def _handle_player_move_performed(self, sender, move_info):
        print(f"Player move performed in {self.game_mode}!")
        if self.game_mode == GameMode.PLAYER_VS_PC and move_info["phase"] == GamePhase.IN_PROGRESS:
            self.mc_manager.notify_move_performed(move_info["move"])
            self.perform_algorithm_move()
        elif move_info["phase"] != GamePhase.IN_PROGRESS:
            self.canvas.set_player_can_click(False)
            self.canvas.game_ended = True

    def _handle_machine_move_performed(self, sender, move_info):
        if move_info["phase"] != GamePhase.IN_PROGRESS:
            self.canvas.set_player_can_click(False)
            self.canvas.game_ended = True
