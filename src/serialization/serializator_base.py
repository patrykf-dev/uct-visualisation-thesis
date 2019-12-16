import abc

from src.uct.algorithm.mc_node import MonteCarloNode


class BaseSerializator(abc.ABC):
    string_dictionary = {}

    @abc.abstractmethod
    def __init__(self):
        self.extension = ""

    def get_file_path(self, file_name: str):
        return "../trees/{}.{}".format(file_name, self.extension)

    @abc.abstractmethod
    def save_node_to_path(self, node: MonteCarloNode, path: str):
        pass

    @abc.abstractmethod
    def get_node_from_path(self, path: str) -> MonteCarloNode:
        pass

    def get_string(self, string):
        string_hash = hash(string)
        if not self.string_dictionary.get(string_hash, None):
            val = self.string_dictionary[string_hash] = string
            return val
        else:
            return self.string_dictionary[string_hash]
