import unittest
from unittest.mock import patch
from itertools import chain

import pygame
from pygame.locals import *
import sys
import time

from src.chess.game import Game
from src.chess.figures import *
from src.chess.enums import GameStatus


class Move:
    def __init__(self, _from_position, _to_position=None):
        self.from_position = _from_position
        self.to_position = _to_position

    def get_pos(self):
        return self.from_position, self.to_position


class TestChess(unittest.TestCase):
    sleep_time_general = 0

    def setUp(self):
        self.game = Game()
        self.game.draw_board()
        pygame.display.flip()

    def tearDown(self):
        self.game.chessboard.figures = []

    # y,x -> x,y
    def get_mouse_position_from_tile(self, tile):
        margin = 1
        return tile[1] * self.game.TILE_HEIGHT + margin, (
                self.game.TILE_NUMBER - 1 - tile[0]) * self.game.TILE_WIDTH + margin

    def mock_process_input(self, event_queue, sleep_time=0.0):
        for event in event_queue:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                grid_pos = self.game.grid_click_to_tile(event.pos)
                self.game.chessboard.react_to_tile_click(grid_pos[::-1])
                self.game.draw_board()
                self.game.draw_moves()
                if sleep_time:
                    time.sleep(sleep_time)
                elif self.sleep_time_general:
                    time.sleep(self.sleep_time_general)
            pygame.display.update()

    def mock_move(self, pos):
        move_pos = self.get_mouse_position_from_tile(pos)
        mouse_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': move_pos, 'button': 1})
        return mouse_event

    def make_moves_from_queue(self, moves, sleep_time=0.0):
        event_queue = []
        for move in moves:
            event_queue.append(self.mock_move(move.from_position))
            if move.to_position:
                event_queue.append(self.mock_move(move.to_position))
        self.mock_process_input(event_queue, sleep_time)

    def test_en_passant_capture_possibility_white(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((6, 1), (4, 1)),
                 Move((4, 0))]
        self.make_moves_from_queue(moves)
        self.assertIn((5, 1), [move.position for move in self.game.chessboard.possible_moves])
        moves = [Move((1, 2), (3, 2)), Move((4, 7), (3, 7)),
                 Move((4, 0))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((5, 1), [move.position for move in self.game.chessboard.possible_moves])

    def test_en_passant_capture_possibility_black(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((4, 7), (3, 7)),
                 Move((1, 6), (3, 6)), Move((3, 7))]
        self.make_moves_from_queue(moves)
        self.assertIn((2, 6), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((6, 0), (5, 0)), Move((1, 1), (3, 1)),
                 Move((3, 7))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((2, 6), [move.position for move in self.game.chessboard.possible_moves])

    def test_en_passant_capture_white(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((6, 1), (4, 1)),
                 Move((4, 0), (5, 1))]
        self.make_moves_from_queue(moves)
        self.assertIsNone(Figure.get_figure(self.game.chessboard.figures, (4, 1)))

    def test_en_passant_capture_black(self):
        moves = [Move((1, 0), (3, 0)), Move((6, 7), (4, 7)),
                 Move((3, 0), (4, 0)), Move((4, 7), (3, 7)),
                 Move((1, 6), (3, 6)), Move((3, 7), (2, 6))]
        self.make_moves_from_queue(moves)
        self.assertIsNone(Figure.get_figure(self.game.chessboard.figures, (3, 6)))

    def test_castle_short_execution_both_colors(self):
        moves = [Move((1, 5), (3, 5)), Move((6, 5), (4, 5)),
                 Move((1, 6), (3, 6)), Move((6, 6), (4, 6)),
                 Move((0, 6), (2, 7)), Move((7, 6), (5, 7)),
                 Move((0, 5), (1, 6)), Move((7, 5), (6, 6)),
                 Move((0, 4), (0, 6)), Move((7, 4), (7, 6)),
                 ]
        self.make_moves_from_queue(moves)
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (0, 5)))
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (0, 6)))
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (7, 5)))
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (7, 6)))
        figure = Figure.get_figure(self.game.chessboard.figures, (0, 5))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.game.chessboard.figures, (0, 6))
        self.assertEqual(figure.figure_type, FigureType.KING)
        figure = Figure.get_figure(self.game.chessboard.figures, (7, 5))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.game.chessboard.figures, (7, 6))
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
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (0, 2)))
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (0, 3)))
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (7, 2)))
        self.assertIsNotNone(Figure.get_figure(self.game.chessboard.figures, (7, 3)))
        figure = Figure.get_figure(self.game.chessboard.figures, (0, 3))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.game.chessboard.figures, (0, 2))
        self.assertEqual(figure.figure_type, FigureType.KING)
        figure = Figure.get_figure(self.game.chessboard.figures, (7, 3))
        self.assertEqual(figure.figure_type, FigureType.ROOK)
        figure = Figure.get_figure(self.game.chessboard.figures, (7, 2))
        self.assertEqual(figure.figure_type, FigureType.KING)

    def test_king_cant_step_back_when_check(self):
        moves = [Move((1, 4), (3, 4)), Move((6, 3), (4, 3)),
                 Move((3, 4), (4, 3)), Move((7, 3), (4, 3)),
                 Move((0, 4), (1, 4)), Move((4, 3), (4, 4)),
                 Move((1, 4))
                 ]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 4), [move.position for move in self.game.chessboard.possible_moves])

    def test_checkmate_ends_game(self):
        self.game.chessboard.figures = [King(Color.BLACK, (7, 0)), Rook(Color.WHITE, (6, 7)), Rook(Color.WHITE, (0, 6)),
                             King(Color.WHITE, (0, 0))]
        moves = [Move((0, 6), (7, 6))]
        self.make_moves_from_queue(moves)
        self.assertFalse(self.game.chessboard.is_there_any_possible_move())

    def test_checkmate_can_be_prevented_by_capture(self):
        self.game.chessboard.figures = [King(Color.BLACK, (7, 0)), Rook(Color.WHITE, (6, 7)), Rook(Color.WHITE, (0, 6)),
                             Bishop(Color.BLACK, (1, 0)), King(Color.WHITE, (0, 0))]
        moves = [Move((0, 6), (7, 6))]
        self.make_moves_from_queue(moves)
        self.assertTrue(self.game.chessboard.is_there_any_possible_move())

    def test_are_moves_reduced_during_check(self):
        self.game.chessboard.figures = [King(Color.BLACK, (5, 5)), Rook(Color.BLACK, (0, 3)), Rook(Color.BLACK, (7, 4)),
                             Bishop(Color.BLACK, (0, 0)), Knight(Color.BLACK, (2, 1)), Queen(Color.BLACK, (0, 6)),
                             Pawn(Color.BLACK, (4, 2)), Bishop(Color.WHITE, (2, 4)), King(Color.WHITE, (6, 7))]
        moves = [Move((2, 4), (3, 3))]
        self.make_moves_from_queue(moves)

        select = [Move((4, 2))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((3, 2), [move.position for move in self.game.chessboard.possible_moves])

        select = [Move((0, 6))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((1, 5), [move.position for move in self.game.chessboard.possible_moves])

        select = [Move((2, 1))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((3, 1), [move.position for move in self.game.chessboard.possible_moves])

        select = [Move((0, 0))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((1, 1), [move.position for move in self.game.chessboard.possible_moves])

        select = [Move((7, 4))]
        self.make_moves_from_queue(select)
        self.assertIn((4, 4), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((7, 0), [move.position for move in self.game.chessboard.possible_moves])

        select = [Move((0, 3))]
        self.make_moves_from_queue(select)
        self.assertIn((3, 3), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((0, 1), [move.position for move in self.game.chessboard.possible_moves])

        select = [Move((5, 5))]
        self.make_moves_from_queue(select)
        self.assertIn((5, 4), [move.position for move in self.game.chessboard.possible_moves])
        self.assertIn((4, 5), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((4, 4), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((6, 6), [move.position for move in self.game.chessboard.possible_moves])

    def test_exposure_of_king_should_not_be_possible(self):
        self.game.chessboard.figures = [King(Color.WHITE, (4, 2)), Rook(Color.WHITE, (2, 2)), Rook(Color.BLACK, (0, 2)),
                             King(Color.BLACK, (7, 7))]
        moves = [Move((2, 2))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((2, 3), [move.position for move in self.game.chessboard.possible_moves])

    def test_promotion(self):
        self.game.chessboard.figures = [King(Color.WHITE, (1, 0)), Pawn(Color.WHITE, (6, 4)), King(Color.BLACK, (6, 7)),
                             Pawn(Color.BLACK, (1, 3))]
        moves = [Move((6, 4), (7, 4))]
        with patch('builtins.input', side_effect="q"):
            self.make_moves_from_queue(moves)
        figure = Figure.get_figure(self.game.chessboard.figures, (7, 4))
        self.assertIsNotNone(figure)
        self.assertEqual(figure.figure_type, FigureType.QUEEN)

        moves = [Move((1, 3), (0, 3))]
        with patch('builtins.input', side_effect="b"):
            self.make_moves_from_queue(moves)
        figure = Figure.get_figure(self.game.chessboard.figures, (0, 3))
        self.assertIsNotNone(figure)
        self.assertEqual(figure.figure_type, FigureType.BISHOP)

    def test_prevent_from_short_castling_when_fields_on_the_way_are_attacked(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), Rook(Color.BLACK, (3, 5)), King(Color.BLACK, (7, 4)),
                             Rook(Color.WHITE, (4, 5)), Rook(Color.WHITE, (0, 7)), Rook(Color.BLACK, (7, 7))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((4, 5), (5, 5)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 6), [move.position for move in self.game.chessboard.possible_moves])

    def test_prevent_from_long_castling_when_fields_on_the_way_are_attacked(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), Rook(Color.BLACK, (3, 3)), King(Color.BLACK, (7, 4)),
                             Rook(Color.WHITE, (4, 3)), Rook(Color.WHITE, (0, 0)), Rook(Color.BLACK, (7, 0))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((4, 3), (5, 3)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 2), [move.position for move in self.game.chessboard.possible_moves])

    def test_prevent_from_short_castling_when_the_last_field_on_the_way_is_attacked(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), Knight(Color.BLACK, (2, 7)), King(Color.BLACK, (7, 4)),
                             Knight(Color.WHITE, (3, 6)), Rook(Color.WHITE, (0, 7)), Rook(Color.BLACK, (7, 7))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((3, 6), (5, 7)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 6), [move.position for move in self.game.chessboard.possible_moves])

    def test_prevent_form_long_castling_when_the_last_field_on_the_way_is_attacked(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), Knight(Color.BLACK, (2, 1)), King(Color.BLACK, (7, 4)),
                             Knight(Color.WHITE, (4, 3)), Rook(Color.WHITE, (0, 0)), Rook(Color.BLACK, (7, 0))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((4, 3), (5, 1)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 2), [move.position for move in self.game.chessboard.possible_moves])

    def test_prevent_from_castling_when_check(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), Rook(Color.BLACK, (3, 4)), King(Color.BLACK, (7, 4)),
                             Rook(Color.WHITE, (3, 3)), Rook(Color.WHITE, (0, 7)), Rook(Color.BLACK, (7, 7)),
                             Rook(Color.WHITE, (0, 0)), Rook(Color.BLACK, (7, 0))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((0, 2), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((3, 3), (3, 4)), Move((7, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((7, 6), [move.position for move in self.game.chessboard.possible_moves])
        self.assertNotIn((7, 2), [move.position for move in self.game.chessboard.possible_moves])

    def test_prevent_short_castling_around_the_other_king(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), King(Color.BLACK, (1, 6)), Rook(Color.WHITE, (0, 7))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 6), [move.position for move in self.game.chessboard.possible_moves])

    def test_prevent_long_castling_around_the_other_king(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 4)), King(Color.BLACK, (1, 2)), Rook(Color.WHITE, (0, 0)),
                             Pawn(Color.WHITE, (1, 7))]
        moves = [Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position for move in self.game.chessboard.possible_moves])

        moves = [Move((1, 7), (2, 7)), Move((1, 2), (1, 1)), Move((0, 4))]
        self.make_moves_from_queue(moves)
        self.assertNotIn((0, 2), [move.position for move in self.game.chessboard.possible_moves])

    def test_checkmate_black(self):
        moves = [Move((1, 5), (3, 5)), Move((6, 4), (5, 4)), Move((1, 6), (3, 6)), Move((7, 3), (3, 7))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.CHECKMATE_BLACK)

    def test_checkmate_white(self):
        moves = [Move((1, 4), (2, 4)), Move((6, 5), (4, 5)), Move((1, 5), (3, 5)), Move((6, 6), (4, 6)),
                 Move((0, 3), (4, 7))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.CHECKMATE_WHITE)

    def test_stalemate_black(self):
        self.game.chessboard.figures = [King(Color.WHITE, (4, 4)), King(Color.BLACK, (7, 5)), Pawn(Color.WHITE, (6, 5))]
        moves = [Move((4, 4), (5, 5))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.STALEMATE)

    def test_stalemate_white(self):
        self.game.chessboard.figures = [King(Color.BLACK, (3, 3)), King(Color.WHITE, (1, 1)), Pawn(Color.BLACK, (1, 2))]
        moves = [Move((1, 1), (0, 2)), Move((3, 3), (2, 2))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.STALEMATE)

    def test_quickest_stalemate_known_in_chess(self):
        moves = [Move((1, 4), (2, 4)), Move((6, 0), (4, 0)), Move((0, 3), (4, 7)), Move((7, 0), (5, 0)),
                 Move((4, 7), (4, 0)), Move((6, 7), (4, 7)), Move((1, 7), (3, 7)), Move((5, 0), (5, 7)),
                 Move((4, 0), (6, 2)), Move((6, 5), (5, 5)), Move((6, 2), (6, 3)), Move((7, 4), (6, 5)),
                 Move((6, 3), (6, 1)), Move((7, 3), (2, 3)), Move((6, 1), (7, 1)), Move((2, 3), (6, 7)),
                 Move((7, 1), (7, 2)), Move((6, 5), (5, 6)), Move((7, 2), (5, 4))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.STALEMATE)

    def test_is_draw_when_two_kings(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)), Rook(Color.BLACK, (1, 1))]
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.DRAW)

    def test_is_draw_when_king_bishop(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)), Rook(Color.BLACK, (1, 1)),
                             Bishop(Color.BLACK, (1, 6))]
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.DRAW)

    def test_is_draw_when_king_knight(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)), Rook(Color.BLACK, (1, 1)),
                             Knight(Color.BLACK, (1, 6))]
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.DRAW)

    def test_is_not_draw_when_king_rook(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)), Rook(Color.BLACK, (1, 1)),
                             Rook(Color.BLACK, (2, 6))]
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.IN_PROGRESS)

    def test_is_draw_when_kings_with_same_bishops(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)), Rook(Color.BLACK, (1, 1)),
                             Bishop(Color.BLACK, (1, 6)), Bishop(Color.WHITE, (3, 6))]
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.DRAW)

    def test_is_not_draw_when_kings_with_other_bishops(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (7, 7)), Rook(Color.BLACK, (1, 1)),
                             Bishop(Color.BLACK, (1, 6)), Bishop(Color.WHITE, (2, 6))]
        moves = [Move((0, 0), (1, 1))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.IN_PROGRESS)

    def test_fifty_move_rule(self):
        self.game.chessboard.figures = [King(Color.WHITE, (0, 0)), King(Color.BLACK, (6, 0)), Pawn(Color.WHITE, (3, 3))]

        moves = [Move((0, 0), (0, 1)), Move((6, 0), (6, 1)), Move((3, 3), (4, 3)), Move((6, 1), (6, 2))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.IN_PROGRESS)

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
        self.assertEqual(self.game.chessboard.game_status, GameStatus.IN_PROGRESS)

        moves = [Move((0, 1), (0, 2)), Move((6, 2), (6, 3))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.IN_PROGRESS)

        moves = [Move((0, 2), (0, 3))]
        self.make_moves_from_queue(moves)
        self.assertEqual(self.game.chessboard.game_status, GameStatus.FIFTY_MOVE_RULE)


if __name__ == '__main__':
    unittest.main()
