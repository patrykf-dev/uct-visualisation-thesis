from src.uct.algorithm.mc_node import MonteCarloNode
from src.uct.algorithm.mc_tree import MonteCarloTree


class ImprovedWalkersAlgorithm:
    def __init__(self, tree: MonteCarloTree):
        self.tree = tree

    def buchheim_algorithm(self):
        self.tree.data.reset_to_defaults()
        self.first_walk(self.tree.root)
        self.second_walk(self.tree.root)

    def first_walk(self, node: MonteCarloNode, distance=1):
        if len(node.children) == 0:
            if node.lmost_sibling:
                node.vis_details.x = node.lbrother().vis_details.x + distance
            else:
                node.vis_details.x = 0
        else:
            default_ancestor = node.children[0]
            for child in node.children:
                self.first_walk(child)
                default_ancestor = self.apportion(child, default_ancestor, distance)
            self.execute_shifts(node)

            midpoint = (node.children[0].vis_details.x + node.children[-1].vis_details.x) / 2

            child = node.lbrother()
            if child:
                node.vis_details.x = child.vis_details.x + distance
                node.vis_details.mod = node.vis_details.x - midpoint
            else:
                node.vis_details.x = midpoint
        return node

    def second_walk(self, node: MonteCarloNode, m=0, depth=0):
        node.vis_details.x += m
        node.vis_details.y = depth
        self.tree.data.update_tree_visual_data(node)
        for child in node.children:
            self.tree.data.update_tree_visits_data(child, depth + 1)
            self.second_walk(child, m + node.vis_details.mod, depth + 1)

    def apportion(self, node: MonteCarloNode, default_ancestor, distance):
        left_brother = node.lbrother()
        if left_brother is not None:
            vir = vor = node
            vil = left_brother
            vol = node.lmost_sibling
            sir = sor = node.vis_details.mod
            sil = vil.vis_details.mod
            sol = vol.vis_details.mod
            while vil.right() and vir.left():
                vil = vil.right()
                vir = vir.left()
                vol = vol.left()
                vor = vor.right()
                vor.ancestor = node
                shift = (vil.vis_details.x + sil) - (vir.vis_details.x + sir) + distance
                if shift > 0:
                    ancestor = self.ancestor(vil, node, default_ancestor)
                    self.move_subtree(ancestor, node, shift)
                    sir = sir + shift
                    sor = sor + shift
                sil += vil.vis_details.mod
                sir += vir.vis_details.mod
                sol += vol.vis_details.mod
                sor += vor.vis_details.mod
            if vil.right() and not vor.right():
                vor.vis_details.thread = vil.right()
                vor.vis_details.mod += sil - sor
            elif vir.left() and not vol.left():
                vol.vis_details.thread = vir.left()
                vol.vis_details.mod += sir - sol
            if node.children:
                default_ancestor = node
        return default_ancestor

    @staticmethod
    def move_subtree(w_left: MonteCarloNode, w_right: MonteCarloNode, shift):
        subtrees = w_right.number - w_left.number
        # TODO zmieniam, sypalo ZeroDivisionError
        if subtrees == 0:
            subtrees = 1
        w_right.vis_details.change -= shift / subtrees
        w_right.vis_details.shift += shift
        w_left.vis_details.change += shift / subtrees
        w_right.vis_details.x += shift
        w_right.vis_details.mod += shift

    @staticmethod
    def execute_shifts(v: MonteCarloNode):
        shift = change = 0
        for child in v.children[::-1]:
            child.vis_details.x += shift
            child.vis_details.mod += shift
            change += child.vis_details.change
            shift += child.vis_details.shift + change

    @staticmethod
    def ancestor(node: MonteCarloNode, v: MonteCarloNode, default_ancestor):
        if node.parent in v.parent.children:
            return node.parent
        else:
            return default_ancestor
