import math

import numpy as np

from src.uct.algorithm.mc_node import MonteCarloNode
from src.uct.algorithm.mc_tree import MonteCarloTree
from src.utils.math_utils import rational_function


class MonteCarloTreeDrawData:
    def __init__(self):
        self.vertices = None
        self.edges = None
        self.vertices_list = None

    def get_node_at(self, world_x, world_y, scale):
        radius = self._calculate_radius(scale)
        for vertex in self.vertices_list:
            center_x = vertex.vis_details.x
            center_y = vertex.vis_details.y
            distance = math.sqrt((center_x - world_x) * (center_x - world_x) +
                                 (center_y - world_y) * (center_y - world_y))
            if distance <= radius:
                return vertex
        return None

    @staticmethod
    def _calculate_radius(scale):
        a = 0.02165432696792
        b = -0.00978532958715
        return rational_function(scale, a, b)


class MonteCarloTreeDrawDataRetriever:
    def __init__(self, tree: MonteCarloTree, most_visited_color, least_visited_color):
        self.tree = tree
        self.most_visited_color = most_visited_color
        self.least_visited_color = least_visited_color
        self.x_span = self.tree.data.max_x - self.tree.data.min_x
        self.y_span = self.tree.data.max_y - self.tree.data.min_y
        self.vertices_count = 0
        self.edges_count = 0
        self.edge_type_desc = [("a_x", np.float32),
                               ("a_y", np.float32),
                               ("a_color", np.float32, 4),
                               ("a_width", np.float32)]

    def retrieve_draw_data(self) -> MonteCarloTreeDrawData:
        tmp_vertices = []
        tmp_edges = []
        self.walk_tree(self.tree.root, tmp_vertices, tmp_edges)

        vertices = np.zeros(self.vertices_count, dtype=[("a_position", np.float32, 3),
                                                        ("a_fg_color", np.float32, 4),
                                                        ("a_bg_color", np.float32, 4),
                                                        ("a_radius", np.float32),
                                                        ("a_linewidth", np.float32)])

        vertices["a_radius"] = 16
        vertices["a_linewidth"] = 2.0
        vertices["a_fg_color"] = (0.1, 0.1, 0.1, 1)

        for i in range(self.vertices_count):
            n = tmp_vertices[i]
            pos = (n.vis_details.x, n.vis_details.y, 1)
            vertices[i]["a_position"] = pos
            if n.move:
                if n.move.player == 1:
                    vertices[i]["a_bg_color"] = (1, 1, 1, 1)
                else:
                    vertices[i]["a_bg_color"] = (0, 0, 0, 1)
            else:
                vertices[i]["a_bg_color"] = (0, 0, 0, 1)

        edges = np.asarray(tmp_edges, dtype=self.edge_type_desc)

        data = MonteCarloTreeDrawData()
        data.vertices = vertices
        data.edges = edges
        data.vertices_list = tmp_vertices
        return data

    def walk_tree(self, node: MonteCarloNode, vertices, edges):
        """
        Update vis_details based on max values
        """
        self._scale_coordinates(node)
        self.vertices_count += 1
        vertices.append(node)
        for child in node.children:
            self.walk_tree(child, vertices, edges)
            self._add_edge(node, child, edges)
            self.edges_count += 1

    def _add_edge(self, parent: MonteCarloNode, child: MonteCarloNode, edges):
        """
        Add edges based on fixed vis_details
        """
        edge_color = self.get_edge_color(child.details.visits_count)
        edge1 = np.array((parent.vis_details.x, parent.vis_details.y, edge_color, 1), dtype=self.edge_type_desc)
        edge2 = np.array((child.vis_details.x, child.vis_details.y, edge_color, 1), dtype=self.edge_type_desc)
        edges.append(edge1)
        edges.append(edge2)

    def _scale_coordinates(self, node: MonteCarloNode):
        x = node.vis_details.x
        y = node.vis_details.y
        new_x = (x - self.tree.data.min_x - (self.x_span / 2))
        new_y = -(y - self.tree.data.min_y - (self.y_span / 2))
        if self.x_span > 0 and self.y_span > 0:
            new_x /= (self.x_span * 0.5)
            new_y /= (self.y_span * 0.5)
        node.vis_details.x = new_x
        node.vis_details.y = new_y

    def get_edge_color(self, visits):
        fraction = visits / self.tree.data.max_visits_count

        red_diff = fraction * (self.most_visited_color[0] - self.least_visited_color[0])
        green_diff = fraction * (self.most_visited_color[1] - self.least_visited_color[1])
        blue_diff = fraction * (self.most_visited_color[2] - self.least_visited_color[2])

        red = (self.least_visited_color[0] + red_diff) / 255
        green = (self.least_visited_color[1] + green_diff) / 255
        blue = (self.least_visited_color[2] + blue_diff) / 255
        return red, green, blue, 1
