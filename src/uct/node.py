from src.uct.mc_node_details import MonteCarloNodeDetails


class Node:
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
        child = Node._create_instance(move)
        child.parent = self
        self.children.append(child)

    def has_children(self):
        return len(self.children) > 0

    @staticmethod
    def create_root():
        return Node._create_instance(None)

    @staticmethod
    def _create_instance(move):
        node = Node()
        node.id = Node.generate_next_id()
        node.move = move
        node.details = MonteCarloNodeDetails()
        node.children = []
        node.parent = None
        return node

    @staticmethod
    def generate_next_id():
        Node._node_counter = Node._node_counter + 1
        return Node._node_counter
