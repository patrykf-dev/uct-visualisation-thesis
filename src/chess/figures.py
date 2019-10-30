from abc import ABC, abstractmethod
from src.chess.enums import FigureType, Color, MoveType
from src.chess.algorithm_relay.chess_move import ChessMove


class Figure(ABC):
    def __init__(self, color, figure_type, image_file, position):
        self.color = color
        self.figure_type = figure_type
        self.image_file = image_file
        self.position = position
        super().__init__()

    @abstractmethod
    def check_moves(self, figures, threat_for_king=False):
        pass

    @staticmethod
    def is_move_valid(move_pos):
        from src.chess.game import TILE_NUMBER
        return 0 <= move_pos[0] <= TILE_NUMBER - 1 and 0 <= move_pos[1] <= TILE_NUMBER - 1

    def move(self, new_position):
        self.position = new_position

    @staticmethod
    def get_figure(figures, position):
        return next((x for x in figures if x.position == position), None)

    @staticmethod
    def remove_figure_on_position(figures, position):
        removed_figure = next((x for x in figures if x.position == position), None)
        if removed_figure:
            figures.remove(removed_figure)

    @staticmethod
    def remove_figure(figures, figure):
        if figure:
            figures.remove(figure)


class FigureWithLinearMovement(Figure):
    @abstractmethod
    def check_moves(self, figures, threat_for_king=False):
        pass

    def check_moves_linear(self, figures, directions, threat_for_king=False):
        possible_moves = []
        for direction in directions:
            position_being_checked = tuple(map(sum, zip(self.position, direction)))
            while self.is_move_valid(position_being_checked):
                figure = self.get_figure(figures, position_being_checked)
                if figure:
                    if figure.color != self.color or threat_for_king:
                        possible_moves.append(ChessMove(position_being_checked, self.position, MoveType.NORMAL))
                    break
                possible_moves.append(ChessMove(position_being_checked, self.position, MoveType.NORMAL))
                position_being_checked = tuple(map(sum, zip(position_being_checked, direction)))
        return possible_moves


class Pawn(Figure):
    def __init__(self, color, position):
        self.can_be_captured_en_passant = False
        image_file = 'pawn-white.png' if color == Color.WHITE else 'pawn-black.png'
        super().__init__(color, FigureType.PAWN, image_file, position)

    def set_can_be_captured_en_passant(self, val):
        self.can_be_captured_en_passant = val

    def check_moves(self, figures, threat_for_king=False):
        from src.chess.game import TILE_NUMBER
        possible_moves = []

        # setting variables
        if self.color == Color.WHITE:
            start_line = 1
            last_line = TILE_NUMBER - 1
            step_forward = lambda x, step: x + step
        else:
            start_line = TILE_NUMBER - 2
            last_line = 0
            step_forward = lambda x, step: x - step

        # pawn at the end - should not happen
        if self.position[0] == last_line:
            print('! Pawn should not be allowed to stay in the end line')
        else:
            pos = step_forward(self.position[0], 1), self.position[1]
            figure = Figure.get_figure(figures, pos)
            if not figure:
                possible_moves.append(ChessMove(pos, self.position, MoveType.NORMAL if pos[0] != last_line else MoveType.PROMOTION))
                # double move at the beginning
                double_move = step_forward(self.position[0], 2), self.position[1]
                if self.position[0] == start_line and not Figure.get_figure(figures, double_move):
                    possible_moves.append(ChessMove(double_move, self.position, MoveType.PAWN_DOUBLE_MOVE))
            # diagonal captures
            possible_moves.extend(self.check_captures(figures, threat_for_king))
        return possible_moves

    def check_captures(self, figures, threat_for_king=False):
        from src.chess.game import TILE_NUMBER

        if self.color == Color.WHITE:
            last_line = TILE_NUMBER - 1
            step_forward = lambda x, step: x + step
            step_backward = lambda x, step: x - step
        else:
            last_line = 0
            step_forward = lambda x, step: x - step
            step_backward = lambda x, step: x + step

        def move_diagonally(_pos, color):
            opposite_color = Color.BLACK if color == Color.WHITE else Color.WHITE
            if not self.is_move_valid(_pos):
                return None
            figure = Figure.get_figure(figures, _pos)
            if figure:
                if figure.color == opposite_color or threat_for_king:
                    if figure.figure_type == FigureType.KING and figure.color == opposite_color:
                        print('! Capture of a king should not be possible')
                    return MoveType.NORMAL if _pos[0] != last_line else MoveType.PROMOTION
            elif threat_for_king:
                return MoveType.NORMAL if _pos[0] != last_line else MoveType.PROMOTION
            # capture en passant
            else:
                opponent_pawn_pos = (step_backward(_pos[0], 1), _pos[1])
                figure = Figure.get_figure(figures, opponent_pawn_pos)
                if not figure:
                    return None
                if self.position[0] == step_backward(last_line, 3) and \
                        figure.figure_type == FigureType.PAWN and \
                        figure.color == opposite_color and \
                        figure.can_be_captured_en_passant:
                    print('capture en passant possible')
                    return MoveType.EN_PASSANT
            return None

        def check_capture_on_one_side(pos_height, color):
            _pos = step_forward(self.position[0], 1), pos_height
            move_type = move_diagonally(_pos, color)
            if move_type:
                if move_type == MoveType.NORMAL or move_type == MoveType.PROMOTION:
                    possible_captures.append(ChessMove(_pos, self.position, move_type))
                elif move_type == MoveType.EN_PASSANT:
                    possible_captures.append(
                        ChessMove(_pos, self.position, move_type, {'opponent-pawn-pos': (self.position[0], pos_height)}))

        possible_captures = []
        if self.position[1] > 0:
            check_capture_on_one_side(self.position[1] - 1, self.color)
        if self.position[1] < TILE_NUMBER - 1:
            check_capture_on_one_side(self.position[1] + 1, self.color)
        return possible_captures

    @staticmethod
    def clear_en_passant_capture_ability_for_one_team(figures, color):
        for figure in figures:
            if figure.figure_type == FigureType.PAWN and color == figure.color:
                figure.set_can_be_captured_en_passant(False)


