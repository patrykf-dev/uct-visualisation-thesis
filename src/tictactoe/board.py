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
        # TODO
        pass
