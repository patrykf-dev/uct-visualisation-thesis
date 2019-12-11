import re

from PyQt5.QtCore import pyqtSignal, QObject

from src.serialization.serializator_binary import BinarySerializator
from src.serialization.serializator_csv import CsvSerializator
from src.uct.algorithm.mc_tree import MonteCarloTree
from src.utils.custom_event import CustomEvent


class TreesRetrieverWorker(QObject):
    tree_retrieved_signal = pyqtSignal(float)

    def __init__(self, paths):
        super().__init__()
        self.paths = paths
        self.trees_info = []

    def do_work(self):
        trees_info = []
        binary_serializator = BinarySerializator()
        csv_serializator = CsvSerializator()
        for i, tree_path in enumerate(self.paths):
            serializator = binary_serializator if tree_path.endswith("tree") else csv_serializator
            root = serializator.get_node_from_path(tree_path)
            filename = self._retrieve_filename_from_path(tree_path)
            trees_info.append(MonteCarloNodeSequenceInfo(MonteCarloTree(root=root), filename))
            self.tree_retrieved_signal.emit((i + 1) / len(self.paths))
        self.trees_info = trees_info

    def _retrieve_filename_from_path(self, path):
        split_strings = re.split('/', path)
        final_split_strings = []
        for split_string in split_strings:
            final_split_strings.extend(re.split(r'\\', split_string))
        return final_split_strings[-1]


class MonteCarloNodeSequenceInfo:
    def __init__(self, tree: MonteCarloTree, filename):
        self.tree = tree
        self.filename = filename

    def __str__(self):
        return f"{self.filename}"
