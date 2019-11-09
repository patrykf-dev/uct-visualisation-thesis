import matplotlib.pyplot as plt

import src.visualisation_algorithm.walkers_algorithm as Walkers
from src.uct.algorithm.mc_node import MonteCarloNode


def create_node(name, move_name):
    n = MonteCarloNode()
    n.details.state_name = name
    if len(move_name) > 0:
        n.details.move = move_name
        n.details.visits_count = 3
        n.details.visits_count_pre_modified = 4
        n.details.average_prize = 4.5
    return n


def create_tree():
    aa = create_node("aa", "")
    bb = create_node("bb", "x")
    cc = create_node("cc", "y")
    dd = create_node("dd", "z")
    ee = create_node("ee", "w")
    ff = create_node("ee", "w")
    gg = create_node("ee", "w")
    hh = create_node("ee", "w")

    aa.add_child_by_node(bb)
    aa.add_child_by_node(gg)
    aa.add_child_by_node(cc)
    cc.add_child_by_node(dd)
    dd.add_child_by_node(hh)
    cc.add_child_by_node(ee)
    cc.add_child_by_node(ff)
    # prev = aa
    # for i in range(20):
    #     new_node = create_node("xx", "z")
    #     prev.add_child_by_node(new_node)
    #     prev = new_node
    return aa


def display_tree(node: MonteCarloNode):
    x_parent = node.vis_details.x
    y_parent = node.vis_details.y
    x.append(node.vis_details.x)
    y.append(node.vis_details.y)
    print(f"{node.details.state_name} ({node.vis_details.x}, {node.vis_details.y})")
    for child in node.children:
        display_tree(child)
        plt.plot([x_parent, child.vis_details.x], [y_parent, child.vis_details.y], "r-")


x = []
y = []


def main_test():
    root = create_tree()
    algorithm_result = Walkers.buchheim(root)
    print("Walkers algorithm finished")

    display_tree(algorithm_result)

    print("display_tree finished")
    plt.scatter(x, y)
    plt.show()


main_test()
