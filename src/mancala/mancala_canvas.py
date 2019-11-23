import copy

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter

from src.main_application.enums import GameMode
from src.main_application.game_canvas import GameCanvas
from src.mancala.algorithm_relay.mancala_move import MancalaMove
from src.mancala.algorithm_relay.mancala_state import MancalaState
from src.mancala.mancala_board import MancalaBoard
from src.mancala.mancala_board_drawer import MancalaBoardDrawer
from src.uct.algorithm.mc_game_manager import MonteCarloGameManager


class MancalaCanvas(GameCanvas):
    def __init__(self, game_mode: GameMode):
        super().__init__(game_mode)
        self.board_drawer = MancalaBoardDrawer(self.WIDTH, self.HEIGHT)
        self.moves_sequence = []
        self.board = MancalaBoard()
        game_state = MancalaState(self.board)
        self.monte_carlo_manager = MonteCarloGameManager(game_state)

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.board_drawer.draw_board(painter, self.board)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        pos = event.pos()
        player_moved, moved_index = self.board_drawer.detect_click(pos.x(), pos.y())
        extra_turn = False
        if player_moved:
            extra_turn = self.board.perform_move_internal(moved_index, self.board.current_player)
            self.moves_sequence.append(moved_index)
        self.repaint()

        if not extra_turn and player_moved:
            player = 1 if self.board.current_player == 2 else 2
            player_move = MancalaMove(copy.deepcopy(self.moves_sequence), player)
            print(f"PLAYER WENT FOR {player_move}")
            self.moves_sequence.clear()

            if self.game_mode == GameMode.PLAYER_VS_PC:
                self.monte_carlo_manager.notify_move_performed(player_move)
                super().perform_player_move()

    def perform_algorithm_move(self):
        super().perform_algorithm_move()
        move = self.monte_carlo_manager.calculate_next_move(max_iterations=500, max_moves_per_simulation=100)
        print(f"Algorithm decided to go for {move.moves_sequence} for player {move.player}")

        self.board.perform_move(move)
        self.on_update_tree(self.monte_carlo_manager.tree.root)
        if self.game_mode == GameMode.PC_VS_PC:
            self.monte_carlo_manager.perform_previous_move()

        self.board_drawer.stones_centers = []  # TODO get rid of this
        self.repaint()
