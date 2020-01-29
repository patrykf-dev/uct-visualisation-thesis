
from chess.enums import MoveType
from uct.game.base_game_move import BaseGameMove


class ChessMove(BaseGameMove):
    """
    Class is implementing BaseGameMove class methods in relation to chess game.
    """
    def __init__(self, position_to, position_from, move_type=MoveType.NORMAL, help_dict=None):
        """
		Args:
			position_to:  last figure's position
			position_from:  new figure's position
			move_type:  enum MoveType object (normal move, double pawn move, castling etc.). Default
			help_dict:  dictionary that helps to locate the other figure's position in less common situations

		Returns:
			(castling, en passant capture). Default: None.        
		"""
        super().__init__()
        self.position_to = position_to
        self.position_from = position_from
        self.move_type = move_type
        self.help_dict = help_dict

    def move_equal(self, move) -> bool:
        """
		Args:
			move:  ChessMove object

		Returns:
			bool, tells whether the moves are equal when it comes to the position and type        
		"""
        return self.position_to[0] == move.position_to[0] and self.position_to[1] == move.position_to[1] and \
               self.position_from[0] == move.position_from[0] and self.position_from[1] == move.position_from[1] and \
               self.move_type == move.move_type

    def __str__(self):
        return f'{self.position_to}, {self.move_type}'

    def real_position_to(self):
        """
        Translates matrix coordinates of chessboard's 'position_to' field to real game-based coordinates.
        columns: 0 -> a, 1 -> b, ..., 7 -> h
        rows: from 0-7 range to 1-8.
        example: (1, 4) -> b5

		Returns:
			string of real game-based chessboard coordinates        
		"""
        return f"{chr(self.position_to[1] + 97)}{self.position_to[0] + 1}"

    def real_position_from(self):
        """
        Translates matrix coordinates of chessboard's 'position_from' field to real game-based coordinates.
        columns: 0 -> a, 1 -> b, ..., 7 -> h
        rows: from 0-7 range to 1-8.
        example: (1, 4) -> b5

		Returns:
			string of real game-based chessboard coordinates        
		"""
        return f"{chr(self.position_from[1] + 97)}{self.position_from[0] + 1}"

