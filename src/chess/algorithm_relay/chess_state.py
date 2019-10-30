import src.utils.random_utils as RandomUtils
from src.chess.enums import GameStatus as ChessPhase, Color
from src.uct.algorithm.enums import GamePhase as AbstractPhase
from src.uct.game.base_game_state import BaseGameState
import src.chess.chess_utils as ChessUtils


class ChessState(BaseGameState):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.current_player = board.current_player

    def get_all_possible_moves(self):
        return ChessUtils.get_all_possible_moves(self.board)

    def perform_random_move(self):
        all_possible_moves = self.board.get_all_possible_moves()
        random_number = RandomUtils.get_random_int(0, len(all_possible_moves))
        move = all_possible_moves[random_number]
        self.board.perform_raw_move(move.position_from, move.position_to)
        print(
            f"Player {move.player} performing move from {move.position_from} to {move.position_to}, figures left {len(self.board.figures)}")
        self.switch_current_player()
        self.phase = ChessState.cast_chess_phase_to_abstract_phase(self.board.game_status)

    def deep_copy(self):
        new_board = self.board.deep_copy()
        rc = ChessState(new_board)
        rc.phase = self.phase
        return rc

    def apply_moves(self, moves):
        for move in moves:
            self.board.perform_raw_move(move.position_from, move.position_to)
        self.phase = ChessState.cast_chess_phase_to_abstract_phase(self.board.game_status)

    @staticmethod
    def cast_chess_phase_to_abstract_phase(chess_phase):
        switcher = {
            ChessPhase.IN_PROGRESS: AbstractPhase.IN_PROGRESS,
            ChessPhase.CHECKMATE_WHITE: AbstractPhase.PLAYER1_WON,
            ChessPhase.CHECKMATE_BLACK: AbstractPhase.PLAYER2_WON,
            ChessPhase.STALEMATE: AbstractPhase.DRAW,
            ChessPhase.DRAW: AbstractPhase.DRAW,
            ChessPhase.THREEFOLD_REPETITION: AbstractPhase.DRAW,
            ChessPhase.PERPETUAL_CHECK: AbstractPhase.DRAW,
            ChessPhase.FIFTY_MOVE_RULE: AbstractPhase.DRAW
        }
        return switcher.get(chess_phase)
