from __future__ import annotations

from src.mancala.algorithm_relay.mancala_move import MancalaMove
from src.uct.algorithm.enums import GamePhase


class MancalaBoard:
    """
    self.board is organized as follows:
        12  11  10   9   8   7
    13--------------------------6
        0   1   2   3   4   5
    """

    def __init__(self):
        self.board_values = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        # self.board = [0, 0, 0, 0, 0, 1, 24, 0, 1, 1, 1, 0, 1, 18]
        self.current_player = 1
        self.phase = GamePhase.IN_PROGRESS

    def perform_move(self, move: MancalaMove, print_moves=True):
        for hole_index in move.moves_sequence:
            self.perform_move_internal(hole_index, move.player, print_moves)

    def perform_move_internal(self, hole_index, player, print_moves=True):
        if (0 <= hole_index <= 5 and self.current_player == 2) or (7 <= hole_index <= 12 and self.current_player == 1):
            raise PermissionError("ILLEGAL MOVE!!!")
        if player != self.current_player:
            raise PermissionError("WRONG PLAYER!!!")
        if self.board_values[hole_index] == 0:
            raise PermissionError("EMPTY HOLE HERE!!!")

        stones = self.board_values[hole_index]
        self.board_values[hole_index] = 0
        index = hole_index + 1
        while stones > 0:
            if index == 6:
                if self.current_player == 1:
                    self.board_values[index] += 1
                    stones -= 1
            elif index == 13:
                if self.current_player == 2:
                    self.board_values[index] += 1
                    stones -= 1
            else:
                self.board_values[index] += 1
                stones -= 1

            index = (index + 1) % 14

        if index == 0:
            index = 13
        else:
            index -= 1

        switch_turns = True
        if (index == 6 and self.current_player == 1) or (index == 13 and self.current_player == 2):
            switch_turns = False
        elif self.board_values[index] == 1:
            opposite_hole_index = 12 - index
            if self.current_player == 1:
                self.board_values[6] += self.board_values[opposite_hole_index]
            else:
                self.board_values[13] += self.board_values[opposite_hole_index]
            self.board_values[opposite_hole_index] = 0

        self.check_if_game_ended()

        if switch_turns:
            self.current_player = 1 if self.current_player == 2 else 2

        # if print_moves:
        #     possible_moves = self.find_all_moves()
        #     print(f"Possible moves for {self.current_player}: {possible_moves}")

        return not switch_turns

    def check_if_game_ended(self):
        game_ended = False
        if not any(self._get_player_holes(1)):
            self.phase = GamePhase.PLAYER1_WON
            self.board_values[13] += sum(self._get_player_holes(2))
            game_ended = True
        elif not any(self._get_player_holes(2)):
            self.phase = GamePhase.PLAYER2_WON
            self.board_values[6] += sum(self._get_player_holes(1))
            game_ended = True

        if game_ended:
            self.board_values = [0 if i != 6 and i != 13 else self.board_values[i] for i in range(14)]

    def get_win_score(self, player):
        if player == 1:
            return self.board_values[6] - self.board_values[13]
        else:
            return self.board_values[13] - self.board_values[6]

    def _get_player_holes(self, player):
        if player == 1:
            return self.board_values[0:6]
        else:
            return self.board_values[7:13]

    def deep_copy(self):
        rc = MancalaBoard()
        rc.current_player = self.current_player
        for i in range(14):
            rc.board_values[i] = self.board_values[i]
        rc.phase = self.phase
        return rc

    def _get_hole_index(self, base_index):
        if self.current_player == 2:
            return base_index + 7
        else:
            return base_index

    def find_all_moves(self):
        all_moves = []
        for i in self.possible_player_moves():
            self.get_player_moves(i, MancalaMove([], self.current_player), all_moves)
        return all_moves

    def possible_player_moves(self):
        for i, a in enumerate(self._get_player_holes(self.current_player)):
            if a > 0:
                yield i

    def get_player_moves(self, hole_index, prev_move: MancalaMove, moves):
        hole_index = self._get_hole_index(hole_index)
        copied_board = self.deep_copy()
        player_pre_move = copied_board.current_player
        next_turn = copied_board.perform_move_internal(hole_index, copied_board.current_player, print_moves=False)
        if next_turn and list(copied_board.possible_player_moves()) and player_pre_move == copied_board.current_player:
            for i in copied_board.possible_player_moves():
                move = MancalaMove(prev_move.moves_sequence + [hole_index], self.current_player)
                copied_board.get_player_moves(i, move, moves)
        else:
            move = MancalaMove(prev_move.moves_sequence + [hole_index], self.current_player)
            move.description = str(move)
            moves.append(move)
            return
