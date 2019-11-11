import os
import sys

import pygame
from pygame.locals import *

from src.chess.algorithm_relay.chess_state import ChessState
from src.chess.chess_game_manager import ChessGameManager
from src.chess.chessboard import Figure
from src.uct.algorithm.mc_tree_search import MonteCarloTreeSearch
from src.visualisation_algorithm.walkers_algorithm import ImprovedWalkersAlgorithm
from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas
from src.visualisation_drawing.mc_tree_window import MonteCarloTreeWindow

WIDTH = 600
HEIGHT = 600
TILE_NUMBER = 8
TILE_WIDTH = int(WIDTH / TILE_NUMBER)
TILE_HEIGHT = int(HEIGHT / TILE_NUMBER)
ICONS_FOLDER = 'icons'
TILES_FONT = None


class Game:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.TILE_NUMBER = TILE_NUMBER
        self.TILE_WIDTH = int(WIDTH / TILE_NUMBER)
        self.TILE_HEIGHT = int(HEIGHT / TILE_NUMBER)
        self.ICONS_FOLDER = 'icons'
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.get_surface()
        self.game_manager = ChessGameManager()

    def get_image(self, image_file):
        tile_image = pygame.image.load(os.path.join(self.ICONS_FOLDER, image_file))
        return pygame.transform.scale(tile_image, (self.TILE_WIDTH, self.TILE_HEIGHT))

    def draw_figure(self, figure, tile_pos):
        if figure:
            tile_image = self.get_image(figure.image_file)
            self.screen.blit(tile_image, tile_pos)

    def draw_board(self):
        for i, row in enumerate(self.game_manager.board_gui.grid):
            for j, tile in enumerate(row):
                pygame.draw.rect(self.window, tile.color, (tile.start_position[0], tile.start_position[1],
                                                           tile.tile_width, tile.tile_height))
                tile_figure = Figure.get_figure(self.game_manager.board.figures, (i, j))
                if tile_figure:
                    self.draw_figure(tile_figure, tile.start_position)
                tile_text_surface = TILES_FONT.render(f"{i}, {j}", False, (255, 255, 255))
                self.screen.blit(tile_text_surface, tile.start_position)

    def grid_click_to_tile(self, pos):
        """
        :param pos: GUI order (x, y)
        :return: GUI order
        """
        if pos[1] == 0:
            pos = pos[0], 1
        return (pos[0] // self.TILE_WIDTH, (self.HEIGHT - pos[1]) // self.TILE_HEIGHT)[::-1]

    def tile_to_grid(self, positions):
        """
        :param positions: matrix order (y, x)
        :return: returns GUI order
        """
        return [(x[1] * self.TILE_WIDTH, x[0] * self.TILE_HEIGHT) for x in positions]

    # moves_projected - GUI order
    def draw_circles(self, moves_projected):
        for move in moves_projected:
            pygame.draw.circle(self.screen, (111, 50, 200),
                               (move[0] + self.TILE_WIDTH // 2, self.HEIGHT - move[1] - self.TILE_HEIGHT // 2), 12)

    def draw_moves(self):
        if self.game_manager.selected_tile:
            if self.game_manager.board.possible_moves:
                moves_projected = self.tile_to_grid(x.position_to for x in self.game_manager.board.possible_moves)
                self.draw_circles(moves_projected)

    def react_to_player_click(self):
        pos = pygame.mouse.get_pos()
        grid_pos = self.grid_click_to_tile(pos)
        player_moved = self.game_manager.react_to_tile_click(grid_pos)
        self.redraw_board()
        if player_moved:
            self.game_manager.deselect_last_moved()

            game_state = ChessState(self.game_manager.board)
            mcts = MonteCarloTreeSearch(game_state, max_iterations=20)
            move, _ = mcts.calculate_next_move()

            print(f"Algorithm decided to go {move.position_from} -> {move.position_to} for player {move.player}")
            self.game_manager.board.perform_legal_move(move)
            self.game_manager.reset_selected_tile()
            self.redraw_board()

            alg = ImprovedWalkersAlgorithm()
            alg.buchheim_algorithm(mcts.tree.root)

            canvas = MonteCarloTreeCanvas(mcts.tree.root)
            window = MonteCarloTreeWindow(canvas)
            window.show()

    def process_input(self, events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.react_to_player_click()
            pygame.display.update()

    def redraw_board(self):
        self.draw_board()
        self.draw_moves()
        pygame.display.update()


if __name__ == "__main__":
    pygame.font.init()
    TILES_FONT = pygame.font.SysFont("Helvetica", 30)
    game = Game()
    game.draw_board()
    pygame.display.flip()
    while True:
        game.process_input(pygame.event.get())
