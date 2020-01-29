
from abc import ABC, abstractmethod

from numpy import zeros

from chess.algorithm_relay.chess_move import ChessMove
from chess.enums import FigureType, Color, MoveType
from chess.figures_collection import ChessFiguresCollection


class Figure(ABC):
    """
    Abstract class for chess figures.
    """
    def __init__(self, color, figure_type, image_file, position):
        self.color = color
        self.figure_type = figure_type
        self.image_file = image_file
        self.position = position
        super().__init__()

    @abstractmethod
    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        """
        Checks all possible moves.

		Args:
			figures:  ChessFiguresCollection object
			threat_for_king:  bool flag, de facto extends possible moves by those that are not causing direct check,

		Returns:
			but king cannot move in those positions anyway. Example: pawn cannot move diagonally unless the opponent's        figure stands one diagonal tile away, otherwise this is not a possible pawn's move. Despite this is not the        possible pawn's move, king cannot move to such tile anyway.        
		"""
        pass

    @staticmethod
    def is_move_valid(move_pos):
        """
		Args:
			move_pos:  tuple indicating chessboard tile

		Returns:
			bool - is each component of a tuple inside range [0; 7]        
		"""
        return 0 <= move_pos[0] <= 7 and 0 <= move_pos[1] <= 7

    @staticmethod
    def get_figure(figures: ChessFiguresCollection, position):
        """
		Args:
			figures:  ChessFiguresCollection object
			position:  tuple indicating chessboard tile

		Returns:
			figure (or None)        
		"""
        return figures.get_figure_at(position)

    @staticmethod
    def remove_figure_on_position(figures: ChessFiguresCollection, position):
        """
		Args:
			figures:  ChessFiguresCollection object
			position:  tuple indicating chessboard tile

		Returns:
			None        
		"""
        figures.remove_figure_at(position)

    @staticmethod
    def remove_figure(figures: ChessFiguresCollection, figure):
        """
		Args:
			figures:  ChessFiguresCollection object
			figure:  Figure object

		Returns:
			index of where the figure was placed in the list        
		"""
        return figures.remove(figure)


class FigureWithLinearMovement(Figure):
    """
    Abstract class for similarly-behaving chess figures with linear movement: Bishop, Rook and Queen.
    """
    @abstractmethod
    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):

        pass

    def check_moves_linear(self, figures: ChessFiguresCollection, directions, threat_for_king=False):
        """
        Foreach direction possible figure's moves are checked.

		Args:
			figures:  ChessFiguresCollection object
			directions:  list of direction tuples
			threat_for_king:  bool flag

		Returns:
			possible moves, but without reducing those that uncover the king        
		"""
        possible_moves = []
        pos_x = self.position[0]
        pos_y = self.position[1]
        for direction in directions:
            dir_x = direction[0]
            dir_y = direction[1]
            pos_being_checked = (pos_x + dir_x, pos_y + dir_y)
            while self.is_move_valid(pos_being_checked):
                figure = figures.get_figure_at(pos_being_checked)
                if figure:
                    if figure.color != self.color or threat_for_king:
                        possible_moves.append(ChessMove(pos_being_checked, self.position, MoveType.NORMAL))
                    break
                possible_moves.append(ChessMove(pos_being_checked, self.position, MoveType.NORMAL))
                pos_being_checked = (pos_being_checked[0] + dir_x, pos_being_checked[1] + dir_y)

        return possible_moves


