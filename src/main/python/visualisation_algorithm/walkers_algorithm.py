
from uct.algorithm.mc_tree import MonteCarloTree

from uct.algorithm.mc_node import MonteCarloNode


class ImprovedWalkersAlgorithm:
    """
    Class implements Improved Walker's Algorithm to draw trees in linear time.
    Source: http://dirk.jivas.de/papers/buchheim02improving.pdf
    'distance' field is the basic distance unit between two neighboring nodes.
    The class is dependent on MonteCarloTree and MonteCarloNode classes.
    """
    distance = 1

    def __init__(self, tree: MonteCarloTree):
        self.tree = tree

    def buchheim_junger_leipert_algorithm(self):
        """
                Executes Improved Walker's Algorithm and calculates positions of each node in the tree. Result is stored inside
                'tree' field.

		Returns:
			None                
		"""
        self.tree.data.reset_to_defaults()
        self._first_walk(self.tree.root)
        self._second_walk(self.tree.root)

    def _first_walk(self, node: MonteCarloNode):
        if not node.has_children():
            if node.leftmost_sibling():
                node.vis_details.x = node.left_sibling().vis_details.x + self.distance
            else:
                node.vis_details.x = 0
        else:
            default_ancestor = node.children[0]
            for child in node.children:
                self._first_walk(child)
                default_ancestor = self._apportion(child, default_ancestor)
            self._execute_shifts(node)
            midpoint = (node.children[0].vis_details.x + node.children[-1].vis_details.x) / 2
            child = node.left_sibling()
            if child:
                node.vis_details.x = child.vis_details.x + self.distance
                node.vis_details.mod = node.vis_details.x - midpoint
            else:
                node.vis_details.x = midpoint
        return node

    def _second_walk(self, node: MonteCarloNode, mod=0, depth=0):
        node.vis_details.x += mod
        node.vis_details.y = depth
        self.tree.data.update_tree_visual_data(node)
        for child in node.children:
            self.tree.data.update_tree_visits_data(child, depth + 1)
            self._second_walk(child, mod + node.vis_details.mod, depth + 1)

    def _apportion(self, node: MonteCarloNode, default_ancestor):
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
                v_out_right._ancestor = node
                shift = (v_in_left.vis_details.x + sum_in_left) - (
                        v_in_right.vis_details.x + sum_in_right) + self.distance
                if shift > 0:
                    ancestor = self._ancestor(v_in_left, node, default_ancestor)
                    self._move_subtree(ancestor, node, shift)
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
    def _move_subtree(w_left: MonteCarloNode, w_right: MonteCarloNode, shift):
        subtrees = w_right.number - w_left.number
        if subtrees == 0:
            subtrees = 1
        w_right.vis_details.change -= shift / subtrees
        w_right.vis_details.shift += shift
        w_left.vis_details.change += shift / subtrees
        w_right.vis_details.x += shift
        w_right.vis_details.mod += shift

    @staticmethod
    def _execute_shifts(v: MonteCarloNode):
        shift = change = 0
        for child in v.children[::-1]:
            child.vis_details.x += shift
            child.vis_details.mod += shift
            change += child.vis_details.change
            shift += child.vis_details.shift + change

    @staticmethod
    def _ancestor(node: MonteCarloNode, v: MonteCarloNode, default_ancestor):
        if node.parent in v.parent.children:
            return node.parent
        else:
            return default_ancestor

