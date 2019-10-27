from enum import Enum


class GamePhase(Enum):
    IN_PROGRESS = 1,
    PLAYER1_WON = 2,
    PLAYER2_WON = 3,
    DRAW = 4


def get_player_win(player):
    if player == 1:
        return GamePhase.PLAYER1_WON
    elif player == 2:
        return GamePhase.PLAYER2_WON
    else:
        raise Exception("Unknown player index")


def get_opponent_win(player):
    return get_player_win(get_opponent(player))


def get_opponent(player):
    if player == 1:
        return 2
    elif player == 2:
        return 1
    else:
        raise Exception("Unknown player index")
