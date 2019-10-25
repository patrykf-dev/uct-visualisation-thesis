from src.uct.node import Node
import src.uct.random_utils as RandomUtils


def get_random_child(node):
    if not node.has_children():
        raise Exception("Node does not have any child nodes")
    else:
        child_index = RandomUtils.get_random_int(0, len(node.children))
        return node.children[child_index]


def get_child_with_max_score(node):
    if not node.has_children():
        raise Exception("Node does not have any child nodes")
    else:
        return max(node.children, key=lambda n: n.details.visits_count)  # TODO: visits_count???
