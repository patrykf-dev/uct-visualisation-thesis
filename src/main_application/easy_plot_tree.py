import matplotlib.pyplot as plt

from src.uct.algorithm.mc_node import MonteCarloNode


def display_tree(node: MonteCarloNode, vertices_x, vertices_y):
    x_parent = node.vis_details.x
    y_parent = node.vis_details.y
    vertices_x.append(node.vis_details.x)
    vertices_y.append(node.vis_details.y)
    for child in node.children:
        display_tree(child, vertices_x, vertices_y)
        plt.plot([x_parent, child.vis_details.x], [y_parent, child.vis_details.y], "r-")


def draw_tree(root: MonteCarloNode):
    vertices_x = []
    vertices_y = []
    display_tree(root, vertices_x, vertices_y)
    plt.scatter(vertices_x, vertices_y)
    plt.show()
