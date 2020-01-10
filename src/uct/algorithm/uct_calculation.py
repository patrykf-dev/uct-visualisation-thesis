from math import sqrt, log

_HUGE_VALUE = 1000000


def find_best_child_with_UCT(node):
    """
    Calculates UCT value for children of a given node, with the formula:
    uct_value = (win_score / visits) + 1.41 * sqrt(log(parent_visit) / visits)
    and returns the most profitable one.
    :param node: MonteCarloNode object
    :return: MonteCarloNode node with the best UCT calculated value
    """
    parent_visit = node.details.visits_count
    return max(node.children, key=lambda n: _UCT_value(n, parent_visit))


def _UCT_value(node, parent_visit):
    visits = node.details.visits_count
    win_score = node.details.win_score

    if visits == 0:
        return _HUGE_VALUE
    else:
        uct_val = (win_score / visits) + 1.41 * sqrt(log(parent_visit) / visits)
        return uct_val
