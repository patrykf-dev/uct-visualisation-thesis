import src.uct.enums as Enums


class TicTacToeBoard:
    def __init__(self, size):
        self.size = size
        self.board_values = [[0 for i in range(size)] for j in range(size)]

    def deep_copy(self):
        new_board = TicTacToeBoard(self.size)
        new_values = [[0 for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                new_values[i][j] = self.board_values[i][j]
        new_board.size = self.size
        return new_board

    def move_valid(self, x, y):
        return x < self.size and y < self.size and self.board_values[y][x] == 0

    def perform_move(self, player, x, y):
        self.board_values[y][x] = player

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

    def check_status(self):
        result = self.check_rows_and_columns()
        if result != Enums.GamePhase.IN_PROGRESS:
            return result
        result = self.check_diags()
        if result != Enums.GamePhase.IN_PROGRESS:
            return result
        if len(self.get_empty_positions()) == 0:
            return Enums.GamePhase.DRAW
        else:
            return Enums.GamePhase.IN_PROGRESS

    def check_diags(self):
        winner = self.board_values[0][0]
        for i in range(self.size):
            if self.board_values[i][i] != winner:
                winner = 0
                break
        if winner != 0:
            return Enums.get_player_win(winner)

        winner = self.board_values[0][self.size - 1]
        for i in range(self.size):
            if self.board_values[i][self.size - i - 1] != winner:
                winner = 0
                break
        if winner != 0:
            return Enums.get_player_win(winner)

        return Enums.GamePhase.IN_PROGRESS

    def check_rows_and_columns(self):
        for i in range(self.size):
            col_equal = True
            col_winner = self.board_values[0][i]
            row_equal = True
            row_winner = self.board_values[i][0]
            if row_winner == 0 and col_winner == 0:
                continue

            for j in range(self.size):
                if self.board_values[i][j] != row_winner:
                    row_equal = False
                if self.board_values[j][i] != col_winner:
                    col_winner = False
                if not col_equal and not row_equal:
                    break

            if col_winner:
                return Enums.get_player_win(col_winner)
            if row_equal:
                return Enums.get_player_win(row_winner)

        return Enums.GamePhase.IN_PROGRESS
