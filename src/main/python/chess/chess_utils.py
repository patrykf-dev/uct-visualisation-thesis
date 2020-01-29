
import copy

from chess.chessboard import Chessboard
from chess.enums import GameStatus
from chess.figures import *


class PastMove:
    """
    CLass is responsible for keeping information about moves already done.
    """
    def __init__(self, position_to, was_check, figure_moved, was_capture, position_from):
        self.position_to = position_to
        self.was_check = was_check
        self.figure_moved = figure_moved
        self.was_capture = was_capture
        self.position_from = position_from

    def __str__(self):
        return f'Move {self.figure_moved} to: {self.position_to}, check: {self.was_check}, capture: {self.was_capture}'


def do_pawn_double_move(board: Chessboard, move: ChessMove, figure_moved):
    """
    Function makes a pawn do double move and exposes it to be captured en passant.

		Args:
			board:  Chessboard object
			move:  ChessMove object
			figure_moved:  Figure object

		Returns:
			None    
		"""
    figure_moved.set_can_be_captured_en_passant(True)
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)


def do_en_passant_move(board: Chessboard, move: ChessMove, figure_moved: Figure):
    """
    Function does an en passant pawn capture. It uses 'opponent-pawn-pos' key from move.help_dict.

		Args:
			board:  Chessboard object
			move:  ChessMove object
			figure_moved:  Figure object

		Returns:
			None    
		"""
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)
    Figure.remove_figure_on_position(board.figures, move.help_dict['opponent-pawn-pos'])


def do_castling(board: Chessboard, move: ChessMove, figure_moved: Figure):
    """
    Function does long or short castling. It uses 'rook' and 'rook-end-pos' keys from move.help_dict.

		Args:
			board:  Chessboard object
			move:  ChessMove object
			figure_moved:  Figure object

		Returns:
			None    
		"""
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)
    rook = move.help_dict['rook']
    board.figures.move_figure_to(rook, move.help_dict['rook-end-pos'])
    figure_moved.set_is_able_to_castle(False)
    rook.set_is_able_to_castle(False)


def is_fifty_move_rule(board: Chessboard):
    """
    Checks whether the fifty-move rule has occurred. This is a situation, where in the 50 past moves not happened a move
    that would push the game forward, e.g. capture, pawn move. This situation means a draw.

		Args:
			board:  Chessboard object

		Returns:
			bool    
		"""
    if len(board.past_moves) < 100:
        return False
    for past_move in board.past_moves[::-1][:100]:
        if past_move.was_capture or past_move.figure_moved.figure_type == FigureType.PAWN:
            return False
    return True


def is_there_a_draw(board: Chessboard):
    """
    Checks whether the game ended in draw if:
    - there are no figures left that are capable of checkmate
    - fifty-move rule occurred

		Args:
			board:  Chessboard object

		Returns:
			bool    
		"""
    if not are_the_figures_left_capable_of_checkmate(board):
        board.game_status = GameStatus.DRAW
        return True
    if is_fifty_move_rule(board):
        board.game_status = GameStatus.FIFTY_MOVE_RULE
        return True
    return False


def get_all_possible_moves(board: Chessboard):
    """
    The function extracts all the possible moves from each figure of current moving player.
    Each move gets description and player assigned.

		Args:
			board:  Chessboard object

		Returns:
			list of all possible moves (ChessMove objects)    
		"""
    all_possible_moves = []
    figures_list = board.figures.figures_list
    copied_figures_list = copy.deepcopy(board.figures.figures_list)
    for i, copied_figure in enumerate(copied_figures_list):
        if figures_list[i].color != board.current_player_color:
            continue

        figure_moves = figures_list[i].check_moves(board.figures)
        reduce_move_range_when_check(board, figures_list[i], figure_moves)

        for j, move in enumerate(figure_moves):
            move.player = get_player_from_color(board.current_player_color)
            f_color = str(copied_figure.color).split(".")[1].lower()
            f_type = str(copied_figure.figure_type).split(".")[1].lower()
            move.description = f"{f_color} {f_type} {move.real_position_from()} -> {move.real_position_to()}"
            s_state = str(board.game_status).split(".")[1].lower()
            figure_moves[j] = (move, s_state)

        if figure_moves:
            all_possible_moves.extend(figure_moves)

    return all_possible_moves


