from src.uct.mc_node_details import MonteCarloNodeDetails


class Node:
    _node_counter = 0

    def __init__(self):
        self.id = -1
        self.game_data = None
        self.node_details = None
        self.children = None
        self.parent = None
        raise Exception("Public constructor shouldn't ever be called, use create_root instead")

    def add_child(self, game_data):
        child = Node._create_instance(game_data)
        child.parent = self
        self.children.append(child)

    @staticmethod
    def create_root(game_data):
        return Node._create_instance(game_data)

    @staticmethod
    def _create_instance(game_data):
        node = Node()
        node.id = Node.generate_next_id()
        node.game_data = game_data
        node.node_details = MonteCarloNodeDetails()
        node.children = []
        node.parent = None
        return node

    @staticmethod
    def generate_next_id():
        Node._node_counter = Node._node_counter + 1
        return Node._node_counter
