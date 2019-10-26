from src.uct.node import Node
from src.uct.mc_node_details import MonteCarloNodeDetails
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


serialization_test()
