import src.serialization.codec_binary as BinaryCodec
from src.serialization.serializator_base import BaseSerializator


class BinarySerializator(BaseSerializator):
    def save_node_to_file(self, node, file_name):
        bin_arrays = []
        self.encode_node(bin_arrays, node)

        with open("../trees/" + file_name + ".tree", 'wb+') as f:
            for bin_array in bin_arrays:
                f.write(bin_array)

    def encode_node(self, bin_list, node):
        BinaryCodec.write_string(bin_list, node.details.state_name)
        BinaryCodec.write_integer(bin_list, len(node.children))
        for child in node.children:
            s = child.details
            if len(s.move) > 0:
                BinaryCodec.write_string(bin_list, s.move)
                BinaryCodec.write_integer(bin_list, s.visits_count)
                BinaryCodec.write_integer(bin_list, s.visits_count_pre_modified)
                BinaryCodec.write_float(bin_list, s.average_prize)
            self.encode_node(bin_list, child)

    def get_node_from_file(self, file_name):
        pass
