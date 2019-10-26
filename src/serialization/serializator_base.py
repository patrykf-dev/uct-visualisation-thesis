from abc import ABC


class BaseSerializator(ABC):
    def save_node_to_file(self, node, file_name):
        pass

    def get_node_from_file(self, file_name):
        pass