class Knight(Figure):
    def __init__(self, color, position):
        image_file = 'knight-white.png' if color == Color.WHITE else 'knight-black.png'
        super().__init__(color, FigureType.KNIGHT, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        def wipe_out_bad_moves(moves):
            toret = []
            for move in moves:
                if not self.is_move_valid(move.position_to):
                    continue
                figure = Figure.get_figure(figures, move.position_to)
                if figure and figure.color == self.color:
                    continue
                toret.append(move)
            return toret

        possible_moves = [ChessMove((self.position[0] + 2, self.position[1] - 1), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] + 2, self.position[1] + 1), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] - 2, self.position[1] + 1), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] - 2, self.position[1] - 1), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] + 1, self.position[1] - 2), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] + 1, self.position[1] + 2), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] - 1, self.position[1] + 2), self.position, MoveType.NORMAL),
                          ChessMove((self.position[0] - 1, self.position[1] - 2), self.position, MoveType.NORMAL)]
        return wipe_out_bad_moves(possible_moves)


class Bishop(FigureWithLinearMovement):
    def __init__(self, color, position):
        self.light_squared = (position[0] + position[1]) % 2 == 1
        image_file = 'bishop-white.png' if color == Color.WHITE else 'bishop-black.png'
        super().__init__(color, FigureType.BISHOP, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.check_moves_linear(figures, directions, threat_for_king)


class Rook(FigureWithLinearMovement):
    def __init__(self, color, position):
        self.is_able_to_castle = True
        image_file = 'rook-white.png' if color == Color.WHITE else 'rook-black.png'
        super().__init__(color, FigureType.ROOK, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        return self.check_moves_linear(figures, directions, threat_for_king)

    def set_is_able_to_castle(self, val):
        self.is_able_to_castle = val


class Queen(FigureWithLinearMovement):
    def __init__(self, color, position):
        image_file = 'queen-white.png' if color == Color.WHITE else 'queen-black.png'
        super().__init__(color, FigureType.QUEEN, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        return self.check_moves_linear(figures, directions, threat_for_king)


class King(Figure):
    def __init__(self, color, position):
        self.is_able_to_castle = True
        self.initial_position = (0, 4) if color == Color.WHITE else (7, 4)
        image_file = 'king-white.png' if color == Color.WHITE else 'king-black.png'
        super().__init__(color, FigureType.KING, image_file, position)

    # check if at least one of all possible rival's moves coincide with 'position';
    def is_check_on_position_given(self, position, figures):
        opponent_moves = set()
        for figure in figures:
            # only look for checks from the opposite color
            if figure.color == self.color:
                continue
            # pawns have different capture rules
            if figure.figure_type == FigureType.PAWN:
                # opponent_moves.update(figure.check_captures((i, j), board, True))
                opponent_moves.update(x.position_to for x in figure.check_captures(figures, True))
            # to avoid recursion
            elif figure.figure_type != FigureType.KING:
                opponent_moves.update(x.position_to for x in figure.check_moves(figures, True))
        return position in opponent_moves

    def possibility_to_castle(self, position, figures):
        def possibility_to_castle_one_side(move_type):
            if move_type == MoveType.CASTLE_SHORT:
                rook_position = (0, 7) if self.color == Color.WHITE else (7, 7)
                offset = -1
            else:
                rook_position = (0, 0) if self.color == Color.WHITE else (7, 0)
                offset = 1
            figure_rook = Figure.get_figure(figures, rook_position)

            figure_offset_1_position = rook_position[0], rook_position[1] + offset
            figure_offset_2_position = rook_position[0], rook_position[1] + 2 * offset
            figure_offset_3_position = rook_position[0], rook_position[1] + 3 * offset

            figure_offset_1 = Figure.get_figure(figures, figure_offset_1_position)
            figure_offset_2 = Figure.get_figure(figures, figure_offset_2_position)
            figure_offset_3 = Figure.get_figure(figures,
                                                figure_offset_3_position) if move_type == MoveType.CASTLE_LONG else None

            if position != self.initial_position:
                return
            if not figure_rook:
                return
            if figure_rook.figure_type != FigureType.ROOK:
                return
            if not figure_rook.is_able_to_castle:
                return
            if figure_offset_1:
                return
            if move_type == MoveType.CASTLE_SHORT and (self.is_check_on_position_given(
                    figure_offset_1_position, figures) or self.is_the_other_king_around(figure_offset_1_position,
                                                                                        figures)):
                return
            if figure_offset_2:
                return
            if self.is_check_on_position_given(figure_offset_2_position, figures) or self.is_the_other_king_around(
                    figure_offset_2_position, figures):
                return
            if move_type == MoveType.CASTLE_LONG and (
                    figure_offset_3 or self.is_check_on_position_given(figure_offset_3_position, figures) or
                    self.is_the_other_king_around(figure_offset_3_position, figures)):
                return

            final_king_pos = figure_offset_1_position if \
                move_type == MoveType.CASTLE_SHORT else figure_offset_2_position
            final_rook_pos = figure_offset_2_position if \
                move_type == MoveType.CASTLE_SHORT else figure_offset_3_position
            possible_moves.append(ChessMove(final_king_pos, self.position, move_type,
                                            {'rook-end-pos': final_rook_pos, 'rook': figure_rook}))

        possible_moves = []
        if self.is_able_to_castle:
            possibility_to_castle_one_side(MoveType.CASTLE_SHORT)
            possibility_to_castle_one_side(MoveType.CASTLE_LONG)
        return possible_moves

    def is_the_other_king_around(self, _pos, figures):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        for _direction in directions:
            _position_being_checked = tuple(map(sum, zip(_pos, _direction)))
            if not Figure.is_move_valid(_position_being_checked):
                continue
            figure = Figure.get_figure(figures, _position_being_checked)
            if figure:
                if figure.figure_type == FigureType.KING and figure.color != self.color:
                    return True
        return False

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        possible_moves = []
        for direction in directions:
            position_being_checked = tuple(map(sum, zip(self.position, direction)))
            if not self.is_move_valid(position_being_checked):
                continue
            figure = Figure.get_figure(figures, position_being_checked)
            if figure:
                if figure.color == self.color:
                    continue
                elif figure.figure_type == FigureType.KING:
                    print('! Two kings cannot stand next to each other')
                    continue
            previous_position = self.position
            self.move((999, 999))
            if self.is_check_on_position_given(position_being_checked, figures):
                self.move(previous_position)
                continue
            self.move(previous_position)
            if self.is_the_other_king_around(position_being_checked, figures):
                continue
            possible_moves.append(ChessMove(position_being_checked, self.position, MoveType.NORMAL))
        if self.is_able_to_castle and not self.is_check_on_position_given(self.position, figures):
            possible_moves.extend(self.possibility_to_castle(self.position, figures))
        return possible_moves

    def set_is_able_to_castle(self, val):
        self.is_able_to_castle = val
