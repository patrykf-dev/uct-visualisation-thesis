import src.uct.algorithm.enums as Enums


class TicTacToeBoard:
    def __init__(self, size):
        self.size = size
        self.board_values = [[0 for i in range(size)] for j in range(size)]
        self._empty_spots = size * size

    def deep_copy(self):
        new_board = TicTacToeBoard(self.size)
        new_values = [[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                new_values[i][j] = self.board_values[i][j]
        new_board.size = self.size
        new_board.board_values = new_values
        new_board._empty_spots = self._empty_spots
        return new_board

    def move_valid(self, x, y):
        return x < self.size and y < self.size and self.board_values[y][x] == 0

    def perform_move(self, player, x, y):
        self.board_values[y][x] = player
        self._empty_spots = self._empty_spots - 1
        return self._get_status_after_move(x, y)

    def get_empty_positions(self):
        rc = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board_values[i][j] == 0:
                    rc.append((j, i))
        return rc

    def get_string_formatted(self):
        rc = ""
        for i in range(self.size):
            for j in range(self.size):
                rc += "[{}]".format(self.board_values[i][j])
            if i < self.size - 1:
                rc += "\n"
        return rc

    def _get_status_after_move(self, x, y):
        if self._empty_spots == 0:
            return Enums.GamePhase.DRAW
        result = self._check_row_and_column_after_move(x, y)
        if result != Enums.GamePhase.IN_PROGRESS:
            return result
        result = self._check_diags_after_move(x, y)
        if result != Enums.GamePhase.IN_PROGRESS:
            return result
        return Enums.GamePhase.IN_PROGRESS

    def _check_diags_after_move(self, x, y):
        if x != y and y != self.size - x - 1:
            return Enums.GamePhase.IN_PROGRESS

        winner = self.board_values[y][x]
        for i in range(self.size):
            if self.board_values[i][i] != winner:
                winner = 0
                break
        if winner != 0:
            return Enums.get_player_win(winner)

        winner = self.board_values[y][x]
        for i in range(self.size):
            if self.board_values[i][self.size - i - 1] != winner:
                winner = 0
                break
        if winner != 0:
            return Enums.get_player_win(winner)

        return Enums.GamePhase.IN_PROGRESS

    def _check_row_and_column_after_move(self, x, y):
        winner = self.board_values[y][x]
        col_equal = True
        row_equal = True
        for i in range(self.size):
            if self.board_values[x][i] != winner:
                row_equal = False
            if self.board_values[i][y] != winner:
                col_equal = False
            if not col_equal and not row_equal:
                break

        if row_equal or col_equal:
            return Enums.get_player_win(winner)

        return Enums.GamePhase.IN_PROGRESS
