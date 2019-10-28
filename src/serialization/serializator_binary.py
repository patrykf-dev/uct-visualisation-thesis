import src.serialization.codec_binary as BinaryCodec
from src.serialization.serializator_base import BaseSerializator
from src.uct.algorithm.mc_node_details import MonteCarloNodeDetails
from src.uct.algorithm.mc_node import MonteCarloNode


class BinarySerializator(BaseSerializator):
    def __init__(self):
        super().__init__()
        self.extension = "tree"

    def save_node_to_file(self, node, file_name):
        bin_arrays = []
        self._encode_node(bin_arrays, node)

        path = self.get_file_path(file_name)
        with open(path, 'wb+') as file:
            for bin_array in bin_arrays:
                file.write(bin_array)

    def get_node_from_file(self, file_name):
        path = self.get_file_path(file_name)
        with open(path, "rb") as file:
            node, _ = self._decode_node(file)
        return node

    def _encode_node(self, bin_list, node):
        BinaryCodec.write_string(bin_list, node.details.state_name)
        BinaryCodec.write_integer(bin_list, len(node.children))
        for child in node.children:
            s = child.details
            if len(s.move) > 0:
                BinaryCodec.write_string(bin_list, s.move)
                BinaryCodec.write_integer(bin_list, s.visits_count)
                BinaryCodec.write_integer(bin_list, s.visits_count_pre_modified)
                BinaryCodec.write_float(bin_list, s.average_prize)
            self._encode_node(bin_list, child)

    def _decode_node(self, file):
        rc = MonteCarloNode()
        state_name = BinaryCodec.read_string(file)
        rc.details.state_name = state_name

        children_count = BinaryCodec.read_integer(file)
        for i in range(children_count):
            details = MonteCarloNodeDetails()
            details.move_name = BinaryCodec.read_string(file)
            details.visits_count = BinaryCodec.read_integer(file)
            details.visits_count_pre_modified = BinaryCodec.read_integer(file)
            details.average_prize = BinaryCodec.read_float(file)
            child, child_state_name = self._decode_node(file)
            details.state_name = child_state_name
            child.details = details
            rc.children.append(child)

        return rc, state_name
