from uct.algorithm.mc_tree import MonteCarloTree

from uct.algorithm.mc_node import MonteCarloNode


class ImprovedWalkersAlgorithm:
    distance = 1

    def __init__(self, tree: MonteCarloTree):
        self.tree = tree

    def buchheim_algorithm(self):
        self.tree.data.reset_to_defaults()
        self.first_walk(self.tree.root)
        self.second_walk(self.tree.root)

    def first_walk(self, node: MonteCarloNode):
        if not node.has_children():
            if node.leftmost_sibling():
                node.vis_details.x = node.left_sibling().vis_details.x + self.distance
            else:
                node.vis_details.x = 0
        else:
            default_ancestor = node.children[0]
            for child in node.children:
                self.first_walk(child)
                default_ancestor = self.apportion(child, default_ancestor)
            self.execute_shifts(node)
            midpoint = (node.children[0].vis_details.x + node.children[-1].vis_details.x) / 2
            child = node.left_sibling()
            if child:
                node.vis_details.x = child.vis_details.x + self.distance
                node.vis_details.mod = node.vis_details.x - midpoint
            else:
                node.vis_details.x = midpoint
        return node

    def second_walk(self, node: MonteCarloNode, mod=0, depth=0):
        node.vis_details.x += mod
        node.vis_details.y = depth
        self.tree.data.update_tree_visual_data(node)
        for child in node.children:
            self.tree.data.update_tree_visits_data(child, depth + 1)
            self.second_walk(child, mod + node.vis_details.mod, depth + 1)

    def apportion(self, node: MonteCarloNode, default_ancestor):
        left_brother = node.left_sibling()
        if left_brother:
            v_in_right = v_out_right = node
            v_in_left = left_brother
            v_out_left = node.leftmost_sibling()
            sum_in_right = v_in_right.vis_details.mod
            sum_out_right = v_out_right.vis_details.mod
            sum_in_left = v_in_left.vis_details.mod
            sum_out_left = v_out_left.vis_details.mod
            while v_in_left.right() and v_in_right.left():
                v_in_left = v_in_left.right()
                v_in_right = v_in_right.left()
                v_out_left = v_out_left.left()
                v_out_right = v_out_right.right()
                v_out_right.ancestor = node
                shift = (v_in_left.vis_details.x + sum_in_left) - (
                        v_in_right.vis_details.x + sum_in_right) + self.distance
                if shift > 0:
                    ancestor = self.ancestor(v_in_left, node, default_ancestor)
                    self.move_subtree(ancestor, node, shift)
                    sum_in_right = sum_in_right + shift
                    sum_out_right = sum_out_right + shift
                sum_in_left += v_in_left.vis_details.mod
                sum_in_right += v_in_right.vis_details.mod
                sum_out_left += v_out_left.vis_details.mod
                sum_out_right += v_out_right.vis_details.mod
            if v_in_left.right() and not v_out_right.right():
                v_out_right.vis_details.thread = v_in_left.right()
                v_out_right.vis_details.mod += sum_in_left - sum_out_right
            elif v_in_right.left() and not v_out_left.left():
                v_out_left.vis_details.thread = v_in_right.left()
                v_out_left.vis_details.mod += sum_in_right - sum_out_left
            if node.children:
                default_ancestor = node
        return default_ancestor

    @staticmethod
    def move_subtree(w_left: MonteCarloNode, w_right: MonteCarloNode, shift):
        subtrees = w_right.number - w_left.number
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
