import math

import numpy as np

from src.uct.algorithm.mc_node import MonteCarloNode


class MonteCarloTreeDrawData:
    RADIUS = 0.02

    def __init__(self):
        self.vertices = None
        self.edges = None
        self.vertices_list = None

    def get_node_at(self, world_x, world_y):
        for vertex in self.vertices_list:
            center_x = vertex[0][0]
            center_y = vertex[0][1]
            distance = math.sqrt((center_x - world_x) * (center_x - world_x) +
                                 (center_y - world_y) * (center_y - world_y))
            if distance <= self.RADIUS:
                # print(
                #     f"You clicked ({round(world_x, 4)}, {round(world_y, 4)}) and that's vertex {str(vertex[0])} "
                #     f"for radius {round(self.RADIUS, 4)}")
                return vertex[1]

        # print(f"Empty click ({round(world_x, 4)}, {round(world_y, 4)})")
        return None


class MonteCarloTreeDrawDataRetriever:
    def __init__(self):
        self.vertices_count = 0
        self.edges_count = 0
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.max_visits_count = 0
        self.edge_type_desc = [("a_x", np.float32),
                               ("a_y", np.float32),
                               ("a_color", np.float32, 4),
                               ("a_width", np.float32)]

    def retrieve_draw_data(self, node: MonteCarloNode, ps) -> MonteCarloTreeDrawData:
        tmp_vertices = []
        tmp_edges = []
        self.walk_tree(node, tmp_vertices)
        self.vertices_count = self.vertices_count + 1
        self.second_walk_tree(tmp_vertices)
        self.third_walk_tree(node, tmp_edges)

        vertices = np.zeros(self.vertices_count, dtype=[("a_position", np.float32, 3),
                                                        ("a_fg_color", np.float32, 4),
                                                        ("a_bg_color", np.float32, 4),
                                                        ("a_radius", np.float32),
                                                        ("a_edge_color", np.float32, 4),
                                                        ("a_linewidth", np.float32)])

        vertices["a_fg_color"] = (0, 0, 0, 1)
        vertices["a_bg_color"] = (1, 1, 1, 1)
        vertices["a_radius"] = 16 * ps
        vertices["a_linewidth"] = 2.0 * ps

        for i in range(self.vertices_count):
            vertices[i]["a_position"] = tmp_vertices[i][0]
            vertices[i]["a_bg_color"] = tmp_vertices[i][2]

        edges = np.asarray(tmp_edges, dtype=self.edge_type_desc)

        data = MonteCarloTreeDrawData()
        data.vertices = vertices
        data.edges = edges
        data.vertices_list = tmp_vertices
        return data

    def walk_tree(self, node: MonteCarloNode, vertices):
        x = node.vis_details.x
        y = node.vis_details.y
        self.update_max_values(x, y, node)
        color = (1, 1, 0, 1)
        if node.move is not None:
            if node.move.player == 1:
                color = (1, 1, 1, 1)
            else:
                color = (0, 0, 0, 1)

        coords = (x, y, 0)
        vertices.append((coords, node, color))
        for child in node.children:
            self.vertices_count = self.vertices_count + 1
            self.edges_count = self.edges_count + 1
            self.walk_tree(child, vertices)

    def update_max_values(self, x, y, node):
        self.max_x = max(x, self.max_x)
        self.min_x = min(x, self.min_x)
        self.max_y = max(y, self.max_y)
        self.min_y = min(y, self.min_y)
        if node.parent is not None:
            self.max_visits_count = max(node.details.visits_count, self.max_visits_count)

    def second_walk_tree(self, vertices):
        x_span = self.max_x - self.min_x
        y_span = self.max_y - self.min_y
        for i in range(len(vertices)):
            x = vertices[i][0][0]
            y = vertices[i][0][1]
            new_x = (x - self.min_x - (x_span / 2)) / (x_span * 0.5)
            new_y = -(y - self.min_y - (y_span / 2)) / (y_span * 0.5)
            vertices[i] = ((new_x, new_y, 0), vertices[i][1], vertices[i][2])
            vertices[i][1].vis_details.x = new_x
            vertices[i][1].vis_details.y = new_y

    def third_walk_tree(self, node: MonteCarloNode, edges):
        for child in node.children:
            edge_color = self.get_edge_color(child.details.visits_count)
            edge1 = np.array((node.vis_details.x, node.vis_details.y, edge_color, 1), dtype=self.edge_type_desc)
            edge2 = np.array((child.vis_details.x, child.vis_details.y, edge_color, 1), dtype=self.edge_type_desc)
            edges.append(edge1)
            edges.append(edge2)
            self.third_walk_tree(child, edges)

    def get_edge_color(self, visits):
        fraction = visits / self.max_visits_count
        if fraction < 0.3:
            fraction += 0.3
        red = ((1 - fraction) * 255) / 255
        green = (fraction * 255) / 255
        print(f"Visits: {visits}/{self.max_visits_count} -> ({red}, {green}, {0})Fraction: {fraction}")
        return red, green, 0, 1
