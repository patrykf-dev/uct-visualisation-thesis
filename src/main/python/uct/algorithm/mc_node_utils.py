
import utils.random_utils as RandomUtils
from uct.algorithm.mc_node import MonteCarloNode


def get_random_child(node: MonteCarloNode):
    """
    Returns random child of the node. Exception is raised if node has no children.

		Args:
			node:  MonteCarloNode object

		Returns:
			MonteCarloNode object, random child of the given node    
		"""
    if not node.has_children():
        raise Exception("Node does not have any child nodes")
    else:
        child_index = RandomUtils.get_random_int(0, len(node.children))
        return node.children[child_index]


def get_child_with_max_score(node: MonteCarloNode):
    """
    Returns child with biggest average prize. Exception is raised if node has no children.

		Args:
			node:  MonteCarloNode object

		Returns:
			MonteCarloNode object, child with biggest average prize    
		"""
    if not node.has_children():
        raise Exception("Node does not have any child nodes")
    else:
        return max(node.children, key=lambda n: n.details.average_prize)