def take_off_potential_figure(board: Chessboard, move: ChessMove):
    """
    Takes of figure from chessboard by given move position. If the move was en passant capture - it takes off the
    captured pawn.

		Args:
			board:  Chessboard object
			move:  ChessMove object

		Returns:
			tuple of 2 values: removed figure, index in figure list where it was placed    
		"""
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
    """
    Puts a figure back into the chessboard's figures list at given figure_index.

		Args:
			board:  Chessboard object
			figure:  Figure object
			figure_index:  index of the figure's previous position in the figures list in chessboard

		Returns:
			None    
		"""
    if figure:
        board.figures.add_figure(figure, figure_index)


def reduce_move_range_when_check(board: Chessboard, figure: Figure, moves):
    """
    Reduces moves from the given list that cannot be executed, e.g. they uncover the king and put it at risk.
    Foreach move in moves of figure makes the move and check if it puts king at risk. If it does, it gets erased from
    the moves list.

		Args:
			board:  Chessboard object
			figure:  Figure object
			moves:  list of figure's possible moves

		Returns:
			None    
		"""
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
    """
    Check if the figure selected is the king that is already put under check.

		Args:
			board:  Chessboard object
			selected_tile:  tuple indicating selected tile

		Returns:
			bool    
		"""
    figure = board.figures.get_figure_at(selected_tile)
    return figure and figure.figure_type == FigureType.KING and figure.color == board.current_player_color and board.check


def get_king_position(board: Chessboard, color: Color):
    """
    Return king's position of given color.

		Args:
			board:  Chessboard object
			color:  Color enum object

		Returns:
			king of given color    
		"""
    return board.figures.get_king_position(color)


def do_normal_move(board: Chessboard, move, figure_moved: Figure):
    """
    Executes normal chess move. It sets ability to castle to false if the figure moved was king or rook.

		Args:
			board:  Chessboard object
			move:  ChessMove object
			figure_moved:  Figure object

		Returns:
			None    
		"""
    if (figure_moved.figure_type == FigureType.KING or figure_moved.figure_type == FigureType.ROOK) and \
            figure_moved.is_able_to_castle:
        figure_moved.set_is_able_to_castle(False)
    potential_figure = board.figures.get_figure_at(move.position_to)
    if potential_figure:
        Figure.remove_figure(board.figures, potential_figure)
    # figure_moved.move(move.position_to)
    board.figures.move_figure_to(figure_moved, move.position_to)


def do_promotion(board: Chessboard, move, figure_moved: Figure):
    """
    Makes promotion move - when pawn reaches last line. It automatically assumes that the player chooses queen.

		Args:
			board:  Chessboard object
			move:  ChessMove object
			figure_moved:  Figure object

		Returns:
			None    
		"""
    do_normal_move(board, move, figure_moved)
    pos = figure_moved.position
    Figure.remove_figure(board.figures, figure_moved)
    board.figures.add_figure(Queen(board.current_player_color, pos))


def are_the_figures_left_capable_of_checkmate(board: Chessboard):
    """
    It check whether there is still checkmate possible depending on the figures left. It is impossible (returns True)
    when there are only:
    - two sole kings,
    - king versus king and bishop,
    - king versus king and knight,
    - king and bishop versus king and bishop and bishops are moving on the same tile color.

		Args:
			board:  Chessboard object

		Returns:
			bool    
		"""
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
    """
    Check if current moving player has any possible move left.

		Args:
			board:  Chessboard object

		Returns:
			bool    
		"""
    for figure in board.figures.figures_list:
        if figure.color != board.current_player_color:
            continue

        possible_moves = figure.check_moves(board.figures)
        reduce_move_range_when_check(board, figure, possible_moves)
        if possible_moves:
            return True
    return False


def get_player_from_color(color: Color):
    """
		Args:
			color:  Color enum object

		Returns:
			1 for Color.WHITE, 2 for Color.BLACK    
		"""
    return 1 if color == Color.WHITE else 2

