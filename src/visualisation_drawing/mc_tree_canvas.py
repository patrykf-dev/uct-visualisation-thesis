import numpy as np
import vispy
from axel import Event
from vispy import app as VispyApp
from vispy.gloo import set_viewport, set_state, clear

from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.mc_tree_draw_data import MonteCarloTreeDrawDataRetriever
from src.visualisation_drawing.shaders.shader_reader import ShaderReader
from src.visualisation_drawing.view_matrix_manager import ViewMatrixManager


class MonteCarloTreeCanvas(VispyApp.Canvas):
    KEY_CODE_LEFT = 16777234
    KEY_CODE_UP = 16777235
    KEY_CODE_RIGHT = 16777236
    KEY_CODE_DOWN = 16777237

    def __init__(self, root: MonteCarloNode, **kwargs):
        VispyApp.Canvas.__init__(self, size=(1000, 1000), **kwargs)
        self.mouse_tics = 0
        self.root = root

        self._setup_widget()
        self._bind_buffers()
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
        if self.mouse_tics < -17:
            self.mouse_tics = -17

        if self.mouse_tics == 0:
            scale = 0.9
        elif self.mouse_tics < 0:
            scale = 0.9 + (self.mouse_tics / 20)
        else:
            scale = 0.9 + (self.mouse_tics / 20)
        self.view_matrix_manager.change_scale(scale)
        self._update_view_matrix()

    def handle_mouse_click_event(self, event):
        pos = event.pos()
        x_clicked = pos.x()
        y_clicked = pos.y()
        width = self.native.frameGeometry().width()
        height = self.native.frameGeometry().height()
        world_x, world_y = self.view_matrix_manager.parse_click(x_clicked, y_clicked, width, height)

        clicked_node = self.tree_draw_data.get_node_at(world_x, world_y)
        self.on_node_clicked(clicked_node)

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

    def _bind_buffers(self):
        ps = self.pixel_scale
        retriever = MonteCarloTreeDrawDataRetriever()
        self.tree_draw_data = retriever.retrieve_draw_data(self.root, ps)
        self.vertices_buffer = vispy.gloo.VertexBuffer(self.tree_draw_data.vertices)
        self.edges_buffer = vispy.gloo.IndexBuffer(self.tree_draw_data.edges)

    def _setup_widget(self):
        self.native.setMinimumWidth(600)
        self.native.setMinimumHeight(600)
        self.native.keyPressEvent = self.handle_key_press_event
        self.native.wheelEvent = self.handle_wheel_event
        self.native.mousePressEvent = self.handle_mouse_click_event
        self.on_node_clicked = Event(self)
        set_viewport(0, 0, *self.physical_size)
        set_state(clear_color=(160 / 255, 160 / 255, 160 / 255, 1), depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))

    def reset_view(self):
        self.mouse_tics = 0
        self.view_matrix_manager.reset_view()
        self._update_view_matrix()
