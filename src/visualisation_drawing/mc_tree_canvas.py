import numpy as np
import vispy
from vispy import app as VispyApp
from vispy.gloo import set_viewport, set_state, clear

from src.visualisation_drawing.mc_tree_draw_data import MonteCarloTreeDrawDataRetriever
from src.visualisation_drawing.shaders.shader_reader import ShaderReader


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
        print(f"Key pressed canvas: {event.key()}")

    def handle_wheel_event(self, event):
        self.mouse_tics = self.mouse_tics + event.angleDelta().y() / 120
        if self.mouse_tics > 30:
            self.mouse_tics = 30
        elif self.mouse_tics < -30:
            self.mouse_tics = -30
        self.react_to_mouse_scroll(self.mouse_tics)

    def react_to_mouse_scroll(self, mouse_tics):
        if mouse_tics == 0:
            scale = 1
        elif mouse_tics < 0:
            scale = 1 + (mouse_tics / 30)
        else:
            scale = 1 + (mouse_tics / 30)
        self._scale_view(scale)
        self.update()

    def _setup_matrices(self):
        self.program_vertices['u_model'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_view'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_projection'] = np.eye(4, dtype=np.float32)
        self.program_edges['u_model'] = np.eye(4, dtype=np.float32)
        self.program_edges['u_view'] = np.eye(4, dtype=np.float32)
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

    def _scale_view(self, scale):
        self.program_vertices['u_view'] = np.copy(self.program_vertices['u_view'])
        self.program_edges['u_view'] = np.copy(self.program_edges['u_view'])
        self.program_vertices['u_view'][0] = scale
        self.program_vertices['u_view'][5] = scale
        self.program_vertices['u_view'][10] = scale
        self.program_edges['u_view'][0] = scale
        self.program_edges['u_view'][5] = scale
        self.program_edges['u_view'][10] = scale

    def _setup_widget(self):
        self.native.keyPressEvent = self.handle_key_press_event
        self.native.wheelEvent = self.handle_wheel_event

        set_viewport(0, 0, *self.physical_size)
        set_state(clear_color='gray', depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))
