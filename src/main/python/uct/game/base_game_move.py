import abc


class BaseGameMove(abc.ABC):
    def __init__(self):
        self.player = 1
        self.description = ""

    @abc.abstractmethod
    def move_equal(self, move) -> bool:
        pass
