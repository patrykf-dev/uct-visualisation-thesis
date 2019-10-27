import abc


class BaseGameMove(abc.ABC):
    def __init__(self):
        self.player = 1
