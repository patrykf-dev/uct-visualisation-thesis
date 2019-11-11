import numpy as np

from src.uct.algorithm.mc_node import MonteCarloNode


class MonteCarloTreeDrawData:
    def __init__(self):
        self.vertices = None
        self.edges = None


class MonteCarloTreeDrawDataRetriever:
    def __init__(self):
        self.vertices_count = 0
        self.edges_count = 0
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def retrieve_draw_data(self, node: MonteCarloNode, ps, scale_vertices=True) -> MonteCarloTreeDrawData:
        tmp_vertices = []
        tmp_edges = []
        self.walk_tree(node, tmp_vertices, tmp_edges)
        self.vertices_count = self.vertices_count + 1

        if scale_vertices:
            self.scale_vertices_coordinates(tmp_vertices)

        # print(f"{self.max_x} x {self.min_x}   {self.max_y} x {self.min_y}")

        vertices = np.zeros(self.vertices_count, dtype=[("a_position", np.float32, 3),
                                                        ("a_fg_color", np.float32, 4),
                                                        ("a_bg_color", np.float32, 4),
                                                        ("a_size", np.float32),
                                                        ("a_linewidth", np.float32)])

        vertices["a_fg_color"] = (0, 0, 0, 1)
        vertices["a_bg_color"] = (1, 1, 1, 1)
        vertices["a_size"] = 16 * ps
        vertices["a_linewidth"] = 2.0 * ps

        for i in range(self.vertices_count):
            vertices[i]["a_position"] = tmp_vertices[i]
        edges = np.asarray(tmp_edges, dtype=np.uint32)

        data = MonteCarloTreeDrawData()
        data.vertices = vertices
        data.edges = edges
        return data

    def walk_tree(self, node: MonteCarloNode, vertices, edges):
        x = node.vis_details.x
        y = node.vis_details.y
        self.update_bounds(x, y)
        # print(f"Adding vertex ({x}, {y})")
        vertices.append((x, y, 0))
        parent_counter = self.vertices_count
        for child in node.children:
            self.vertices_count = self.vertices_count + 1
            edges.append((self.vertices_count, parent_counter))
            self.edges_count = self.edges_count + 1
            self.walk_tree(child, vertices, edges)

    def update_bounds(self, x, y):
        self.max_x = max(x, self.max_x)
        self.min_x = min(x, self.min_x)
        self.max_y = max(y, self.max_y)
        self.min_y = min(y, self.min_y)

    def scale_vertices_coordinates(self, vertices):
        x_span = self.max_x - self.min_x
        y_span = self.max_y - self.min_y
        for i in range(len(vertices)):
            x = vertices[i][0]
            y = vertices[i][1]
            new_x = (x - self.min_x - (x_span / 2)) / (x_span * 0.5)
            new_y = -(y - self.min_y - (y_span / 2)) / (y_span * 0.5)
            vertices[i] = (new_x, new_y, 0)
            # print(f"Scaled vertex: ({x}, {y}) -> ({new_x}, {new_y})")
