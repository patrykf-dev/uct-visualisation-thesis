from itertools import chain

from src.chess.chessboard import Chessboard
from src.chess.enums import GameStatus
from src.chess.figures import *


def do_pawn_double_move(move: ChessMove, figure_moved):
    figure_moved.set_can_be_captured_en_passant(True)
    figure_moved.move(move.position_to)


def do_en_passant_move(board: Chessboard, move: ChessMove, figure_moved: Figure):
    figure_moved.move(move.position_to)
    Figure.remove_figure_on_position(board.figures, move.help_dict['opponent-pawn-pos'])


def do_castling(move: ChessMove, figure_moved: Figure):
    figure_moved.move(move.position_to)  # TODO to or from?
    rook = move.help_dict['rook']
    rook.move(move.help_dict['rook-end-pos'])
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


def get_all_possible_moves(board: Chessboard):
    all_possible_moves = []
    for figure in board.figures:
        if figure.color != board.current_player_color:
            continue
        possible_moves = figure.check_moves(board.figures)
        possible_moves_reduced = reduce_move_range_when_check(board, figure, possible_moves)

        for move in possible_moves_reduced:
            move.player = get_player_from_color(board.current_player_color)

        if possible_moves_reduced:
            all_possible_moves.append(possible_moves_reduced)
    return list(chain.from_iterable(all_possible_moves))


def reduce_move_range_when_check(board: Chessboard, figure: Figure, moves):
    reduced_moves = []
    for move in moves:
        previous_position = figure.position
        potential_figure = Figure.get_figure(board.figures, move.position_to)
        if potential_figure:
            Figure.remove_figure(board.figures, potential_figure)
        figure.move(move.position_to)
        king_pos = get_king_position(board, board.current_player_color)
        king = Figure.get_figure(board.figures, king_pos)
        if not king.is_check_on_position_given(king_pos, board.figures):
            reduced_moves.append(move)
        figure.move(previous_position)
        if potential_figure:
            board.figures.append(potential_figure)
    return reduced_moves


def is_king_selected_to_move_in_check(board: Chessboard, selected_tile):
    figure = Figure.get_figure(board.figures, selected_tile)
    return figure and figure.figure_type == FigureType.KING and figure.color == board.current_player_color and board.check


def get_king_position(board: Chessboard, color : Color):
    king = next((x for x in board.figures if x.figure_type == FigureType.KING and x.color == color), None)
    return king.position if king else None


def do_normal_move(board: Chessboard, move, figure_moved: Figure):
    if (figure_moved.figure_type == FigureType.KING or figure_moved.figure_type == FigureType.ROOK) and \
            figure_moved.is_able_to_castle:
        figure_moved.set_is_able_to_castle(False)
    potential_figure = Figure.get_figure(board.figures, move.position_to)
    if potential_figure:
        Figure.remove_figure(board.figures, potential_figure)
    figure_moved.move(move.position_to)


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
    board.figures.append(new_figure(board.current_player_color, pos))


def are_the_figures_left_capable_of_checkmate(board: Chessboard):
    figures_left_count = len(board.figures)
    if figures_left_count > 4:
        return True
    if figures_left_count == 2:
        return False
    figures_except_kings = list(filter(lambda x: x.figure_type != FigureType.KING, board.figures))
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
    for figure in board.figures:
        if figure.color != board.current_player_color:
            continue
        possible_moves = figure.check_moves(board.figures)
        possible_moves_reduced = reduce_move_range_when_check(board, figure, possible_moves)
        if possible_moves_reduced:
            return True
    return False


def get_player_from_color(color: Color):
    return 1 if color == Color.WHITE else 2
