import src.utils.random_utils as RandomUtils
from src.uct.algorithm.mc_node import MonteCarloNode


def get_random_child(node: MonteCarloNode):
    if not node.has_children():
        raise Exception("Node does not have any child nodes")
    else:
        child_index = RandomUtils.get_random_int(0, len(node.children))
        return node.children[child_index]


def get_child_with_max_score(node: MonteCarloNode):
    if not node.has_children():
        raise Exception("Node does not have any child nodes")
    else:
        return max(node.children, key=lambda n: n.details.win_score)
