from src.uct.game.base_game_move import BaseGameMove


class ChessMove(BaseGameMove):
    def __init__(self, position_to, position_from, move_type, help_dict=None):
        super().__init__()
        self.position = position_to
        self.position_from = position_from
        self.move_type = move_type
        self.help_dict = help_dict

    def __str__(self):
        return f'{self.position_to}, {self.move_type}'
