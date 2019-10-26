from src.uct.node import Node
from src.serialization.serializator_binary import BinarySerializator


def serialization_test():
    aa = create_node("aa", "")
    bb = create_node("bb", "x")
    cc = create_node("cc", "y")
    dd = create_node("dd", "z")
    ee = create_node("ee", "w")

    aa.children = [bb, cc]
    cc.children = [dd, ee]

    serializator = BinarySerializator()
    serializator.save_node_to_file(aa, "serialization_test")


def create_node(name, move_name):
    n = Node()
    n.details.state_name = name
    if len(move_name) > 0:
        n.details.move = move_name
        n.details.visits_count = 3
        n.details.visits_count_pre_modified = 4
        n.details.win_score = 4.5
    return n


def deserialization_test():
    serializator = BinarySerializator()
    node = serializator.get_node_from_file("serialization_test")
    d = node.details
    print("Root: [{}] : ([{}], {}, {}, {})".format(d.state_name, d.move, d.visits_count, d.visits_count_pre_modified,
                                                  d.average_prize))
    d = node.children[0].details
    print("First child: [{}] : ([{}], {}, {}, {})".format(d.state_name, d.move, d.visits_count, d.visits_count_pre_modified,
                                                  d.average_prize))


serialization_test()
