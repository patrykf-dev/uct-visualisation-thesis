from itertools import chain

from src.chess.enums import Color, FigureType
from src.chess.figures import Figure


def do_pawn_double_move(move, figure_moved):
    figure_moved.set_can_be_captured_en_passant(True)
    figure_moved.move(move.position_to)


def do_en_passant_move(board, move, figure_moved):
    figure_moved.move(move.position_to)
    Figure.remove_figure_on_position(board.figures, move.help_dict['opponent-pawn-pos'])


def do_castling(move, figure_moved):
    figure_moved.move(move.position)
    rook = move.help_dict['rook']
    rook.move(move.help_dict['rook-end-pos'])
    figure_moved.set_is_able_to_castle(False)
    rook.set_is_able_to_castle(False)


def get_all_possible_moves(board):
    all_possible_moves = []
    print(f"Current move color: {board.current_player}")
    for figure in board.figures:
        if figure.color == board.current_player:
            continue
        possible_moves = figure.check_moves(board.figures)
        possible_moves_reduced = reduce_move_range_when_check(figure, possible_moves)

        for move in possible_moves_reduced:
            if board.current_player == Color.WHITE:
                move.player = 2
            else:
                move.player = 1

        if possible_moves_reduced:
            all_possible_moves.append(possible_moves_reduced)
    return list(chain.from_iterable(all_possible_moves))


def reduce_move_range_when_check(board, figure, moves):
    reduced_moves = []
    for move in moves:
        previous_position = figure.position
        potential_figure = Figure.get_figure(board.figures, move.position_to)
        if potential_figure:
            Figure.remove_figure(board.figures, potential_figure)
        figure.move(move.position_to)
        king_pos = get_king_position(board, board.current_player)
        king = Figure.get_figure(board.figures, king_pos)
        if not king.is_check_on_position_given(king_pos, board.figures):
            reduced_moves.append(move)
        figure.move(previous_position)
        if potential_figure:
            board.figures.append(potential_figure)
    return reduced_moves


def get_king_position(board, color):
    king = next((x for x in board.figures if x.figure_type == FigureType.KING and x.color == color), None)
    return king.position if king else None


def is_there_any_possible_move(board):
    for figure in board.figures:
        if figure.color != board.current_player:
            continue
        possible_moves = figure.check_moves(board.figures)
        possible_moves_reduced = reduce_move_range_when_check(board, figure, possible_moves)
        if possible_moves_reduced:
            return True
    return False
