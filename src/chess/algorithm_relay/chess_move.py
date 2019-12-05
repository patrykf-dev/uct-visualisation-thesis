from src.chess.enums import MoveType
from src.uct.game.base_game_move import BaseGameMove


class ChessMove(BaseGameMove):
    def __init__(self, position_to, position_from, move_type=MoveType.NORMAL, help_dict=None):
        super().__init__()
        self.position_to = position_to
        self.position_from = position_from
        self.move_type = move_type
        self.help_dict = help_dict

    def move_equal(self, move) -> bool:
        return self.position_to[0] == move.position_to[0] and self.position_to[1] == move.position_to[1] and \
               self.position_from[0] == move.position_from[0] and self.position_from[1] == move.position_from[1] and \
               self.move_type == move.move_type

    def __str__(self):
        return f'{self.position_to}, {self.move_type}'
