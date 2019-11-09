from abc import ABC, abstractmethod
from numpy import zeros

from src.chess.algorithm_relay.chess_move import ChessMove
from src.chess.enums import FigureType, Color, MoveType
from src.chess.figures_collection import ChessFiguresCollection


class Figure(ABC):
    def __init__(self, color, figure_type, image_file, position):
        self.color = color
        self.figure_type = figure_type
        self.image_file = image_file
        self.position = position
        super().__init__()

    @abstractmethod
    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        pass

    @staticmethod
    def is_move_valid(move_pos):
        return 0 <= move_pos[0] <= 7 and 0 <= move_pos[1] <= 7

    @staticmethod
    def get_figure(figures: ChessFiguresCollection, position):
        return figures.get_figure_at(position)

    @staticmethod
    def remove_figure_on_position(figures: ChessFiguresCollection, position):
        figures.remove_figure_at(position)

    @staticmethod
    def remove_figure(figures: ChessFiguresCollection, figure):
        figures.remove(figure)


class FigureWithLinearMovement(Figure):
    @abstractmethod
    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        pass

    def check_moves_linear(self, figures: ChessFiguresCollection, directions, threat_for_king=False):
        possible_moves = []
        for direction in directions:
            pos_being_checked = (self.position[0] + direction[0], self.position[1] + direction[1])
            while self.is_move_valid(pos_being_checked):
                figure = self.get_figure(figures, pos_being_checked)
                if figure:
                    if figure.color != self.color or threat_for_king:
                        possible_moves.append(ChessMove(pos_being_checked, self.position, MoveType.NORMAL))
                    break
                possible_moves.append(ChessMove(pos_being_checked, self.position, MoveType.NORMAL))
                pos_being_checked = (pos_being_checked[0] + direction[0], pos_being_checked[1] + direction[1])
        return possible_moves


class Pawn(Figure):
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
        self.can_be_captured_en_passant = val

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        possible_moves = []
        move_setup = Pawn.MOVE_SETUPS[self.color]

        # pawn at the end - should not happen
        if self.position[0] == move_setup["last_line"]:
            print('! Pawn should not be allowed to stay in the end line')
        else:
            pos = move_setup["step_forward"](self.position[0], 1), self.position[1]
            figure = Figure.get_figure(figures, pos)
            if not figure:
                if pos[0] != move_setup["last_line"]:
                    move = ChessMove(pos, self.position, MoveType.NORMAL)
                else:
                    move = ChessMove(pos, self.position, MoveType.PROMOTION)
                possible_moves.append(move)
                # double move at the beginning
                double_move = move_setup["step_forward"](self.position[0], 2), self.position[1]
                if self.position[0] == move_setup["start_line"] and not Figure.get_figure(figures, double_move):
                    possible_moves.append(ChessMove(double_move, self.position, MoveType.PAWN_DOUBLE_MOVE))
            possible_moves.extend(self.check_captures(figures, threat_for_king))
        return possible_moves

    def check_captures(self, figures: ChessFiguresCollection, threat_for_king=False):
        def move_diagonally(_pos, color):
            move_setup = Pawn.MOVE_SETUPS[self.color]
            opposite_color = Color.BLACK if color == Color.WHITE else Color.WHITE
            if not self.is_move_valid(_pos):
                return None
            figure = Figure.get_figure(figures, _pos)
            if figure:
                if figure.color == opposite_color or threat_for_king:
                    # if figure.figure_type == FigureType.KING and figure.color == opposite_color:
                    #     print('! Capture of a king should not be possible')
                    return MoveType.NORMAL if _pos[0] != move_setup["last_line"] else MoveType.PROMOTION
            elif threat_for_king:
                return MoveType.NORMAL if _pos[0] != move_setup["last_line"] else MoveType.PROMOTION
            # capture en passant
            else:
                opponent_pawn_pos = (move_setup["step_backward"](_pos[0], 1), _pos[1])
                figure = Figure.get_figure(figures, opponent_pawn_pos)
                if not figure:
                    return None
                if self.position[0] == move_setup["step_backward"](move_setup["last_line"], 3) and \
                        figure.figure_type == FigureType.PAWN and \
                        figure.color == opposite_color and \
                        figure.can_be_captured_en_passant:
                    return MoveType.EN_PASSANT
            return None

        def check_capture_on_one_side(pos_height, color):
            move_setup = Pawn.MOVE_SETUPS[self.color]
            _pos = move_setup["step_forward"](self.position[0], 1), pos_height
            move_type = move_diagonally(_pos, color)
            if move_type:
                if move_type == MoveType.NORMAL or move_type == MoveType.PROMOTION:
                    possible_captures.append(ChessMove(_pos, self.position, move_type))
                elif move_type == MoveType.EN_PASSANT:
                    possible_captures.append(
                        ChessMove(_pos, self.position, move_type,
                                  {'opponent-pawn-pos': (self.position[0], pos_height)}))

        possible_captures = []
        if self.position[1] > 0:
            check_capture_on_one_side(self.position[1] - 1, self.color)
        if self.position[1] < 7:
            check_capture_on_one_side(self.position[1] + 1, self.color)
        return possible_captures

    @staticmethod
    def clear_en_passant_capture_ability_for_one_team(figures: ChessFiguresCollection, color):
        for figure in figures.figures_list:
            if figure.figure_type == FigureType.PAWN and color == figure.color:
                figure.set_can_be_captured_en_passant(False)


