import matplotlib.pyplot as plt

import src.trees.example_trees as ExampleTrees
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_algorithm.walkers_algorithm import ImprovedWalkersAlgorithm


def display_tree(node: MonteCarloNode):
    x_parent = node.vis_details.x
    y_parent = node.vis_details.y
    print(f"{node.details.state_name} - ({node.vis_details.x}, {node.vis_details.y})")
    x.append(node.vis_details.x)
    y.append(node.vis_details.y)
    for child in node.children:
        display_tree(child)
        plt.plot([x_parent, child.vis_details.x], [y_parent, child.vis_details.y], "r-")


x = []
y = []


def main_test():
    root = ExampleTrees.create_tree_1()
    alg = ImprovedWalkersAlgorithm()
    algorithm_result, spans = alg.buchheim_algorithm(root)
    print(f"Walkers algorithm finished - {spans[0]} x {spans[1]}")

    display_tree(algorithm_result)

    plt.scatter(x, y)
    plt.show()


main_test()
