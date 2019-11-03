import matplotlib.pyplot as plt

import src.visualisation.walkers_algorithm as Walkers
from src.visualisation.tree import Tree

x = []
y = []


def display_tree(tree: Walkers.DrawTree):
    x_parent = tree.x
    y_parent = tree.y
    x.append(tree.x)
    y.append(tree.y)
    print(tree)
    for child in tree.children:
        display_tree(child)
        plt.plot([x_parent, child.x], [y_parent, child.y], "r-")


example_tree = Tree.get_tree()
print("Starting...")
algorithm_result = Walkers.buchheim(example_tree)
print("Finished")
display_tree(algorithm_result)

plt.scatter(x, y)
plt.show()