class Knight(Figure):
    def __init__(self, color, position):
        self.value = 3
        image_file = 'knight-white.png' if color == Color.WHITE else 'knight-black.png'
        super().__init__(color, FigureType.KNIGHT, image_file, position)

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        def wipe_out_bad_moves(move_positions):
            toret = []
            for move_position in move_positions:
                if not self.is_move_valid(move_position):
                    continue
                figure = Figure.get_figure(figures, move_position)
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
        return wipe_out_bad_moves(possible_moves_positions)


class Bishop(FigureWithLinearMovement):
    def __init__(self, color, position):
        self.value = 3
        self.light_squared = (position[0] + position[1]) % 2 == 1
        image_file = 'bishop-white.png' if color == Color.WHITE else 'bishop-black.png'
        super().__init__(color, FigureType.BISHOP, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.check_moves_linear(figures, directions, threat_for_king)


class Rook(FigureWithLinearMovement):
    def __init__(self, color, position):
        self.value = 5
        self.is_able_to_castle = True
        image_file = 'rook-white.png' if color == Color.WHITE else 'rook-black.png'
        super().__init__(color, FigureType.ROOK, image_file, position)

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        return self.check_moves_linear(figures, directions, threat_for_king)

    def set_is_able_to_castle(self, val):
        self.is_able_to_castle = val


class Queen(FigureWithLinearMovement):
    def __init__(self, color, position):
        self.value = 9
        image_file = 'queen-white.png' if color == Color.WHITE else 'queen-black.png'
        super().__init__(color, FigureType.QUEEN, image_file, position)

    def check_moves(self, figures, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        return self.check_moves_linear(figures, directions, threat_for_king)


class King(Figure):
    def __init__(self, color, position):
        self.is_able_to_castle = True
        self.initial_position = (0, 4) if color == Color.WHITE else (7, 4)
        self.check_mask = zeros(shape=(8, 8), dtype=bool)
        self.value = 0
        image_file = 'king-white.png' if color == Color.WHITE else 'king-black.png'
        super().__init__(color, FigureType.KING, image_file, position)

    def update_check_mask_around_rival_king(self, figures: ChessFiguresCollection):
        opposite_color = Color.WHITE if self.color == Color.BLACK else Color.BLACK
        rival_king_position = figures.get_king_position(opposite_color)
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        for direction in directions:
            position_being_checked = rival_king_position[0] + direction[0], rival_king_position[1] + direction[1]
            if self.is_move_valid(position_being_checked):
                self.check_mask[position_being_checked] = True
        self.check_mask[rival_king_position] = True

    def reset_check_mask(self):
        self.check_mask = zeros(shape=(8, 8), dtype=bool)

    def update_check_mask_by_given_moves(self, moves):
        for move in moves:
            self.check_mask[move.position_to] = True

    # check if at least one of all possible rival's moves coincide with 'position';
    def update_check_mask(self, figures: ChessFiguresCollection):
        self.reset_check_mask()
        previous_position = self.position
        figures.temporarily_disable(self)

        self.update_check_mask_around_rival_king(figures)

        for figure in figures.figures_list:
            attacked_fields = []
            # only look for checks from the opposite color
            if figure.color == self.color:
                continue
            # pawns have different capture rules
            if figure.figure_type == FigureType.PAWN:
                attacked_fields = figure.check_captures(figures, True)
            # to avoid recursion
            elif figure.figure_type != FigureType.KING:
                attacked_fields = figure.check_moves(figures, True)

            if attacked_fields:
                self.update_check_mask_by_given_moves(attacked_fields)
        figures.restore(self, previous_position)

    def possibility_to_castle(self, figures: ChessFiguresCollection):
        def possibility_to_castle_one_side(move_type):
            if self.position != self.initial_position:
                return

            if move_type == MoveType.CASTLE_SHORT:
                rook_position = (0, 7) if self.color == Color.WHITE else (7, 7)
                offset = -1
            else:
                rook_position = (0, 0) if self.color == Color.WHITE else (7, 0)
                offset = 1
            figure_rook = Figure.get_figure(figures, rook_position)

            if not figure_rook:
                return
            if figure_rook.figure_type != FigureType.ROOK:
                return
            if not figure_rook.is_able_to_castle:
                return

            figure_offset_1_position = rook_position[0], rook_position[1] + offset
            figure_offset_2_position = rook_position[0], rook_position[1] + 2 * offset
            figure_offset_3_position = rook_position[0], rook_position[1] + 3 * offset

            figure_offset_1 = Figure.get_figure(figures, figure_offset_1_position)
            figure_offset_2 = Figure.get_figure(figures, figure_offset_2_position)
            figure_offset_3 = Figure.get_figure(figures,
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
            possibility_to_castle_one_side(MoveType.CASTLE_SHORT)
            possibility_to_castle_one_side(MoveType.CASTLE_LONG)
        return possible_moves

    def check_moves(self, figures: ChessFiguresCollection, threat_for_king=False):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, -1), (0, 1)]
        possible_moves = []
        for direction in directions:
            position_being_checked = self.position[0] + direction[0], self.position[1] + direction[1]
            if not self.is_move_valid(position_being_checked):
                continue
            figure = Figure.get_figure(figures, position_being_checked)
            if figure:
                if figure.color == self.color:
                    continue
                elif figure.figure_type == FigureType.KING:
                    print('! Two kings cannot stand next to each other')
                    continue
            if not self.check_mask[position_being_checked]:
                possible_moves.append(ChessMove(position_being_checked, self.position, MoveType.NORMAL))
        if self.is_able_to_castle and not self.check_mask[self.position]:
            possible_moves.extend(self.possibility_to_castle(figures))
        return possible_moves

    def set_is_able_to_castle(self, val):
        self.is_able_to_castle = val
