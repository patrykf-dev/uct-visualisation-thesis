import unittest
from unittest.mock import patch
from itertools import chain

import sys
import time

from chess.figures import *
from chess.enums import GameStatus
import chess.chess_utils as ChessUtils
from chess.chessboard import Chessboard


class Move:
    def __init__(self, _from_position, _to_position=None):
        self.from_position = _from_position
        self.to_position = _to_position

    def get_pos(self):
        return self.from_position, self.to_position


class TestChess(unittest.TestCase):
    sleep_time_general = 0

    def setUp(self):
        self.chessboard = Chessboard()
        self.possible_moves = []

    def make_moves_from_queue(self, moves):
        for move in moves:
            figure = self.chessboard.figures.get_figure_at(move.from_position)
            self.possible_moves = figure.check_moves(self.chessboard.figures)
            ChessUtils.reduce_move_range_when_check(self.chessboard, figure, self.possible_moves)
            if move.to_position:
                move_from_pool = [_move for _move in self.possible_moves if _move.position_to == move.to_position][0]
                self.chessboard.perform_legal_move(move_from_pool)
            else:
                break

    def test_en_passant_capture_possibility_white(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((6, 1), (4, 1)), Move((4, 0))]
        self.make_moves_from_queue(moves)
        self.assertIn((5, 1), [move.position_to for move in self.possible_moves])

        moves = [Move((1, 2), (3, 2)), Move((4, 7), (3, 7)),
                 Move((4, 0))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((5, 1), [move.position_to for move in self.possible_moves])

    def test_en_passant_capture_possibility_black(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((4, 7), (3, 7)),
                 Move((1, 6), (3, 6)), Move((3, 7))]
        self.make_moves_from_queue(moves)
        self.assertIn((2, 6), [move.position_to for move in self.possible_moves])

        moves = [Move((6, 0), (5, 0)), Move((1, 1), (3, 1)),
                 Move((3, 7))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((2, 6), [move.position_to for move in self.possible_moves])

    def test_en_passant_capture_white(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((6, 1), (4, 1)),
                 Move((4, 0), (5, 1))]
        self.make_moves_from_queue(moves)
        self.assertIsNone(Figure.get_figure(self.chessboard.figures, (4, 1)))

    def test_en_passant_capture_black(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((4, 7), (3, 7)),
                 Move((1, 6), (3, 6)), Move((3, 7), (2, 6))]
        self.make_moves_from_queue(moves)
        self.assertIsNone(Figure.get_figure(self.chessboard.figures, (3, 6)))

    def test_castle_short_execution_both_colors(self):
        moves = [Move((1, 5), (3, 5)), Move((6, 5), (4, 5)),
                 Move((1, 6), (3, 6)), Move((6, 6), (4, 6)),
                 Move((0, 6), (2, 7)), Move((7, 6), (5, 7)),
                 Move((0, 5), (1, 6)), Move((7, 5), (6, 6)),
                 Move((0, 4), (0, 6)), Move((7, 4), (7, 6)),
                 ]
        self.make_moves_from_queue(moves)
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (0, 5)))
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (0, 6)))
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (7, 5)))
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (7, 6)))
        figure = Figure.get_figure(self.chessboard.figures, (0, 5))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.chessboard.figures, (0, 6))
        self.assertEqual(figure.figure_type, FigureType.KING)
        figure = Figure.get_figure(self.chessboard.figures, (7, 5))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.chessboard.figures, (7, 6))
        self.assertEqual(figure.figure_type, FigureType.KING)

    def test_castle_long_execution_both_colors(self):
        moves = [Move((1, 1), (3, 1)), Move((6, 1), (4, 1)),
                 Move((1, 2), (3, 2)), Move((6, 2), (4, 2)),
                 Move((1, 3), (3, 3)), Move((6, 3), (4, 3)),
                 Move((0, 1), (2, 0)), Move((7, 1), (5, 0)),
                 Move((0, 2), (1, 1)), Move((7, 2), (6, 1)),
                 Move((0, 3), (1, 3)), Move((7, 3), (6, 3)),
                 Move((0, 4), (0, 2)), Move((7, 4), (7, 2)),
                 ]
        self.make_moves_from_queue(moves)
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (0, 2)))
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (0, 3)))
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (7, 2)))
        self.assertIsNotNone(Figure.get_figure(self.chessboard.figures, (7, 3)))
        figure = Figure.get_figure(self.chessboard.figures, (0, 3))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.chessboard.figures, (0, 2))
        self.assertEqual(figure.figure_type, FigureType.KING)
        figure = Figure.get_figure(self.chessboard.figures, (7, 3))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.chessboard.figures, (7, 2))
        self.assertEqual(figure.figure_type, FigureType.KING)

    def test_king_cant_step_back_when_check(self):
        moves = [Move((1, 4), (3, 4)), Move((6, 3), (4, 3)),
                 Move((3, 4), (4, 3)), Move((7, 3), (4, 3)),
                 Move((0, 4), (1, 4)), Move((4, 3), (4, 4)),
                 Move((1, 4))
                 ]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 4), [move.position_to for move in self.chessboard.possible_moves])

    def test_checkmate_ends_game(self):
        figures = [King(Color.BLACK, (7, 0)), Rook(Color.WHITE, (6, 7)),
                                                Rook(Color.WHITE, (0, 6)),
                                                King(Color.WHITE, (0, 0))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 6), (7, 6))]
        self.make_moves_from_queue(moves)
        self.assertFalse(ChessUtils.is_there_any_possible_move(self.chessboard))

    def test_checkmate_can_be_prevented_by_capture(self):
        figures = [King(Color.BLACK, (7, 0)), Rook(Color.WHITE, (6, 7)),
                                                Rook(Color.WHITE, (0, 6)),
                                                Bishop(Color.BLACK, (1, 0)), King(Color.WHITE, (0, 0))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 6), (7, 6))]
        self.make_moves_from_queue(moves)
        self.assertTrue(ChessUtils.is_there_any_possible_move(self.chessboard))

    def test_are_moves_reduced_during_check(self):
        figures = [King(Color.BLACK, (5, 5)), Rook(Color.BLACK, (0, 3)),
                                                Rook(Color.BLACK, (7, 4)),
                                                Bishop(Color.BLACK, (0, 0)), Knight(Color.BLACK, (2, 1)),
                                                Queen(Color.BLACK, (0, 6)),
                                                Pawn(Color.BLACK, (4, 2)), Bishop(Color.WHITE, (2, 4)),
                                                King(Color.WHITE, (6, 7))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((2, 4), (3, 3))]
        self.make_moves_from_queue(moves)

        select = [Move((4, 2))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position_to for move in self.possible_moves])
        self.assertNotIn((3, 2), [move.position_to for move in self.possible_moves])

        select = [Move((0, 6))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position_to for move in self.possible_moves])
        self.assertNotIn((1, 5), [move.position_to for move in self.possible_moves])

        select = [Move((2, 1))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position_to for move in self.possible_moves])
        self.assertNotIn((3, 1), [move.position_to for move in self.possible_moves])

        select = [Move((0, 0))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position_to for move in self.possible_moves])
        self.assertNotIn((1, 1), [move.position_to for move in self.possible_moves])

        select = [Move((7, 4))]
        self.make_moves_from_queue(select)
        self.assertIn((4, 4), [move.position_to for move in self.possible_moves])
        self.assertNotIn((7, 0), [move.position_to for move in self.possible_moves])

        select = [Move((0, 3))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position_to for move in self.possible_moves])
        self.assertNotIn((0, 1), [move.position_to for move in self.possible_moves])

        select = [Move((5, 5))]
        self.make_moves_from_queue(select)
        self.assertIn((5, 4), [move.position_to for move in self.possible_moves])
        self.assertIn((4, 5), [move.position_to for move in self.possible_moves])
        self.assertNotIn((4, 4), [move.position_to for move in self.possible_moves])
        self.assertNotIn((6, 6), [move.position_to for move in self.possible_moves])

    def test_exposure_of_king_should_not_be_possible(self):
        figures = [King(Color.WHITE, (4, 2)), Rook(Color.WHITE, (2, 2)),
                                                Rook(Color.BLACK, (0, 2)),
                                                King(Color.BLACK, (7, 7))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((2, 2))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((2, 3), [move.position_to for move in self.chessboard.possible_moves])

    # def test_promotion(self):
    #     figures = [King(Color.WHITE, (1, 0)), Pawn(Color.WHITE, (6, 4)), King(Color.BLACK, (6, 7)),
    #                Pawn(Color.BLACK, (1, 3))]
    #     self.chessboard.figures = ChessFiguresCollection(figures)
    #     moves = [Move((6, 4), (7, 4))]
    #     with patch('builtins.input', side_effect="q"):
    #         self.make_moves_from_queue(moves)
    #     figure = Figure.get_figure(self.chessboard.figures, (7, 4))
    #     self.assertIsNotNone(figure)
    #     self.assertEqual(figure.figure_type, FigureType.QUEEN)
    #
    #     moves = [Move((1, 3), (0, 3))]
    #     with patch('builtins.input', side_effect="b"):
    #         self.make_moves_from_queue(moves)
    #     figure = Figure.get_figure(self.chessboard.figures, (0, 3))
    #     self.assertIsNotNone(figure)
    #     self.assertEqual(figure.figure_type, FigureType.BISHOP)

    def test_prevent_from_short_castling_when_fields_on_the_way_are_attacked(self):
        figures = [King(Color.WHITE, (0, 4)), Rook(Color.BLACK, (3, 5)),
                                                King(Color.BLACK, (7, 4)),
                                                Rook(Color.WHITE, (4, 5)), Rook(Color.WHITE, (0, 7)),
                                                Rook(Color.BLACK, (7, 7))]
        figures = self.chessboard.figures = ChessFiguresCollection(figures)
        figures.get_king(Color.WHITE).update_check_mask(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position_to for move in self.chessboard.possible_moves])

        moves = [Move((4, 5), (5, 5)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 6), [move.position_to for move in self.chessboard.possible_moves])

    def test_prevent_from_long_castling_when_fields_on_the_way_are_attacked(self):
        figures = [King(Color.WHITE, (0, 4)), Rook(Color.BLACK, (3, 3)),
                                                King(Color.BLACK, (7, 4)),
                                                Rook(Color.WHITE, (4, 3)), Rook(Color.WHITE, (0, 0)),
                                                Rook(Color.BLACK, (7, 0))]
        figures = self.chessboard.figures = ChessFiguresCollection(figures)
        figures.get_king(Color.WHITE).update_check_mask(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position_to for move in self.chessboard.possible_moves])

        moves = [Move((4, 3), (5, 3)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 2), [move.position_to for move in self.chessboard.possible_moves])

    def test_prevent_from_short_castling_when_the_last_field_on_the_way_is_attacked(self):
        figures = [King(Color.WHITE, (0, 4)), Knight(Color.BLACK, (2, 7)),
                                                King(Color.BLACK, (7, 4)),
                                                Knight(Color.WHITE, (3, 6)), Rook(Color.WHITE, (0, 7)),
                                                Rook(Color.BLACK, (7, 7))]
        figures = self.chessboard.figures = ChessFiguresCollection(figures)
        figures.get_king(Color.WHITE).update_check_mask(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position_to for move in self.chessboard.possible_moves])

        moves = [Move((3, 6), (5, 7)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 6), [move.position_to for move in self.chessboard.possible_moves])

    def test_prevent_form_long_castling_when_the_last_field_on_the_way_is_attacked(self):
        figures = [King(Color.WHITE, (0, 4)), Knight(Color.BLACK, (2, 1)),
                                                King(Color.BLACK, (7, 4)),
                                                Knight(Color.WHITE, (4, 3)), Rook(Color.WHITE, (0, 0)),
                                                Rook(Color.BLACK, (7, 0))]
        figures = self.chessboard.figures = ChessFiguresCollection(figures)
        figures.get_king(Color.WHITE).update_check_mask(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position_to for move in self.chessboard.possible_moves])

        moves = [Move((4, 3), (5, 1)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 2), [move.position_to for move in self.chessboard.possible_moves])

    def test_prevent_from_castling_when_check(self):
        figures = [King(Color.WHITE, (0, 4)), Rook(Color.BLACK, (3, 4)),
                                                King(Color.BLACK, (7, 4)),
                                                Rook(Color.WHITE, (3, 3)), Rook(Color.WHITE, (0, 7)),
                                                Rook(Color.BLACK, (7, 7)),
                                                Rook(Color.WHITE, (0, 0)), Rook(Color.BLACK, (7, 0))]
        figures = self.chessboard.figures = ChessFiguresCollection(figures)
        figures.get_king(Color.WHITE).update_check_mask(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position_to for move in self.chessboard.possible_moves])
        self.assertNotIn((0, 2), [move.position_to for move in self.chessboard.possible_moves])

        moves = [Move((3, 3), (3, 4)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 6), [move.position_to for move in self.chessboard.possible_moves])
        self.assertNotIn((7, 2), [move.position_to for move in self.chessboard.possible_moves])

    def test_prevent_short_castling_around_the_other_king(self):
        figures = [King(Color.WHITE, (0, 4)), King(Color.BLACK, (1, 6)),
                                                Rook(Color.WHITE, (0, 7))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position_to for move in self.chessboard.possible_moves])

    def test_prevent_long_castling_around_the_other_king(self):
        figures = [King(Color.WHITE, (0, 4)), King(Color.BLACK, (1, 2)),
                                                Rook(Color.WHITE, (0, 0)),
                                                Pawn(Color.WHITE, (1, 7))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position_to for move in self.chessboard.possible_moves])

        moves = [Move((1, 7), (2, 7)), Move((1, 2), (1, 1)), Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position_to for move in self.chessboard.possible_moves])

    def test_checkmate_black(self):
        moves = [Move((1, 5), (3, 5)), Move((6, 4), (5, 4)), Move((1, 6), (3, 6)), Move((7, 3), (3, 7))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.CHECKMATE_BLACK)

    def test_checkmate_white(self):
        moves = [Move((1, 4), (2, 4)), Move((6, 5), (4, 5)), Move((1, 5), (3, 5)), Move((6, 6), (4, 6)),
                 Move((0, 3), (4, 7))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.CHECKMATE_WHITE)

    def test_stalemate_black(self):
        figures = [King(Color.WHITE, (4, 4)), King(Color.BLACK, (7, 5)),
                                                Pawn(Color.WHITE, (6, 5))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((4, 4), (5, 5))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.STALEMATE)

    def test_stalemate_white(self):
        figures = [King(Color.BLACK, (3, 3)), King(Color.WHITE, (1, 1)),
                                                Pawn(Color.BLACK, (1, 2))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((1, 1), (0, 2)), Move((3, 3), (2, 2))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.STALEMATE)

    def test_quickest_stalemate_known_in_chess(self):
        moves = [Move((1, 4), (2, 4)), Move((6, 0), (4, 0)), Move((0, 3), (4, 7)), Move((7, 0), (5, 0)),
                 Move((4, 7), (4, 0)), Move((6, 7), (4, 7)), Move((1, 7), (3, 7)), Move((5, 0), (5, 7)),
                 Move((4, 0), (6, 2)), Move((6, 5), (5, 5)), Move((6, 2), (6, 3)), Move((7, 4), (6, 5)),
                 Move((6, 3), (6, 1)), Move((7, 3), (2, 3)), Move((6, 1), (7, 1)), Move((2, 3), (6, 7)),
                 Move((7, 1), (7, 2)), Move((6, 5), (5, 6)), Move((7, 2), (5, 4))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.STALEMATE)

    def test_is_draw_when_two_kings(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)),
                                                Rook(Color.BLACK, (1, 1))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.DRAW)

    def test_is_draw_when_king_bishop(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)),
                                                Rook(Color.BLACK, (1, 1)),
                                                Bishop(Color.BLACK, (1, 6))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.DRAW)

    def test_is_draw_when_king_knight(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)),
                                                Rook(Color.BLACK, (1, 1)),
                                                Knight(Color.BLACK, (1, 6))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.DRAW)

    def test_is_not_draw_when_king_rook(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)),
                                                Rook(Color.BLACK, (1, 1)),
                                                Rook(Color.BLACK, (2, 6))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.IN_PROGRESS)

    def test_is_draw_when_kings_with_same_bishops(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)),
                                                Rook(Color.BLACK, (1, 1)),
                                                Bishop(Color.BLACK, (1, 6)), Bishop(Color.WHITE, (3, 6))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.DRAW)

    def test_is_not_draw_when_kings_with_other_bishops(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)),
                                                Rook(Color.BLACK, (1, 1)),
                                                Bishop(Color.BLACK, (1, 6)), Bishop(Color.WHITE, (2, 6))]
        self.chessboard.figures = ChessFiguresCollection(figures)
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.IN_PROGRESS)

    def test_fifty_move_rule(self):
        figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (6, 0)),
                                                Pawn(Color.WHITE, (3, 3))]
        self.chessboard.figures = ChessFiguresCollection(figures)

        moves = [Move((0, 0), (0, 1)), Move((6, 0), (6, 1)), Move((3, 3), (4, 3)), Move((6, 1), (6, 2))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.IN_PROGRESS)

        moves_white = [
            Move((0, 1), (0, 2)), Move((0, 2), (0, 3)), Move((0, 3), (0, 4)),
            Move((0, 4), (0, 5)), Move((0, 5), (0, 6)), Move((0, 6), (0, 7)), Move((0, 7), (1, 7)),
            Move((1, 7), (1, 6)), Move((1, 6), (1, 5)), Move((1, 5), (1, 4)), Move((1, 4), (1, 3)),
            Move((1, 3), (1, 2)), Move((1, 2), (1, 1)), Move((1, 1), (1, 0)), Move((1, 0), (0, 0)),
            Move((0, 0), (0, 1)), Move((0, 1), (0, 2)), Move((0, 2), (0, 3)), Move((0, 3), (0, 4)),
            Move((0, 4), (0, 5)), Move((0, 5), (0, 6)), Move((0, 6), (0, 7)), Move((0, 7), (1, 7)),
            Move((1, 7), (1, 6)), Move((1, 6), (1, 5)), Move((1, 5), (1, 4)), Move((1, 4), (1, 3)),
            Move((1, 3), (1, 2)), Move((1, 2), (1, 1)), Move((1, 1), (1, 0)), Move((1, 0), (0, 0)),
            Move((0, 0), (0, 1)), Move((0, 1), (0, 2)), Move((0, 2), (0, 3)), Move((0, 3), (0, 4)),
            Move((0, 4), (0, 5)), Move((0, 5), (0, 6)), Move((0, 6), (0, 7)), Move((0, 7), (1, 7)),
            Move((1, 7), (1, 6)), Move((1, 6), (1, 5)), Move((1, 5), (1, 4)), Move((1, 4), (1, 3)),
            Move((1, 3), (1, 2)), Move((1, 2), (1, 1)), Move((1, 1), (1, 0)), Move((1, 0), (0, 0)),
            Move((0, 0), (0, 1))]
        moves_black = [
            Move((6, 2), (6, 3)), Move((6, 3), (6, 4)),
            Move((6, 4), (6, 5)), Move((6, 5), (6, 6)), Move((6, 6), (6, 7)), Move((6, 7), (7, 7)),
            Move((7, 7), (7, 6)), Move((7, 6), (7, 5)), Move((7, 5), (7, 4)), Move((7, 4), (7, 3)),
            Move((7, 3), (7, 2)), Move((7, 2), (7, 1)), Move((7, 1), (7, 0)), Move((7, 0), (6, 0)),
            Move((6, 0), (6, 1)), Move((6, 1), (6, 2)), Move((6, 2), (6, 3)), Move((6, 3), (6, 4)),
            Move((6, 4), (6, 5)), Move((6, 5), (6, 6)), Move((6, 6), (6, 7)), Move((6, 7), (7, 7)),
            Move((7, 7), (7, 6)), Move((7, 6), (7, 5)), Move((7, 5), (7, 4)), Move((7, 4), (7, 3)),
            Move((7, 3), (7, 2)), Move((7, 2), (7, 1)), Move((7, 1), (7, 0)), Move((7, 0), (6, 0)),
            Move((6, 0), (6, 1)), Move((6, 1), (6, 2)), Move((6, 2), (6, 3)), Move((6, 3), (6, 4)),
            Move((6, 4), (6, 5)), Move((6, 5), (6, 6)), Move((6, 6), (6, 7)), Move((6, 7), (7, 7)),
            Move((7, 7), (7, 6)), Move((7, 6), (7, 5)), Move((7, 5), (7, 4)), Move((7, 4), (7, 3)),
            Move((7, 3), (7, 2)), Move((7, 2), (7, 1)), Move((7, 1), (7, 0)), Move((7, 0), (6, 0)),
            Move((6, 0), (6, 1)), Move((6, 1), (6, 2))]
        moves = list(chain.from_iterable(zip(moves_white, moves_black)))
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.IN_PROGRESS)

        moves = [Move((0, 1), (0, 2)), Move((6, 2), (6, 3))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.IN_PROGRESS)

        moves = [Move((0, 2), (0, 3))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.chessboard.game_status, GameStatus.FIFTY_MOVE_RULE)

    def test_en_passant_capture_should_not_uncover_the_king(self):
        figures = [King(Color.WHITE, (3, 2)), King(Color.BLACK, (7, 7)),
                   Pawn(Color.WHITE, (4, 4)), Pawn(Color.BLACK, (6, 3)),
                   Queen(Color.BLACK, (4, 7))]
        self.chessboard.figures = ChessFiguresCollection(figures)

        moves = [Move((3, 2), (4, 2)), Move((6, 3), (4, 3)), Move((4, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((5, 3), [move.position_to for move in self.chessboard.possible_moves])


if __name__ == '__main__':
    unittest.main()
