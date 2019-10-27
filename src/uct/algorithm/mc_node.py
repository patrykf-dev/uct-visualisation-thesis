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

    def add_child(self, move):
        child = MonteCarloNode._create_instance(move)
        child.parent = self
        self.children.append(child)

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
        node.details = MonteCarloNodeDetails()
        node.children = []
        node.parent = None
        return node

    @staticmethod
    def generate_next_id():
        MonteCarloNode._node_counter = MonteCarloNode._node_counter + 1
        return MonteCarloNode._node_counter
