from src.uct.game.base_game_move import BaseGameMove


class MancalaMove(BaseGameMove):
    def __init__(self, hole_index):
        super().__init__()
        self.hole_index = hole_index

    def move_equal(self, move) -> bool:
        return self.hole_index == move.hole_index and self.player == move.player
