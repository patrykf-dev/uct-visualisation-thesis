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
        self.x = 0
        self.y = 0
        self.scale = 1

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

        self.x = self.x + x_diff
        self.y = self.y + y_diff
        self.update_view()

    def look_at(self, x, y):
        eye = np.array([x, y, 0])
        center = np.array([x, y, 1])
        up = np.array([0, -1, 0])
        z = eye - center
        z = self.normalize(z)
        x = np.cross(up, z)
        y = np.cross(z, x)
        x = self.normalize(x)
        y = self.normalize(y)
        rc = np.array([
            [x[0], x[1], x[2], np.dot(-x, eye)],
            [y[0], -y[1], y[2], np.dot(-y, eye)],
            [z[0], z[1], z[2], np.dot(-z, eye)],
            [0, 0, 0, 1]
        ]).transpose()
        return rc

    @staticmethod
    def normalize(v):
        norm = np.linalg.norm(v, ord=1)
        if norm == 0:
            norm = np.finfo(v.dtype).eps
        return v / norm

    def handle_wheel_event(self, event):
        self.mouse_tics = self.mouse_tics + event.angleDelta().y() / 120
        if self.mouse_tics < -30:
            self.mouse_tics = -30
        self.react_to_mouse_scroll(self.mouse_tics)

    def react_to_mouse_scroll(self, mouse_tics):
        if mouse_tics == 0:
            self.scale = 1
        elif mouse_tics < 0:
            self.scale = 1 + (mouse_tics / 30)
        else:
            self.scale = 1 + (mouse_tics / 30)
        self.update_view()

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

    def update_view(self):
        view = self.look_at(self.x, self.y)
        self.program_vertices['u_view'] = view
        self.program_edges['u_view'] = view
        self._scale_view()
        self.update()

    def _scale_view(self):
        self.program_vertices['u_view'] = np.copy(self.program_vertices['u_view'])
        self.program_edges['u_view'] = np.copy(self.program_edges['u_view'])
        self.program_vertices['u_view'][0] = self.scale
        self.program_vertices['u_view'][5] = self.scale
        self.program_vertices['u_view'][10] = self.scale
        self.program_edges['u_view'][0] = self.scale
        self.program_edges['u_view'][5] = self.scale
        self.program_edges['u_view'][10] = self.scale

    def _setup_widget(self):
        self.native.keyPressEvent = self.handle_key_press_event
        self.native.wheelEvent = self.handle_wheel_event

        set_viewport(0, 0, *self.physical_size)
        set_state(clear_color='gray', depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