class Pawn(Figure):
    """
    Class representing pawn chess figure.
    """
    MOVE_SETUPS = {
        Color.WHITE: {
            "start_line": 1,
            "last_line": 7,
            "step_forward": lambda x, step: x + step,
            "step_backward": lambda x, step: x - step
        },
        Color.BLACK: {
            "start_line": 6,
            "last_line": 0,
            "step_forward": lambda x, step: x - step,
            "step_backward": lambda x, step: x + step
        }
    }

    def __init__(self, color, position):
        self.can_be_captured_en_passant = False
        self.value = 1
        image_file = 'pawn-white.png' if color == Color.WHITE else 'pawn-black.png'
        super().__init__(color, FigureType.PAWN, image_file, position)

    def set_can_be_captured_en_passant(self, val):
        """
        Setter.

		Args:
			val:  bool

		Returns:
			None        
		"""
        self.can_be_captured_en_passant = val

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        possible_moves = []
        move_setup = Pawn.MOVE_SETUPS[self.color]

        if self.position[0] == move_setup["last_line"]:
            pass
        else:
            pos = move_setup["step_forward"](self.position[0], 1), self.position[1]
            figure = figures.get_figure_at(pos)
            if not figure:
                if pos[0] != move_setup["last_line"]:
                    move = ChessMove(pos, self.position, MoveType.NORMAL)
                else:
                    move = ChessMove(pos, self.position, MoveType.PROMOTION)
                possible_moves.append(move)
                # double move at the beginning
                double_move = move_setup["step_forward"](self.position[0], 2), self.position[1]
                if self.position[0] == move_setup["start_line"] and not figures.get_figure_at(double_move):
                    possible_moves.append(ChessMove(double_move, self.position, MoveType.PAWN_DOUBLE_MOVE))
            possible_moves.extend(self.check_captures(figures, threat_for_king))
        return possible_moves

    def check_captures(self, figures: ChessFiguresCollection, threat_for_king=False):
        """
        Check possible pawn's captures in both sides.

		Args:
			figures:  ChessFiguresCollection object
			threat_for_king:  bool flag

		Returns:
			possible captures, but without reducing those that uncover the king        
		"""
        def _move_diagonally(_pos, color):
            move_setup = Pawn.MOVE_SETUPS[self.color]
            opposite_color = Color.BLACK if color == Color.WHITE else Color.WHITE
            if not self.is_move_valid(_pos):
                return None
            figure = figures.get_figure_at(_pos)
            if figure:
                if figure.color == opposite_color or threat_for_king:
                    return MoveType.NORMAL if _pos[0] != move_setup["last_line"] else MoveType.PROMOTION
            elif threat_for_king:
                return MoveType.NORMAL if _pos[0] != move_setup["last_line"] else MoveType.PROMOTION
            else:
                opponent_pawn_pos = (move_setup["step_backward"](_pos[0], 1), _pos[1])
                figure = figures.get_figure_at(opponent_pawn_pos)
                if not figure:
                    return None
                if self.position[0] == move_setup["step_backward"](move_setup["last_line"], 3) and \
                        figure.figure_type == FigureType.PAWN and \
                        figure.color == opposite_color and \
                        figure.can_be_captured_en_passant:
                    return MoveType.EN_PASSANT
            return None

        def _check_capture_on_one_side(pos_height, color):
            move_setup = Pawn.MOVE_SETUPS[self.color]
            _pos = move_setup["step_forward"](self.position[0], 1), pos_height
            move_type = _move_diagonally(_pos, color)
            if move_type:
                if move_type == MoveType.NORMAL or move_type == MoveType.PROMOTION:
                    possible_captures.append(ChessMove(_pos, self.position, move_type))
                elif move_type == MoveType.EN_PASSANT:
                    possible_captures.append(
                        ChessMove(_pos, self.position, move_type,
                                  {'opponent-pawn-pos': (self.position[0], pos_height)}))

        possible_captures = []
        if self.position[1] > 0:
            _check_capture_on_one_side(self.position[1] - 1, self.color)
        if self.position[1] < 7:
            _check_capture_on_one_side(self.position[1] + 1, self.color)
        return possible_captures

    @staticmethod
    def clear_en_passant_capture_ability_for_one_team(figures: ChessFiguresCollection, color):
        """
        Disables ability to be captured en passant for each pawn of given color.

		Args:
			figures:  ChessFiguresCollection object
			color:  Color enum object

		Returns:
			None        
		"""
        for figure in figures.figures_list:
            if figure.figure_type == FigureType.PAWN and color == figure.color:
                figure.set_can_be_captured_en_passant(False)


