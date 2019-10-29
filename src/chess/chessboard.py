from src.chess.board_gui import BoardGUI
from src.chess.enums import MoveStatus, GameStatus
from src.chess.figures import *
from src.chess.utilities import PastMove


class Chessboard:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    @staticmethod
    def init_figures():
        figures = [Rook(Color.WHITE, (0, 0)), Knight(Color.WHITE, (0, 1)), Bishop(Color.WHITE, (0, 2)),
                   Queen(Color.WHITE, (0, 3)), King(Color.WHITE, (0, 4)), Bishop(Color.WHITE, (0, 5)),
                   Knight(Color.WHITE, (0, 6)), Rook(Color.WHITE, (0, 7)), Rook(Color.BLACK, (7, 0)),
                   Knight(Color.BLACK, (7, 1)), Bishop(Color.BLACK, (7, 2)), Queen(Color.BLACK, (7, 3)),
                   King(Color.BLACK, (7, 4)), Bishop(Color.BLACK, (7, 5)), Knight(Color.BLACK, (7, 6)),
                   Rook(Color.BLACK, (7, 7))]
        for i in range(8):
            figures.append(Pawn(Color.WHITE, (1, i)))
            figures.append(Pawn(Color.BLACK, (6, i)))
        return figures

    def __init__(self):
        self.move_status = MoveStatus.FIGURE_NOT_SELECTED
        self.move_color = Color.WHITE
        self.selected_tile = None
        self.possible_moves = []
        self.check = False
        self.figures = self.init_figures()
        self.move_was_executed = False
        self.game_status = GameStatus.IN_PROGRESS
        self.past_moves = []
        self.board_gui = BoardGUI()

    def select_figure(self, grid_pos):
        figure = Figure.get_figure(self.figures, grid_pos)
        if figure and figure.color == self.move_color:
            self.board_gui.mark_tile_selected(grid_pos)
            self.move_status = MoveStatus.FIGURE_SELECTED
            self.selected_tile = grid_pos
            self.possible_moves = figure.check_moves(self.figures)
            self.possible_moves = self.reduce_move_range_when_check(figure, self.possible_moves)
        else:
            self.deselect_figure()

    def deselect_last_moved(self):
        if not self.past_moves:
            return
        tile_1 = self.past_moves[-1].position
        tile_2 = self.past_moves[-1].old_position
        self.board_gui.mark_tile_deselected(tile_1)
        self.board_gui.mark_tile_deselected(tile_2)

    def is_king_selected_to_move_in_check(self):
        figure = Figure.get_figure(self.figures, self.selected_tile)
        return figure and figure.figure_type == FigureType.KING and figure.color == self.move_color and self.check

    def deselect_figure(self):
        if self.selected_tile:
            if not self.check:
                self.board_gui.mark_tile_deselected(self.get_king_position(self.move_color))
            self.board_gui.mark_tile_deselected(self.selected_tile, when_checked=self.is_king_selected_to_move_in_check())
        self.selected_tile = None
        self.possible_moves = []
        self.move_status = MoveStatus.FIGURE_NOT_SELECTED

    def get_opposite_color(self):
        return Color.WHITE if self.move_color == Color.BLACK else Color.BLACK

    def change_turn(self):
        self.move_color = self.get_opposite_color()

    def get_king_position(self, color):
        king = next((x for x in self.figures if x.figure_type == FigureType.KING and x.color == color), None)
        return king.position if king else None

    # sprawdzamy czy my szachujemy
    def check_for_check(self, color_that_causes_check):
        king_pos = self.get_king_position(color_that_causes_check)
        # zakladamy ze jest krol na mapie
        king = Figure.get_figure(self.figures, king_pos)
        self.check = king.is_check_on_position_given(king_pos, self.figures)

    def do_normal_move(self, move, figure_moved):
        if (figure_moved.figure_type == FigureType.KING or figure_moved.figure_type == FigureType.ROOK) and \
                figure_moved.is_able_to_castle:
            figure_moved.set_is_able_to_castle(False)
        potential_figure = Figure.get_figure(self.figures, move.position)
        if potential_figure:
            Figure.remove_figure(self.figures, potential_figure)
        figure_moved.move(move.position)

    def do_pawn_double_move(self, move, figure_moved):
        figure_moved.set_can_be_captured_en_passant(True)
        figure_moved.move(move.position)

    def do_en_passant_move(self, move, figure_moved):
        figure_moved.move(move.position)
        Figure.remove_figure_on_position(self.figures, move.help_dict['opponent-pawn-pos'])

    def do_promotion(self, move, figure_moved):
        while True:
            figure_type_chosen = input("Choose figure: (Q)ueen, (R)ook, (K)night, (B)ishop\n").lower()
            if figure_type_chosen in ["q", "r", "k", "b"]:
                break
        print(figure_type_chosen)
        self.do_normal_move(move, figure_moved)
        pos = figure_moved.position
        Figure.remove_figure(self.figures, figure_moved)
        if figure_type_chosen == "q":
            new_figure = Queen
        elif figure_type_chosen == "r":
            new_figure = Rook
        elif figure_type_chosen == "k":
            new_figure = Knight
        elif figure_type_chosen == "b":
            new_figure = Bishop
        self.figures.append(new_figure(self.move_color, pos))

    def do_castling(self, move, figure_moved):
        figure_moved.move(move.position)
        rook = move.help_dict['rook']
        rook.move(move.help_dict['rook-end-pos'])
        figure_moved.set_is_able_to_castle(False)
        rook.set_is_able_to_castle(False)

    def do_move(self, move):
        figure_moved = Figure.get_figure(self.figures, self.selected_tile)
        if move.move_type == MoveType.NORMAL:
            self.do_normal_move(move, figure_moved)
        elif move.move_type == MoveType.PAWN_DOUBLE_MOVE:
            self.do_pawn_double_move(move, figure_moved)
        elif move.move_type == MoveType.EN_PASSANT:
            self.do_en_passant_move(move, figure_moved)
        elif move.move_type == MoveType.PROMOTION:
            self.do_promotion(move, figure_moved)
        elif move.move_type == MoveType.CASTLE_SHORT or move.move_type == MoveType.CASTLE_LONG:
            self.do_castling(move, figure_moved)

    def add_past_move(self, position, figures_count_before_move, old_position):
        figure = Figure.get_figure(self.figures, position)
        self.past_moves.append(
            PastMove(position, self.check, figure, len(self.figures) < figures_count_before_move, old_position))

    # grid_pos - matrix order (y, x)
    def decide_move_action(self, grid_pos):
        # choose figure
        if self.move_status == MoveStatus.FIGURE_NOT_SELECTED:
            self.select_figure(grid_pos)

        else:
            positions_list = [x.position for x in self.possible_moves]
            move_index = positions_list.index(grid_pos) if grid_pos in positions_list else -1
            if move_index != -1:
                Pawn.clear_en_passant_capture_ability_for_one_team(self.figures, self.move_color)
                move = self.possible_moves[move_index]
                figures_count_before_move = len(self.figures)
                self.do_move(move)
                self.check_for_check(self.get_opposite_color())
                print("CZY JEST SZACH: " + str(self.check))
                self.deselect_last_moved()
                if self.check:
                    king_pos = self.get_king_position(self.get_opposite_color())
                    self.board_gui.mark_tile_checked(king_pos)
                selected_tile = self.selected_tile
                self.add_past_move(move.position, figures_count_before_move, selected_tile)
                self.deselect_figure()
                self.board_gui.mark_tile_moved(selected_tile)
                self.board_gui.mark_tile_moved(move.position)
                self.change_turn()
                self.move_was_executed = True
                self.check_and_set_game_status()
                print('now moving ' + str(self.move_color) + '\n')
            else:
                # figure select exchange
                if self.selected_tile:
                    self.deselect_figure()
                self.select_figure(grid_pos)

    def is_there_any_possible_move(self):
        for figure in self.figures:
            if figure.color != self.move_color:
                continue
            possible_moves = figure.check_moves(self.figures)
            possible_moves_reduced = self.reduce_move_range_when_check(figure, possible_moves)
            if possible_moves_reduced:
                return True
        return False

    def reduce_move_range_when_check(self, figure, moves):
        reduced_moves = []
        for move in moves:
            previous_position = figure.position
            potential_figure = Figure.get_figure(self.figures, move.position)
            if potential_figure:
                Figure.remove_figure(self.figures, potential_figure)
            figure.move(move.position)
            king_pos = self.get_king_position(self.move_color)
            king = Figure.get_figure(self.figures, king_pos)
            if not king.is_check_on_position_given(king_pos, self.figures):
                reduced_moves.append(move)
            figure.move(previous_position)
            if potential_figure:
                self.figures.append(potential_figure)
        # print(moves)
        # print(reduced_moves)
        return reduced_moves

    def are_the_figures_left_capable_of_checkmate(self):
        figures_left_count = len(self.figures)
        if figures_left_count > 4:
            return True
        if figures_left_count == 2:
            return False
        figures_except_kings = list(filter(lambda x: x.figure_type != FigureType.KING, self.figures))
        if len(figures_except_kings) == 1:
            return not (figures_except_kings[0].figure_type == FigureType.KNIGHT or figures_except_kings[
                0].figure_type == FigureType.BISHOP)
        figure_1 = figures_except_kings[0]
        figure_2 = figures_except_kings[1]
        if figure_1.figure_type == FigureType.BISHOP and figure_2.figure_type == FigureType.BISHOP and \
                figure_1.color != figure_2.color and figure_1.light_squared == figure_2.light_squared:
            return False
        return True

    def is_fifty_move_rule(self):
        if len(self.past_moves) < 100:
            return False
        for past_move in self.past_moves[::-1][:100]:
            if past_move.was_capture or past_move.figure_moved.figure_type == FigureType.PAWN:
                return False
        return True

    def is_there_a_draw(self):
        if not self.are_the_figures_left_capable_of_checkmate():
            self.game_status = GameStatus.DRAW
            return True
        if self.is_fifty_move_rule():
            self.game_status = GameStatus.FIFTY_MOVE_RULE
            return True
        return False

    def check_and_set_game_status(self):
        if self.move_was_executed:
            self.move_was_executed = False
            move_is_possible = self.is_there_any_possible_move()
            if not move_is_possible:
                if self.check:
                    self.game_status = \
                        GameStatus.CHECKMATE_WHITE if self.move_color == Color.BLACK else GameStatus.CHECKMATE_BLACK
                else:
                    self.game_status = GameStatus.STALEMATE
                print('=' * 50)
                print(f'!!!\tGAME ENDED: {self.game_status}')
                print('=' * 50)
            elif self.is_there_a_draw():
                print('=' * 50)
                print(f'!!!\tGAME ENDED: {self.game_status}')
                print('=' * 50)
