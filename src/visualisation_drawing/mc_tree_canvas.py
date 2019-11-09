import numpy as np
import vispy
from vispy import app as VispyApp
from vispy.gloo import set_viewport, set_state, clear

from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.shaders.shader_reader import ShaderReader

vertices_count = 0
edges_count = 0


def add_node_data(node: MonteCarloNode, vertices, edges):
    global vertices_count, edges_count
    x = node.vis_details.x / 12
    y = 0.5 - node.vis_details.y / 5.5
    vertices['a_position'][vertices_count] = (x, y, 0)
    parent_counter = vertices_count
    for child in node.children:
        vertices_count = vertices_count + 1
        edges[edges_count] = (vertices_count, parent_counter)
        edges_count = edges_count + 1
        add_node_data(child, vertices, edges)


def generate_graph_data(node: MonteCarloNode, ps):
    global vertices_count
    edges = np.zeros((29, 2)).astype(np.uint32)

    vertices = np.zeros(29, dtype=[('a_position', np.float32, 3),
                                   ('a_fg_color', np.float32, 4),
                                   ('a_bg_color', np.float32, 4),
                                   ('a_size', np.float32),
                                   ('a_linewidth', np.float32)])

    add_node_data(node, vertices, edges)

    vertices_count = vertices_count + 1

    vertices['a_fg_color'] = 0, 0, 0, 1
    color = np.random.uniform(0.1, 1.0, (vertices_count, 3))
    vertices['a_bg_color'] = np.hstack((color, np.ones((vertices_count, 1))))
    vertices['a_size'] = np.random.randint(size=vertices_count, low=15 * ps, high=18 * ps)
    vertices['a_linewidth'] = 1.0 * ps
    return vertices, edges


class MonteCarloTreeCanvas(VispyApp.Canvas):
    def __init__(self, tree, **kwargs):
        VispyApp.Canvas.__init__(self, size=(1000, 1000), **kwargs)

        ps = self.pixel_scale
        vertices, edges = generate_graph_data(tree, ps)

        u_antialias = 1

        self.vbo = vispy.gloo.VertexBuffer(vertices)
        self.index = vispy.gloo.IndexBuffer(edges)

        set_viewport(0, 0, *self.physical_size)

        shader_reader = ShaderReader()
        self.program_vertices = vispy.gloo.Program(shader_reader.get_vertices_vshader(),
                                                   shader_reader.get_vertices_fshader())
        self.program_vertices.bind(self.vbo)
        self.program_vertices['u_size'] = 1
        self.program_vertices['u_antialias'] = u_antialias
        self.program_vertices['u_model'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_view'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_projection'] = np.eye(4, dtype=np.float32)

        self.program_edges = vispy.gloo.Program(shader_reader.get_edges_vshader(), shader_reader.get_edges_fshader())
        self.program_edges.bind(self.vbo)

        set_state(clear_color='gray', depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_edges.draw('lines', self.index)
        self.program_vertices.draw('points')
