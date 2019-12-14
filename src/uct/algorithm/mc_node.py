import src.visualisation_algorithm_new.mc_node_vis_details as Vis
from src.uct.algorithm.mc_node_details import MonteCarloNodeDetails


class MonteCarloNode:
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
        self._left_most_sibling = None
        # this is the number of the node in its group of siblings 1..n
        self.number = 1

    def add_child_by_move(self, move):
        child = MonteCarloNode._create_instance(move)
        child.parent = self
        child.vis_details.y = self.vis_details.y + 1
        self.children.append(child)
        child.number = len(self.children)

    def add_child_by_node(self, child):
        child.parent = self
        child.vis_details.y = self.vis_details.y + 1
        self.children.append(child)
        child.number = len(self.children)

    def has_children(self):
        return len(self.children) > 0

    @staticmethod
    def create_root():
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
        MonteCarloNode._node_counter = MonteCarloNode._node_counter + 1
        return MonteCarloNode._node_counter

    def left(self):
        """
        :rtype: MonteCarloNode
        """
        if self.has_children():
            rc = self.children[0]
        else:
            rc = self.vis_details.thread
        return rc

    def right(self):
        """
        :rtype: MonteCarloNode
        """
        if self.has_children():
            rc = self.children[-1]
        else:
            rc = self.vis_details.thread
        return rc

    def lbrother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return n
                else:
                    n = node
        return n

    def get_lmost_sibling(self):
        if not self._left_most_sibling and self.parent and self != self.parent.children[0]:
            self._left_most_sibling = self.parent.children[0]
        return self._left_most_sibling

    lmost_sibling = property(get_lmost_sibling)