class Knight(Figure):
    """
    Class representing knight chess figure.
    """
    def __init__(self, color, position):
        self.value = 3
        image_file = 'knight-white.png' if color == Color.WHITE else 'knight-black.png'
        super().__init__(color, FigureType.KNIGHT, image_file, position)

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        def _wipe_out_bad_moves(move_positions):
            toret = []
            for move_position in move_positions:
                if not self.is_move_valid(move_position):
                    continue
                figure = figures.get_figure_at(move_position)
                if figure and figure.color == self.color:
                    continue
                toret.append(ChessMove(move_position, self.position, MoveType.NORMAL))
            return toret

        possible_moves_positions = [
            (self.position[0] + 2, self.position[1] - 1),
            (self.position[0] + 2, self.position[1] + 1),
            (self.position[0] - 2, self.position[1] + 1),
            (self.position[0] - 2, self.position[1] - 1),
            (self.position[0] + 1, self.position[1] - 2),
            (self.position[0] + 1, self.position[1] + 2),
            (self.position[0] - 1, self.position[1] + 2),
            (self.position[0] - 1, self.position[1] - 2)]
        return _wipe_out_bad_moves(possible_moves_positions)


class Bishop(FigureWithLinearMovement):
    """
    Class representing bishop chess figure.
    """
    def __init__(self, color, position):
        self.value = 3
        self.light_squared = (position[0] + position[1]) % 2 == 1
        image_file = 'bishop-white.png' if color == Color.WHITE else 'bishop-black.png'
        super().__init__(color, FigureType.BISHOP, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.check_moves_linear(figures, directions, threat_for_king)


class Rook(FigureWithLinearMovement):
    """
    Class representing rook chess figure.
    """
    def __init__(self, color, position):
        self.value = 5
        self.is_able_to_castle = True
        image_file = 'rook-white.png' if color == Color.WHITE else 'rook-black.png'
        super().__init__(color, FigureType.ROOK, image_file, position)

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        return self.check_moves_linear(figures, directions, threat_for_king)

    def set_is_able_to_castle(self, val):
        """
        Setter.

		Args:
			val:  bool

		Returns:
			None        
		"""
        self.is_able_to_castle = val


class Queen(FigureWithLinearMovement):
    """
    Class representing queen chess figure.
    """
    def __init__(self, color, position):
        self.value = 9
        image_file = 'queen-white.png' if color == Color.WHITE else 'queen-black.png'
        super().__init__(color, FigureType.QUEEN, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        return self.check_moves_linear(figures, directions, threat_for_king)


class King(Figure):
    """
    Class representing king chess figure.
    It contains the information about chessboard fields, on which king would be under check in 'check_mask'.
    """
    def __init__(self, color, position):
        self.is_able_to_castle = True
        self.initial_position = (0, 4) if color == Color.WHITE else (7, 4)
        self.check_mask = zeros(shape=(8, 8), dtype=bool)
        self.value = 0
        image_file = 'king-white.png' if color == Color.WHITE else 'king-black.png'
        super().__init__(color, FigureType.KING, image_file, position)

    def update_check_mask_around_rival_king(self, figures: ChessFiguresCollection):
        """
        Fills the numpy array of check mask with chessboard fields around the rival king, because kings cannot stand
        next to each other.

		Args:
			figures:  ChessFiguresCollection object

		Returns:
			None        
		"""
        opposite_color = Color.WHITE if self.color == Color.BLACK else Color.BLACK
        rival_king_position = figures.get_king_position(opposite_color)
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        for direction in directions:
            position_being_checked = rival_king_position[0] + direction[0], rival_king_position[1] + direction[1]
            if self.is_move_valid(position_being_checked):
                self.check_mask[position_being_checked] = True
        self.check_mask[rival_king_position] = True

    def reset_check_mask(self):
        """
        Resets check mask with False values.

		Returns:
			None        
		"""
        self.check_mask = zeros(shape=(8, 8), dtype=bool)

    def update_check_mask_by_given_moves(self, moves):
        """
        Updates check mask by positions of given moves.

		Args:
			moves:  list of ChessMove objects

		Returns:
			None        
		"""
        for move in moves:
            self.check_mask[move.position_to] = True

    def update_check_mask(self, figures: ChessFiguresCollection):
        """
        Fills the numpy array of check mask with chessboard fields on which king would be under check.

		Args:
			figures:  ChessFiguresCollection object

		Returns:
			None        
		"""
        self.reset_check_mask()
        previous_position = self.position
        figures.temporarily_disable(self)

        self.update_check_mask_around_rival_king(figures)

        for figure in figures.figures_list:
            attacked_fields = []
            if figure.color == self.color:
                continue
            if figure.figure_type == FigureType.PAWN:
                attacked_fields = figure.check_captures(figures, True)
            elif figure.figure_type != FigureType.KING:
                attacked_fields = figure.check_moves(figures, True)

            if attacked_fields:
                self.update_check_mask_by_given_moves(attacked_fields)

        figures.restore(self, previous_position)

    def possibility_to_castle(self, figures: ChessFiguresCollection):
        """
        Checks whether the king is able to make long or short castling.
        Conditions checked:
        - king did not move before
        - rook did not move before
        - no obstacles are standing on the way from king to rook
        - there is no possible check on the way from king to rook

		Args:
			figures:  ChessFiguresCollection object

		Returns:
			list of possible castling moves of ChessMove class.        
		"""
        def _possibility_to_castle_one_side(move_type):
            if self.position != self.initial_position:
                return

            if move_type == MoveType.CASTLE_SHORT:
                rook_position = (0, 7) if self.color == Color.WHITE else (7, 7)
                offset = -1
            else:
                rook_position = (0, 0) if self.color == Color.WHITE else (7, 0)
                offset = 1
            figure_rook = figures.get_figure_at(rook_position)

            if not figure_rook:
                return
            if figure_rook.figure_type != FigureType.ROOK:
                return
            if not figure_rook.is_able_to_castle:
                return

            figure_offset_1_position = rook_position[0], rook_position[1] + offset
            figure_offset_2_position = rook_position[0], rook_position[1] + 2 * offset
            figure_offset_3_position = rook_position[0], rook_position[1] + 3 * offset

            figure_offset_1 = figures.get_figure_at(figure_offset_1_position)
            figure_offset_2 = figures.get_figure_at(figure_offset_2_position)
            figure_offset_3 = figures.get_figure_at(
                figure_offset_3_position) if move_type == MoveType.CASTLE_LONG else None

            if figure_offset_1:
                return
            if move_type == MoveType.CASTLE_SHORT and self.check_mask[figure_offset_1_position]:
                return
            if figure_offset_2:
                return
            if self.check_mask[figure_offset_2_position]:
                return
            if move_type == MoveType.CASTLE_LONG and (figure_offset_3 or self.check_mask[figure_offset_3_position]):
                return
            final_king_pos = figure_offset_1_position if \
                move_type == MoveType.CASTLE_SHORT else figure_offset_2_position
            final_rook_pos = figure_offset_2_position if \
                move_type == MoveType.CASTLE_SHORT else figure_offset_3_position
            possible_moves.append(ChessMove(final_king_pos, self.position, move_type,
                                            {'rook-end-pos': final_rook_pos, 'rook': figure_rook}))

        possible_moves = []
        if self.is_able_to_castle:
            _possibility_to_castle_one_side(MoveType.CASTLE_SHORT)
            _possibility_to_castle_one_side(MoveType.CASTLE_LONG)
        return possible_moves

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        possible_moves = []
        for direction in directions:
            position_being_checked = self.position[0] + direction[0], self.position[1] + direction[1]
            if not self.is_move_valid(position_being_checked):
                continue
            figure = figures.get_figure_at(position_being_checked)
            if figure:
                if figure.color == self.color:
                    continue
                elif figure.figure_type == FigureType.KING:
                    continue
            if not self.check_mask[position_being_checked]:
                possible_moves.append(ChessMove(position_being_checked, self.position, MoveType.NORMAL))
        if self.is_able_to_castle and not self.check_mask[self.position]:
            possible_moves.extend(self.possibility_to_castle(figures))
        return possible_moves

    def set_is_able_to_castle(self, val):
        """
        Setter.

		Args:
			val:  bool

		Returns:
			None        
		"""
        self.is_able_to_castle = val

