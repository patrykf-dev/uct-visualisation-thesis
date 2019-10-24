from src.uct.node import Node
from math import sqrt, log

_HUGE_VALUE = 1000000


def find_best_child_with_UCT(node):
    parent_visit = node.node_details.visits_count
    return max(node.children, lambda n: _UCT_value(n, parent_visit))[0]


def _UCT_value(node, parent_visit):
    visits = node.details.visits_count
    win_score = node.details.win_score

    if visits == 0:
        return _HUGE_VALUE
    else:
        uct_val = (win_score / visits) + 1.41 * sqrt(log(parent_visit / visits))
        return uct_val
