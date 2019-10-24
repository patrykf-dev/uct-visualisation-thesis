class MoveObject:
    def __init__(self, pos, move_type, help_dict=None):
        self.position = pos
        self.move_type = move_type
        self.help_dict = help_dict

    def __str__(self):
        return f'{self.position}, {self.move_type}'


class PastMove:
    def __init__(self, position, was_check, figure_moved, was_capture, old_position):
        self.position = position
        self.was_check = was_check
        self.figure_moved = figure_moved
        self.was_capture = was_capture
        self.old_position = old_position

    def __str__(self):
        return f'Move {self.figure_moved} to: {self.position}, check: {self.was_check}, capture: {self.was_capture}'
