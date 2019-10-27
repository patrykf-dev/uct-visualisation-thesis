from src.uct.game.base_game_move import BaseGameMove


class TicTacToeMove(BaseGameMove):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y