import os
import pygame
import sys
from pygame.locals import *

from src.chess.chessboard import Chessboard, Figure

WIDTH = 600
HEIGHT = 600
TILE_NUMBER = 8
TILE_WIDTH = int(WIDTH / TILE_NUMBER)
TILE_HEIGHT = int(HEIGHT / TILE_NUMBER)
ICONS_FOLDER = 'icons'


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
        self.chessboard = Chessboard()

    def get_image(self, image_file):
        tile_image = pygame.image.load(os.path.join(self.ICONS_FOLDER, image_file))
        return pygame.transform.scale(tile_image, (self.TILE_WIDTH, self.TILE_HEIGHT))

    def draw_figure(self, figure, tile_pos):
        if figure:
            tile_image = self.get_image(figure.image_file)
            self.screen.blit(tile_image, tile_pos)

    def draw_board(self):
        for i, row in enumerate(self.chessboard.board.grid):
            for j, tile in enumerate(row):
                pygame.draw.rect(self.window, tile.color, (tile.start_position[0], tile.start_position[1],
                                                           tile.tile_width, tile.tile_height))
                tile_figure = Figure.get_figure(self.chessboard.figures, (i, j))
                if tile_figure:
                    self.draw_figure(tile_figure, tile.start_position)

    # pos - GUI order (x, y)
    # returns GUI order
    def grid_click_to_tile(self, pos):
        if pos[1] == 0:
            pos = pos[0], 1
        return pos[0] // self.TILE_WIDTH, (self.HEIGHT - pos[1]) // self.TILE_HEIGHT

    # positions - matrix order (y, x)
    # returns GUI order
    def tile_to_grid(self, positions):
        return [(x[1] * self.TILE_WIDTH, x[0] * self.TILE_HEIGHT) for x in positions]

    # moves_projected - GUI order
    def draw_circles(self, moves_projected):
        for move in moves_projected:
            pygame.draw.circle(self.screen, (111, 50, 200),
                               (move[0] + self.TILE_WIDTH // 2, self.HEIGHT - move[1] - self.TILE_HEIGHT // 2), 12)

    def draw_moves(self):
        if self.chessboard.selected_tile:
            if self.chessboard.possible_moves:
                moves_projected = self.tile_to_grid(x.position for x in self.chessboard.possible_moves)
                self.draw_circles(moves_projected)

    def process_input(self, events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                grid_pos = self.grid_click_to_tile(pos)
                self.chessboard.decide_move_action(grid_pos[::-1])
                self.draw_board()
                # self.draw_figures()
                self.draw_moves()
            else:
                pass
                # print(event)
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.draw_board()
    pygame.display.flip()
    while True:
        game.process_input(pygame.event.get())
