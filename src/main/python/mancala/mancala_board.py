
from mancala.algorithm_relay.mancala_move import MancalaMove
from uct.algorithm.enums import GamePhase


class MancalaBoard:
    """
    Class is responsible for mancala logic.

    Indices of the holes are organized as follows:
        12  11  10   9   8   7
    13--------------------------6
        0   1   2   3   4   5
    """
    def __init__(self):
        self.board_values = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.current_player = 1
        self.phase = GamePhase.IN_PROGRESS

    def perform_move(self, move: MancalaMove, print_moves=True):
        """
        For each move in internal moves sequence perform internal move, which makes for a single whole move.

		Args:
			move:  MancalaMove object

		Returns:
			None        
		"""
        for hole_index in move.moves_sequence:
            self.perform_move_internal(hole_index, move.player, print_moves)

    def perform_move_internal(self, hole_index, player, print_moves=True):
        """
        Performs mancala move. It is called internal, because a whole single move can be a sequence of such moves.
        This method calculates values of holes after the move and updates them.

		Args:
			hole_index:  index of the chosen hole, from which the move executes
			player:  player issuing the move

		Returns:
			bool informing if the whole move was made and the turn changes        
		"""
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
        opposite_hole_index = 12 - index
        if (index == 6 and self.current_player == 1) or (index == 13 and self.current_player == 2):
            switch_turns = False
        elif self.board_values[index] == 1 and self.is_the_hole_of_current_player(index) and self.board_values[
            opposite_hole_index] > 0:
            if self.current_player == 1:
                self.board_values[6] += self.board_values[opposite_hole_index] + 1
            else:
                self.board_values[13] += self.board_values[opposite_hole_index] + 1
            self.board_values[opposite_hole_index] = 0
            self.board_values[index] = 0

        self.check_if_game_ended()

        if switch_turns:
            self.current_player = 1 if self.current_player == 2 else 2

        return not switch_turns

    def determine_winner(self):
        """
        Updates game phase by calculating which player collected more points.

		Returns:
			None        
		"""
        player1_points = self.board_values[6]
        player2_points = self.board_values[13]
        if player1_points > player2_points:
            self.phase = GamePhase.PLAYER1_WON
        elif player1_points < player2_points:
            self.phase = GamePhase.PLAYER2_WON
        else:
            self.phase = GamePhase.DRAW

    def check_if_game_ended(self):
        """
        Checks if the game ended i.e. there are no stones left on one side. If the game has ended, the winner is
        determined.

		Returns:
			None        
		"""
        game_ended = False
        if not any(self._get_player_holes(1)):
            self.board_values[13] += sum(self._get_player_holes(2))
            game_ended = True
        elif not any(self._get_player_holes(2)):
            self.board_values[6] += sum(self._get_player_holes(1))
            game_ended = True

        if game_ended:
            self.board_values = [0 if i != 6 and i != 13 else self.board_values[i] for i in range(14)]
            self.determine_winner()

    def get_win_score(self, player):
        """
		Args:
			player:  1 - first player / 2 - second player

		Returns:
			difference between points collected in bases of two players. The score is negative when given 'player'                 has less points than the rival.        
		"""
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
        """
		Returns:
			Deep copy of MancalaBoard object        
		"""
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
        """
		Returns:
			All possible moves of currently moving player        
		"""
        all_moves = []
        for i in self.possible_player_moves():
            self.get_player_moves(i, MancalaMove([], self.current_player), all_moves)
        return all_moves

    def possible_player_moves(self):
        """
        Generates possible moves of current moving player.

		Returns:
			yields hole index if a move from that hole is possible        
		"""
        for i, a in enumerate(self._get_player_holes(self.current_player)):
            if a > 0:
                yield i

    def get_player_moves(self, hole_index, prev_move: MancalaMove, moves):
        """
        Recursive function that checks for player moves that can be executed from given hole.
        For example, if the player 1 has such configuration of stones:
        [1, 0, 0, 0, 2, 1] in holes of corresponding indexes [0, 1, 2, 3, 4, 5]
        the result would be:
        [[0], [4, 0], [4, 5], [5, 0], [5, 4, 0], [5, 4, 5, 0]] - these are the all possible moves
        (sequences ob sub-moves). Result is stored in moves variable, that is passed as an argument.

		Args:
			hole_index:  index of
			prev_move:  MancalaMove of previous move
			moves:  list of MancalaMove objects that is recursively filled

		Returns:
			None        
		"""
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
            move.description = str(f"Player {move.player} went: {move.moves_sequence}")
            moves.append((move, f"Current player: {copied_board.current_player}"))
            return

    def is_the_hole_of_current_player(self, index):
        """
        Checks if the given hole index belongs to currently moving player.
        Player 1: 0-5
        Player 2: 7-12.
        Indexes 6 and 13 are stores and the result is False.

		Args:
			index:  index of hole that is being checked

		Returns:
			bool value        
		"""
        if index in range(0, 6) and self.current_player == 1:
            return True
        if index in range(7, 13) and self.current_player == 2:
            return True
        return False

    def is_hole_empty(self, index):
        """
		Args:
			index:  index of hole

		Returns:
			bool informing if the hole has no stones inside        
		"""
        return self.board_values[index] == 0

    def is_hole_valid(self, index):
        """
		Args:
			index:  index of hole

		Returns:
			bool informing if the hole belongs to the currently moving player and is empty (so that the move can                 be executed)        
		"""
        return self.is_the_hole_of_current_player(index) and not self.is_hole_empty(index)

