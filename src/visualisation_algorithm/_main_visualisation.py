import matplotlib.pyplot as plt

import src.trees.example_trees as ExampleTrees
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_algorithm.walkers_algorithm import ImprovedWalkersAlgorithm


def display_tree(node: MonteCarloNode):
    x_parent = node.vis_details.x
    y_parent = node.vis_details.y
    x.append(node.vis_details.x)
    y.append(node.vis_details.y)
    for child in node.children:
        display_tree(child)
        plt.plot([x_parent, child.vis_details.x], [y_parent, child.vis_details.y], "r-")


x = []
y = []


def draw_tree(root: MonteCarloNode):
    alg = ImprovedWalkersAlgorithm()
    alg.buchheim_algorithm(root)
    display_tree(root)
    plt.scatter(x, y)
    plt.show()


if __name__ == '__main__':
    root = ExampleTrees.create_sample_tree_1()
    draw_tree(root)
