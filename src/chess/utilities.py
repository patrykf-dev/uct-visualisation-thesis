class PastMove:
    def __init__(self, position_to, was_check, figure_moved, was_capture, position_from):
        self.position_to = position_to
        self.was_check = was_check
        self.figure_moved = figure_moved
        self.was_capture = was_capture
        self.position_from = position_from

    def __str__(self):
        return f'Move {self.figure_moved} to: {self.position_to}, check: {self.was_check}, capture: {self.was_capture}'
