import numpy as np
import vispy
from vispy import app as VispyApp
from vispy.gloo import set_viewport, set_state, clear

from src.visualisation_drawing.mc_tree_draw_data import MonteCarloTreeDrawDataRetriever
from src.visualisation_drawing.shaders.shader_reader import ShaderReader
from src.visualisation_drawing.view_matrix_manager import ViewMatrixManager


class MonteCarloTreeCanvas(VispyApp.Canvas):
    KEY_CODE_LEFT = 16777234
    KEY_CODE_UP = 16777235
    KEY_CODE_RIGHT = 16777236
    KEY_CODE_DOWN = 16777237

    def __init__(self, tree, **kwargs):
        VispyApp.Canvas.__init__(self, size=(1000, 1000), **kwargs)
        self.mouse_tics = 0
        self._setup_widget()
        self._bind_buffers(tree)
        self._bind_shaders()
        self._setup_matrices()

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_edges.draw('lines', self.edges_buffer)
        self.program_vertices.draw('points')

    def handle_key_press_event(self, event):
        x_diff = 0
        y_diff = 0
        if event.key() == self.KEY_CODE_RIGHT:
            x_diff = 0.1
        elif event.key() == self.KEY_CODE_LEFT:
            x_diff = -0.1
        elif event.key() == self.KEY_CODE_UP:
            y_diff = -0.1
        elif event.key() == self.KEY_CODE_DOWN:
            y_diff = 0.1

        self.view_matrix_manager.translate_view(x_diff, y_diff)
        self._update_view_matrix()

    def handle_wheel_event(self, event):
        self.mouse_tics += event.angleDelta().y() / 120
        if self.mouse_tics < -20:
            self.mouse_tics = -20

        if self.mouse_tics == 0:
            scale = 1
        elif self.mouse_tics < 0:
            scale = 1 + (self.mouse_tics / 20)
        else:
            scale = 1 + (self.mouse_tics / 20)
        self.view_matrix_manager.change_scale(scale)
        self._update_view_matrix()

    def _update_view_matrix(self):
        self.program_vertices['u_view'] = self.view_matrix_manager.view_matrix_1
        self.program_edges['u_view'] = self.view_matrix_manager.view_matrix_2
        self.update()

    def _setup_matrices(self):
        self.view_matrix_manager = ViewMatrixManager()
        self.program_vertices['u_model'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_view'] = self.view_matrix_manager.view_matrix_1
        self.program_vertices['u_projection'] = np.eye(4, dtype=np.float32)
        self.program_edges['u_model'] = np.eye(4, dtype=np.float32)
        self.program_edges['u_view'] = self.view_matrix_manager.view_matrix_2
        self.program_edges['u_projection'] = np.eye(4, dtype=np.float32)

    def _bind_shaders(self):
        shader_reader = ShaderReader()
        self.program_vertices = vispy.gloo.Program(shader_reader.get_vertices_vshader(),
                                                   shader_reader.get_vertices_fshader())
        self.program_vertices['u_size'] = 1
        self.program_vertices['u_antialias'] = 1
        self.program_vertices.bind(self.vertices_buffer)

        self.program_edges = vispy.gloo.Program(shader_reader.get_edges_vshader(), shader_reader.get_edges_fshader())
        self.program_edges.bind(self.vertices_buffer)

    def _bind_buffers(self, tree):
        ps = self.pixel_scale
        retriever = MonteCarloTreeDrawDataRetriever()
        data = retriever.retrieve_draw_data(tree, ps)
        self.vertices_buffer = vispy.gloo.VertexBuffer(data.vertices)
        self.edges_buffer = vispy.gloo.IndexBuffer(data.edges)

    def _setup_widget(self):
        self.native.keyPressEvent = self.handle_key_press_event
        self.native.wheelEvent = self.handle_wheel_event

        set_viewport(0, 0, *self.physical_size)
        set_state(clear_color='gray', depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))
