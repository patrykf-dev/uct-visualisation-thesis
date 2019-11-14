import csv

from src.serialization.serializator_base import BaseSerializator
from src.uct.algorithm.mc_node import MonteCarloNode


class CsvSerializator(BaseSerializator):
    def __init__(self):
        super().__init__()
        self.extension = "csv"

    def save_node_to_path(self, node, path):
        with open(path, "w+", newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            self._encode_node(writer, node)

    def get_node_from_path(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            node = self._decode_node(reader)
        return node

    def _encode_node(self, writer, node):
        s = node.details
        row = [s.move_name, s.visits_count, s.visits_count_pre_modified, s.average_prize, s.state_name,
               len(node.children)]
        writer.writerow(row)
        for child in node.children:
            self._encode_node(writer, child)

    def _decode_node(self, reader, depth=0):
        row = next(reader)
        node = MonteCarloNode()
        d = node.details
        d.move_name = row[0]
        d.visits_count = int(row[1])
        d.visits_count_pre_modified = int(row[2])
        d.average_prize = float(row[3])
        d.state_name = row[4]
        children = int(row[5])
        for i in range(children):
            child = self._decode_node(reader, depth+1)
            node.add_child_by_node(child)
        return node
