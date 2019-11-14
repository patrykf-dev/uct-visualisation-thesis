from src.trees.example_trees import create_sample_tree_1
from src.visualisation_algorithm.walkers_algorithm import ImprovedWalkersAlgorithm
from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas
from src.visualisation_drawing.mc_tree_window import MonteCarloTreeWindow

if __name__ == '__main__':
    root = create_sample_tree_1()
    alg = ImprovedWalkersAlgorithm()
    alg.buchheim_algorithm(root)

    canvas = MonteCarloTreeCanvas(root)
    window = MonteCarloTreeWindow(canvas)
    window.show()
