class MancalaBoardNew:
    """
    self.board is organized as follows:
        12  11  10   9   8   7
    13--------------------------6
        0   1   2   3   4   5
    """

    def __init__(self):
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        # self.board = [0, 0, 0, 0, 0, 1, 24, 0, 1, 1, 1, 0, 1, 18]
        self.current_player = 1

    def perform_move(self, hole_index):
        stones = self.board[hole_index]
        self.board[hole_index] = 0
        index = hole_index + 1
        while stones > 0:
            if index == 6:
                if self.current_player == 1:
                    self.board[index] += 1
                    stones -= 1
            elif index == 13:
                if self.current_player == 2:
                    self.board[index] += 1
                    stones -= 1
            else:
                self.board[index] += 1
                stones -= 1

            index = (index + 1) % 14

        index -= 1
        switch_turns = True
        if (index == 6 and self.current_player == 1) or (index == 13 and self.current_player == 2):
            switch_turns = False
        elif self.board[index] == 1:
            opposite_hole_index = 12 - index
            if self.current_player == 1:
                self.board[6] += self.board[opposite_hole_index]
            else:
                self.board[13] += self.board[opposite_hole_index]
            self.board[opposite_hole_index] = 0

        self.check_if_game_ended()

        if switch_turns:
            self.current_player = 1 if self.current_player == 2 else 2

        print(f"Player {self.current_player} turn")

    def check_if_game_ended(self):
        game_ended = False
        if not any(self.board[0:6]):
            print("Player 1 ended the game!")
            self.board[13] += sum(self.board[7:13])
            game_ended = True
        elif not any(self.board[7:13]):
            print("Player 2 ended the game!")
            self.board[6] += sum(self.board[0:6])
            game_ended = True

        if game_ended:
            self.board = [0 if i != 6 and i != 13 else self.board[i] for i in range(14)]
