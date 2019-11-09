import numpy as np
import vispy
from vispy import app as VispyApp
from vispy.gloo import set_viewport, set_state, clear

from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.mc_tree_draw_data import MonteCarloTreeDrawDataRetriever
from src.visualisation_drawing.shaders.shader_reader import ShaderReader


class MonteCarloTreeCanvas(VispyApp.Canvas):
    def __init__(self, tree, **kwargs):
        VispyApp.Canvas.__init__(self, size=(1000, 1000), **kwargs)
        ps = self.pixel_scale
        retriever = MonteCarloTreeDrawDataRetriever()
        data = retriever.retrieve_draw_data(tree, ps)
        self.vbo = vispy.gloo.VertexBuffer(data.vertices)
        self.index = vispy.gloo.IndexBuffer(data.edges)

        self._bind_shaders()
        self._setup_matrices()

        set_viewport(0, 0, *self.physical_size)
        set_state(clear_color='gray', depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_edges.draw('lines', self.index)
        self.program_vertices.draw('points')

    def _setup_matrices(self):
        self.program_vertices['u_model'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_view'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_projection'] = np.eye(4, dtype=np.float32)

    def _bind_shaders(self):
        shader_reader = ShaderReader()
        self.program_vertices = vispy.gloo.Program(shader_reader.get_vertices_vshader(),
                                                   shader_reader.get_vertices_fshader())
        self.program_vertices['u_size'] = 1
        self.program_vertices['u_antialias'] = 1
        self.program_vertices.bind(self.vbo)

        self.program_edges = vispy.gloo.Program(shader_reader.get_edges_vshader(), shader_reader.get_edges_fshader())
        self.program_edges.bind(self.vbo)
