import copy
from multiprocessing import Pool, cpu_count
from itertools import chain

from src.chess.chessboard import Chessboard
from src.chess.enums import GameStatus
from src.chess.figures import *


class PastMove:
    def __init__(self, position_to, was_check, figure_moved, was_capture, position_from):
        self.position_to = position_to
        self.was_check = was_check
        self.figure_moved = figure_moved
        self.was_capture = was_capture
        self.position_from = position_from

    def __str__(self):
        return f'Move {self.figure_moved} to: {self.position_to}, check: {self.was_check}, capture: {self.was_capture}'


def do_pawn_double_move(board: Chessboard, move: ChessMove, figure_moved):
    figure_moved.set_can_be_captured_en_passant(True)
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)


def do_en_passant_move(board: Chessboard, move: ChessMove, figure_moved: Figure):
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)
    Figure.remove_figure_on_position(board.figures, move.help_dict['opponent-pawn-pos'])


def do_castling(board: Chessboard, move: ChessMove, figure_moved: Figure):
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)  # TODO to or from?
    rook = move.help_dict['rook']
    board.figures.move_figure_to(rook, move.help_dict['rook-end-pos'])
    figure_moved.set_is_able_to_castle(False)
    rook.set_is_able_to_castle(False)


def is_fifty_move_rule(board: Chessboard):
    if len(board.past_moves) < 100:
        return False
    for past_move in board.past_moves[::-1][:100]:
        if past_move.was_capture or past_move.figure_moved.figure_type == FigureType.PAWN:
            return False
    return True


def is_there_a_draw(board: Chessboard):
    if not are_the_figures_left_capable_of_checkmate(board):
        board.game_status = GameStatus.DRAW
        return True
    if is_fifty_move_rule(board):
        board.game_status = GameStatus.FIFTY_MOVE_RULE
        return True
    return False


def process_func(args):
    figure, board = args
    figure_moves = figure.check_moves(board.figures)
    reduce_move_range_when_check(board, figure, figure_moves)

    for move in figure_moves:
        move.player = get_player_from_color(board.current_player_color)

        f_color = str(figure.color).split(".")[1].lower()
        f_type = str(figure.figure_type).split(".")[1].lower()
        move.description = f"{f_color} {f_type} {move.position_from} -> {move.position_to}"

    return figure_moves


def get_all_possible_moves(board: Chessboard):
    figure_list_current_color = [fig for fig in board.figures.figures_list if board.current_player_color == fig.color]
    parallel_calls = cpu_count()
    pool = Pool(processes=parallel_calls)
    args = [(figure, copy.deepcopy(board)) for figure in figure_list_current_color]

    all_possible_moves = []
    situations_number = len(args)
    counter = 0
    while counter <= situations_number:
        real_args = args[counter: counter + parallel_calls]
        possible_moves = pool.map(process_func, real_args)
        all_possible_moves.extend(possible_moves)
        counter += parallel_calls
    pool.close()

    all_possible_moves = list(chain(*all_possible_moves))
    return all_possible_moves


def take_off_potential_figure(board: Chessboard, move: ChessMove):
    figure = board.figures.get_figure_at(move.position_to)
    list_index = 0
    if figure:
        list_index = Figure.remove_figure(board.figures, figure)
    elif move.move_type == MoveType.EN_PASSANT:
        opponent_figure_position = move.help_dict['opponent-pawn-pos']
        figure = board.figures.get_figure_at(opponent_figure_position)
        list_index = Figure.remove_figure(board.figures, figure)
    return figure, list_index


def put_back_potential_figure(board: Chessboard, figure: Figure, figure_index):
    if figure:
        board.figures.add_figure(figure, figure_index)


def reduce_move_range_when_check(board: Chessboard, figure: Figure, moves):
    bad_moves = []
    figs = board.figures
    king = figs.get_king(board.current_player_color)
    previous_position = figure.position
    for i in range(len(moves)):
        move = moves[i]
        potential_figure, figure_index = take_off_potential_figure(board, move)
        figs.move_figure_to(figure, move.position_to)
        king.update_check_mask(figs)
        if king.check_mask[king.position]:
            bad_moves.append(i)
        figs.move_figure_to(figure, previous_position)
        put_back_potential_figure(board, potential_figure, figure_index)

    for bad_move in bad_moves[::-1]:
        moves.pop(bad_move)


def is_king_selected_to_move_in_check(board: Chessboard, selected_tile):
    figure = board.figures.get_figure_at(selected_tile)
    return figure and figure.figure_type == FigureType.KING and figure.color == board.current_player_color and board.check


def get_king_position(board: Chessboard, color: Color):
    return board.figures.get_king_position(color)


def do_normal_move(board: Chessboard, move, figure_moved: Figure):
    if (figure_moved.figure_type == FigureType.KING or figure_moved.figure_type == FigureType.ROOK) and \
            figure_moved.is_able_to_castle:
        figure_moved.set_is_able_to_castle(False)
    potential_figure = board.figures.get_figure_at(move.position_to)
    if potential_figure:
        Figure.remove_figure(board.figures, potential_figure)
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)


def do_promotion(board: Chessboard, move, figure_moved: Figure):
    # TODO: Grzesiek, extract it from game logic
    # while True:
    #     figure_type_chosen = input("Choose figure: (Q)ueen, (R)ook, (K)night, (B)ishop\n").lower()
    #     if figure_type_chosen in ["q", "r", "k", "b"]:
    #         break
    figure_type_chosen = "q"
    do_normal_move(board, move, figure_moved)
    pos = figure_moved.position
    Figure.remove_figure(board.figures, figure_moved)
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
    board.figures.add_figure(new_figure(board.current_player_color, pos))


def are_the_figures_left_capable_of_checkmate(board: Chessboard):
    figures_left_count = len(board.figures.figures_list)
    if figures_left_count > 4:
        return True
    if figures_left_count == 2:
        return False
    figures_except_kings = list(filter(lambda x: x.figure_type != FigureType.KING, board.figures.figures_list))
    if len(figures_except_kings) == 1:
        return not (figures_except_kings[0].figure_type == FigureType.KNIGHT or figures_except_kings[
            0].figure_type == FigureType.BISHOP)
    figure_1 = figures_except_kings[0]
    figure_2 = figures_except_kings[1]
    if figure_1.figure_type == FigureType.BISHOP and figure_2.figure_type == FigureType.BISHOP and \
            figure_1.color != figure_2.color and figure_1.light_squared == figure_2.light_squared:
        return False
    return True


def is_there_any_possible_move(board: Chessboard):
    for figure in board.figures.figures_list:
        if figure.color != board.current_player_color:
            continue

        possible_moves = figure.check_moves(board.figures)
        reduce_move_range_when_check(board, figure, possible_moves)
        if possible_moves:
            return True
    return False


def get_player_from_color(color: Color):
    return 1 if color == Color.WHITE else 2
