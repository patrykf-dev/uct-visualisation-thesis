import src.chess.chess_utils as ChessUtils
import src.utils.random_utils as RandomUtils
from src.chess.chessboard import Chessboard
from src.chess.enums import GameStatus as ChessPhase
from src.uct.algorithm.enums import GamePhase as AbstractPhase
from src.uct.game.base_game_state import BaseGameState


class ChessState(BaseGameState):
    def __init__(self, board: Chessboard):
        super().__init__()
        self.board = board
        self.current_player = ChessUtils.get_player_from_color(board.current_player_color)

    def get_win_score(self):
        if self.current_player == 1:
            return self.board.figures.player1_value
        else:
            return self.board.figures.player2_value

    def get_all_possible_moves(self):
        return ChessUtils.get_all_possible_moves(self.board)

    def perform_random_move(self):
        all_possible_moves = ChessUtils.get_all_possible_moves(self.board)
        random_number = RandomUtils.get_random_int(0, len(all_possible_moves))
        move = all_possible_moves[random_number]
        self.board.perform_legal_move(move)
        self.switch_current_player()
        self.phase = ChessState.cast_chess_phase_to_abstract_phase(self.board.game_status)

    def deep_copy(self):
        new_board = self.board.deep_copy()
        rc = ChessState(new_board)
        rc.phase = self.phase
        rc.current_player = ChessUtils.get_player_from_color(self.board.current_player_color)
        return rc

    def apply_moves(self, moves):
        for move in moves:
            self.board.perform_legal_move(move)
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
