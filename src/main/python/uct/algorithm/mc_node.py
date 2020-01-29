
import visualisation_algorithm.mc_node_vis_details as Vis
from uct.algorithm.mc_node_details import MonteCarloNodeDetails


class MonteCarloNode:
    """
    Class is responsible for storing information about a single node in Monte Carlo tree.
    """
    _node_counter = 0

    def __init__(self):
        """
        Public constructor shouldn't ever be called, use create_root instead
        """
        self.id = -1
        self.move = None
        self.details = MonteCarloNodeDetails()
        self.children = []
        self.parent = None
        self.vis_details = Vis.MonteCarloNodeVisualisationDetails(self)
        self.left_most_sibling = None
        self.number = 1

    def add_child_by_move(self, move, state_desc=""):
        """
        Adds child node to the node. New node represents given move.

		Args:
			move:  BaseGameMove object

		Returns:
			None        
		"""
        child = MonteCarloNode._create_instance(move)
        if state_desc != "":
            child.details.state_name = state_desc
        child.parent = self
        child.vis_details.y = self.vis_details.y + 1
        self.children.append(child)
        child.number = len(self.children)

    def add_child_by_node(self, child):
        """
        Adds child node to the node.

		Args:
			child:  MonteCarloNode object

		Returns:
			None        
		"""
        child.parent = self
        child.vis_details.y = self.vis_details.y + 1
        self.children.append(child)
        child.number = len(self.children)

    def has_children(self):
        """
		Returns:
			bool informing if node has any children nodes        
		"""
        return len(self.children) > 0

    @staticmethod
    def create_root():
        """
		Returns:
			MonteCarloNode object representing root node (has no move assigned)        
		"""
        return MonteCarloNode._create_instance(None)

    @staticmethod
    def _create_instance(move):
        node = MonteCarloNode()
        node.id = MonteCarloNode.generate_next_id()
        node.move = move
        node.vis_details = Vis.MonteCarloNodeVisualisationDetails(node)
        node.details = MonteCarloNodeDetails()
        node.children = []
        node.parent = None
        if move:
            node.details.move_name = move.description
        return node

    @staticmethod
    def generate_next_id():
        """
		Returns:
			int, unique id for a node (starts from 1)        
		"""
        MonteCarloNode._node_counter = MonteCarloNode._node_counter + 1
        return MonteCarloNode._node_counter

    def left(self):
        """
        Needed for Improved Walker's Algorithm.

		Returns:
			MonteCarloNode object, leftmost child or thread of the node        
		"""
        if self.has_children():
            rc = self.children[0]
        else:
            rc = self.vis_details.thread
        return rc

    def right(self):
        """
        Needed for Improved Walker's Algorithm.

		Returns:
			MonteCarloNode object, rightmost child or thread of the node        
		"""
        if self.has_children():
            rc = self.children[-1]
        else:
            rc = self.vis_details.thread
        return rc

    def left_sibling(self):
        """
        Needed for Improved Walker's Algorithm.

		Returns:
			MonteCarloNode object, left sibling of the node        
		"""
        left_node = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return left_node
                left_node = node
        return left_node

    def leftmost_sibling(self):
        """
        Needed for Improved Walker's Algorithm.

		Returns:
			MonteCarloNode object, leftmost sibling of the node        
		"""
        if not self.left_most_sibling and self.parent and self != self.parent.children[0]:
            self.left_most_sibling = self.parent.children[0]
        return self.left_most_sibling

