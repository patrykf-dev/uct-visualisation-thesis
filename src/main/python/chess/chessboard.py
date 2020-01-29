
import copy


from chess.enums import GameStatus, TileMarkArgs, TileMarkType
from chess.figures import *
from chess.figures_collection import ChessFiguresCollection
from utils.custom_event import CustomEvent


class Chessboard:
    """
    Class is responsible for chess logic.
    """
    def __init__(self):
        """
        Initialize chess-game logic class. Set white color to start.
        """
        self.possible_moves = []
        self.check = False
        self.current_player_color = Color.WHITE
        self.figures = ChessFiguresCollection(Chessboard.create_figures())
        self.game_status = GameStatus.IN_PROGRESS
        self.past_moves = []
        self.notify_tile_marked = CustomEvent()

    @staticmethod
    def create_figures():
        """
        Arranges chess figures in their native positions.

		Returns:
			list of chess figures        
		"""
        base_figures = [Rook(Color.WHITE, (0, 0)), Knight(Color.WHITE, (0, 1)), Bishop(Color.WHITE, (0, 2)),
                        Queen(Color.WHITE, (0, 3)), King(Color.WHITE, (0, 4)), Bishop(Color.WHITE, (0, 5)),
                        Knight(Color.WHITE, (0, 6)), Rook(Color.WHITE, (0, 7)), Rook(Color.BLACK, (7, 0)),
                        Knight(Color.BLACK, (7, 1)), Bishop(Color.BLACK, (7, 2)), Queen(Color.BLACK, (7, 3)),
                        King(Color.BLACK, (7, 4)), Bishop(Color.BLACK, (7, 5)), Knight(Color.BLACK, (7, 6)),
                        Rook(Color.BLACK, (7, 7))]
        for i in range(8):
            base_figures.append(Pawn(Color.WHITE, (1, i)))
            base_figures.append(Pawn(Color.BLACK, (6, i)))
        return base_figures

    def deep_copy(self):
        """
        Creates a deep copy.

		Returns:
			deep copy        
		"""
        rc = Chessboard()
        rc.current_player_color = self.current_player_color
        rc.check = self.check
        rc.game_status = self.game_status

        rc.possible_moves = copy.deepcopy(self.possible_moves)
        rc.figures = copy.deepcopy(self.figures)
        rc.past_moves = copy.deepcopy(self.past_moves)
        return rc

    def check_for_check(self, color_that_causes_check):
        """
        Determines if player with given color threatens the opponent with check. The function updates check mask of
        the king if this color.

		Args:
			color_that_causes_check:  color of the king to check if threatened

		Returns:
			bool value telling whether there is a check        
		"""
        king = self.figures.get_king(color_that_causes_check)
        king.update_check_mask(self.figures)
        self.check = king.check_mask[king.position]

    def do_move(self, move, selected_tile):
        """
        Does chess move and changes positions of the involved figures. Determines which move type is this.
        Updates king's position.

		Args:
			move:  ChessMove class object
			selected_tile:  tile selected to move to

		Returns:
			None        
		"""
        figure_moved = self.figures.get_figure_at(selected_tile)
        if move.move_type == MoveType.NORMAL:
            from chess.chess_utils import do_normal_move
            do_normal_move(self, move, figure_moved)
        elif move.move_type == MoveType.PAWN_DOUBLE_MOVE:
            from chess.chess_utils import do_pawn_double_move
            do_pawn_double_move(self, move, figure_moved)
        elif move.move_type == MoveType.EN_PASSANT:
            from chess.chess_utils import do_en_passant_move
            do_en_passant_move(self, move, figure_moved)
        elif move.move_type == MoveType.PROMOTION:
            from chess.chess_utils import do_promotion
            do_promotion(self, move, figure_moved)
        elif move.move_type == MoveType.CASTLE_SHORT or move.move_type == MoveType.CASTLE_LONG:
            from chess.chess_utils import do_castling
            do_castling(self, move, figure_moved)
        if figure_moved.figure_type == FigureType.KING:
            self.figures.set_king_reference(figure_moved)

    def add_past_move(self, position, figures_count_before_move, old_position):
        """
        Adds move to the 'historical moves' list.

		Args:
			position:  position we make move on
			figures_count_before_move:  to determine whether the move was a capture
			old_position:  position we make move from

		Returns:
			None        
		"""
        figure = self.figures.get_figure_at(position)
        from chess.chess_utils import PastMove
        self.past_moves.append(
            PastMove(position, self.check, figure, len(self.figures.figures_list) < figures_count_before_move,
                     old_position))

    def perform_legal_move(self, move):
        """
        Main function that does a move and updates game status afterwards.
        It does move, checks for king-check, adds move to the list of past moves, switches current moving player
        and updates game status. It also clears 'effects' on pawns that could be captured en passant.

		Args:
			move:  ChessMove object

		Returns:
			None        
		"""
        Pawn.clear_en_passant_capture_ability_for_one_team(self.figures, self.current_player_color)
        figures_count_before_move = len(self.figures.figures_list)
        self.do_move(move, move.position_from)
        self.check_for_check(self.get_opposite_color())
        if self.check:
            king_pos = self.figures.get_king_position(self.get_opposite_color())
            self.notify_tile_marked.fire(self, earg=TileMarkArgs(king_pos, TileMarkType.CHECKED))
        self.add_past_move(move.position_to, figures_count_before_move, move.position_from)
        self.notify_tile_marked.fire(self, earg=TileMarkArgs(move.position_from, TileMarkType.MOVED))
        self.notify_tile_marked.fire(self, earg=TileMarkArgs(move.position_to, TileMarkType.MOVED))
        self.switch_current_player()
        self.update_game_status()

    def update_game_status(self):
        """
        Determins if game is still in progress or it has ended (with checkmate, stalemate, draw, etc.)

		Returns:
			None        
		"""
        from chess.chess_utils import is_there_any_possible_move
        move_is_possible = is_there_any_possible_move(self)
        if not move_is_possible:
            if self.check:
                self.game_status = \
                    GameStatus.CHECKMATE_WHITE if self.current_player_color == Color.BLACK else GameStatus.CHECKMATE_BLACK
            else:
                self.game_status = GameStatus.STALEMATE
        else:
            from chess.chess_utils import is_there_a_draw
            is_there_a_draw(self)

    def get_opposite_color(self):
        """
		Returns:
			Opponent's color        
		"""
        return Color.WHITE if self.current_player_color == Color.BLACK else Color.BLACK

    def switch_current_player(self):
        """
        Sets opponent as the current moving player.
        """
        self.current_player_color = self.get_opposite_color()

