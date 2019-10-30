import copy

import src.chess.chess_utils as ChessUtils
from src.chess.board_gui import BoardGUI
from src.chess.enums import GameStatus
from src.chess.figures import *
from src.chess.utilities import PastMove


class Chessboard:
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
        self.if_figure_selected = False
        self.check = False
        self.current_player = Color.WHITE
        self.selected_tile = None
        self.possible_moves = []
        self.figures = self.init_figures()
        self.game_status = GameStatus.IN_PROGRESS
        self.past_moves = []
        self.board_gui = BoardGUI()

    def deep_copy(self):
        rc = Chessboard()
        rc.if_figure_selected = self.if_figure_selected
        rc.current_player = self.current_player
        rc.selected_tile = self.selected_tile
        rc.check = self.check
        rc.game_status = self.game_status

        rc.possible_moves = copy.deepcopy(self.possible_moves)
        rc.figures = copy.deepcopy(self.figures)
        rc.past_moves = copy.deepcopy(self.past_moves)
        return rc

    def select_figure(self, grid_pos):
        figure = Figure.get_figure(self.figures, grid_pos)
        if figure and figure.color == self.current_player:
            self.board_gui.mark_tile_selected(grid_pos)
            self.if_figure_selected = True
            self.selected_tile = grid_pos
            self.possible_moves = figure.check_moves(self.figures)
            self.possible_moves = ChessUtils.reduce_move_range_when_check(self, figure, self.possible_moves)
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
        return figure and figure.figure_type == FigureType.KING and figure.color == self.current_player and self.check

    def deselect_figure(self):
        if self.selected_tile:
            if not self.check:
                self.board_gui.mark_tile_deselected(ChessUtils.get_king_position(self, self.current_player))
            self.board_gui.mark_tile_deselected(self.selected_tile,
                                                when_checked=self.is_king_selected_to_move_in_check())
        self.selected_tile = None
        self.possible_moves = []
        self.if_figure_selected = False

    def get_opposite_color(self):
        return Color.WHITE if self.current_player == Color.BLACK else Color.BLACK

    def switch_current_player(self):
        self.current_player = self.get_opposite_color()

    # sprawdzamy czy my szachujemy
    def check_for_check(self, color_that_causes_check):
        king_pos = ChessUtils.get_king_position(self, color_that_causes_check)
        # zakladamy ze jest krol na mapie
        king = Figure.get_figure(self.figures, king_pos)
        self.check = king.is_check_on_position_given(king_pos, self.figures)

    def do_normal_move(self, move, figure_moved):
        if (figure_moved.figure_type == FigureType.KING or figure_moved.figure_type == FigureType.ROOK) and \
                figure_moved.is_able_to_castle:
            figure_moved.set_is_able_to_castle(False)
        potential_figure = Figure.get_figure(self.figures, move.position_to)
        if potential_figure:
            Figure.remove_figure(self.figures, potential_figure)
        figure_moved.move(move.position_to)

    def do_promotion(self, move, figure_moved):
        # TODO: Grzesiek, extract it from game logic
        # while True:
        #     figure_type_chosen = input("Choose figure: (Q)ueen, (R)ook, (K)night, (B)ishop\n").lower()
        #     if figure_type_chosen in ["q", "r", "k", "b"]:
        #         break
        figure_type_chosen = "q"
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
        else:
            new_figure = Queen
        self.figures.append(new_figure(self.current_player, pos))

    def do_move(self, move):
        figure_moved = Figure.get_figure(self.figures, self.selected_tile)
        if move.move_type == MoveType.NORMAL:
            self.do_normal_move(move, figure_moved)
        elif move.move_type == MoveType.PAWN_DOUBLE_MOVE:
            ChessUtils.do_pawn_double_move(move, figure_moved)
        elif move.move_type == MoveType.EN_PASSANT:
            ChessUtils.do_en_passant_move(self, move, figure_moved)
        elif move.move_type == MoveType.PROMOTION:
            self.do_promotion(move, figure_moved)
        elif move.move_type == MoveType.CASTLE_SHORT or move.move_type == MoveType.CASTLE_LONG:
            ChessUtils.do_castling(move, figure_moved)

    def add_past_move(self, position, figures_count_before_move, old_position):
        figure = Figure.get_figure(self.figures, position)
        self.past_moves.append(
            PastMove(position, self.check, figure, len(self.figures) < figures_count_before_move, old_position))

    # grid_pos - matrix order (y, x)
    def react_to_tile_click(self, grid_pos):
        if not self.if_figure_selected:
            self.select_figure(grid_pos)
            return False
        else:
            positions_list = [x.position_to for x in self.possible_moves]
            move_index = positions_list.index(grid_pos) if grid_pos in positions_list else -1
            clicked_possible_move = move_index != -1
            if clicked_possible_move:
                self.perform_legal_move(move_index)
                return True
            else:
                if self.selected_tile:
                    self.deselect_figure()
                self.select_figure(grid_pos)
                return False

    def perform_legal_move(self, move_index):
        Pawn.clear_en_passant_capture_ability_for_one_team(self.figures, self.current_player)
        move = self.possible_moves[move_index]
        figures_count_before_move = len(self.figures)
        self.do_move(move)
        self.check_for_check(self.get_opposite_color())
        self.deselect_last_moved()
        if self.check:
            king_pos = ChessUtils.get_king_position(self, self.get_opposite_color())
            self.board_gui.mark_tile_checked(king_pos)
        selected_tile = self.selected_tile
        self.add_past_move(move.position_to, figures_count_before_move, selected_tile)
        self.deselect_figure()

        self.board_gui.mark_tile_moved(selected_tile)
        self.board_gui.mark_tile_moved(move.position_to)

        self.switch_current_player()
        self.update_game_status()

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

    def perform_raw_move(self, pos_from, pos_to):
        self.react_to_tile_click(pos_from)
        self.react_to_tile_click(pos_to)
        self.switch_current_player()
        self.update_game_status()

    def update_game_status(self):
        move_is_possible = ChessUtils.is_there_any_possible_move(self)
        if not move_is_possible:
            if self.check:
                self.game_status = \
                    GameStatus.CHECKMATE_WHITE if self.current_player == Color.BLACK else GameStatus.CHECKMATE_BLACK
            else:
                self.game_status = GameStatus.STALEMATE
            print(f'!!!\tGAME ENDED: {self.game_status}')
        elif self.is_there_a_draw():
            print(f'!!!\tGAME ENDED: {self.game_status}')
