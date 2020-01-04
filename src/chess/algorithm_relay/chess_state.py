from math import pi, atan

import src.chess.chess_utils as ChessUtils
import src.utils.random_utils as RandomUtils
from src.chess.chessboard import Chessboard
from src.chess.enums import GameStatus as ChessPhase
from src.uct.algorithm.enums import GamePhase as AbstractPhase
from src.uct.game.base_game_state import BaseGameState


class ChessState(BaseGameState):
    """
    Class is implementing BaseGameState class methods in relation to chess game.
    """
    def __init__(self, board: Chessboard):
        super().__init__()
        self.board = board
        self.current_player = ChessUtils.get_player_from_color(board.current_player_color)

    def get_win_score(self, player):
        """
        Function evaluates score for a player's move. It is reserved for situations when after the move game is still
        in progress.
        Function used - atan(0.25*x), curved in the middle. It was used instead of linear function, to make a capture's
        reward relatively higher.
        diff - difference between figures' values on board. Range: [-39; 39]
        :param player: number 1 (white player) or 2 (black player)
        :return: value from range [0.2; 0.8] (middle value is 0.5 - treated like a draw)
        """
        player1_value = min(39, self.board.figures.player1_value)
        player2_value = min(39, self.board.figures.player2_value)
        if player == 1:
            diff = player1_value - player2_value
        else:
            diff = player2_value - player1_value

        diff_normalized = 0.6 * (((2 / pi) * atan(0.25 * diff) + 1) / 2) + 0.2
        return diff_normalized

    def get_all_possible_moves(self):
        """
        :return: All possible moves of currently moving player. List of ChessMove objects.
        """
        return ChessUtils.get_all_possible_moves(self.board)

    def perform_random_move(self):
        """
        Function chooses on of the all possible moves of currently moving player and performs it, changing the current
        player afterwards. Game phase is saved after the performed move.
        :return: None
        """
        all_possible_moves = ChessUtils.get_all_possible_moves(self.board)
        random_number = RandomUtils.get_random_int(0, len(all_possible_moves))
        move = all_possible_moves[random_number]
        self.board.perform_legal_move(move)
        self.switch_current_player()
        self.phase = ChessState.cast_chess_phase_to_abstract_phase(self.board.game_status)

    def deep_copy(self):
        """
        :return: Deep copy of ChessState object.
        """
        new_board = self.board.deep_copy()
        rc = ChessState(new_board)
        rc.phase = self.phase
        rc.current_player = ChessUtils.get_player_from_color(self.board.current_player_color)
        return rc

    def generate_description(self):
        """
        :return: Description of current game state including: its name, figures left on board, values of figures
                 of both players.
        """
        status = str(self.board.game_status).split(".")[1]
        return f"{status}, {len(self.board.figures.figures_list)} figures left on board," \
               f" player1 value: {self.board.figures.player1_value}, player2 value: {self.board.figures.player2_value}"

    def apply_moves(self, moves):
        """
        Applies moves from the given list and saves the current game phase.
        :param moves: list of ChessMove objects
        :return: None
        """
        for move in moves:
            self.board.perform_legal_move(move)
        self.phase = ChessState.cast_chess_phase_to_abstract_phase(self.board.game_status)

    @staticmethod
    def cast_chess_phase_to_abstract_phase(chess_phase):
        """
        Casts ChessPhase enum items to match the abstract GamePhase interface.
        checkmate white -> player 1 won
        checkmate black -> player 2 won
        draw/stalemate/fifty move rule -> draw
        game in progress -> game in progress
        :param chess_phase: ChessPhase object
        :return: GamePhase object
        """
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
