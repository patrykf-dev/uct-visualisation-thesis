from src.uct.game.base_game_move import BaseGameMove


class ChessMove(BaseGameMove):
    def __init__(self, pos, figure_type, move_type, help_dict=None):
        super().__init__()
        self.position = pos
        self.figure_type = figure_type
        self.move_type = move_type
        self.help_dict = help_dict

    def __str__(self):
        return f'{self.position}, {self.move_type}'
