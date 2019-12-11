import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

from src import vispy
from src.main_application.sequence_utils import MonteCarloNodeSequenceInfo
from src.uct.algorithm.mc_node import MonteCarloNode
from src.uct.algorithm.mc_tree import MonteCarloTree
from src.utils.custom_event import CustomEvent
from src.vispy import app as VispyApp
from src.vispy.gloo import set_viewport, clear, set_state
from src.visualisation_algorithm_new.walkers_algorithm_new import ImprovedWalkersAlgorithmNew
from src.visualisation_drawing.draw_data import MonteCarloTreeDrawDataRetriever
from src.visualisation_drawing.shaders.shader_reader import ShaderReader
from src.visualisation_drawing.view_matrix_manager import ViewMatrixManager


class MonteCarloTreeCanvas(VispyApp.Canvas):
    def __init__(self, tree: MonteCarloTree = None, trees_info: MonteCarloNodeSequenceInfo = None, **kwargs):
        VispyApp.Canvas.__init__(self, **kwargs)
        self.previous_mouse_pos = None
        self.tree = tree
        self.trees_info = trees_info
        self.tree_index = 0
        self._setup_widget()
        if self.tree:
            self.use_tree_data(self.tree)

    def use_tree_data(self, tree: MonteCarloTree):
        self.tree = tree
        alg = ImprovedWalkersAlgorithmNew(self.tree)
        alg.buchheim_algorithm()
        self._bind_buffers()
        self._bind_shaders()
        self._setup_matrices()
        self.update()

    def make_next_tree_as_root(self):
        if self.tree_index + 1 < len(self.trees_info):
            self.tree_index += 1
            self.tree = self.trees_info[self.tree_index].tree
            return True
        return False

    def make_previous_tree_as_root(self):
        if self.tree_index >= 1:
            self.tree_index -= 1
            self.tree = self.trees_info[self.tree_index].tree
            return True
        return False

    def on_resize(self, event):
        set_viewport(0, 0, event.physical_size[0], event.physical_size[1])

    def on_draw(self, event):
        clear(color=True, depth=True)
        if self.tree:
            self.program_edges.draw("lines")
            self.program_vertices.draw("points")

    def handle_wheel_event(self, event):
        if not self.tree:
            return
        wheel_direction = event.angleDelta().y()

        if wheel_direction < 0:
            self.view_matrix_manager.zoom_out()
        else:
            self.view_matrix_manager.zoom_in()
        self._update_view_matrix()

    def _setup_matrices(self):
        self.view_matrix_manager = ViewMatrixManager()
        self.program_vertices["u_model"] = np.eye(4, dtype=np.float32)
        self.program_vertices["u_view"] = self.view_matrix_manager.view_matrix_1
        self.program_vertices["u_projection"] = self.view_matrix_manager.projection_matrix_1
        self.program_edges["u_model"] = np.eye(4, dtype=np.float32)
        self.program_edges["u_view"] = self.view_matrix_manager.view_matrix_2
        self.program_edges["u_projection"] = self.view_matrix_manager.projection_matrix_2
        self.program_vertices["u_radius_multiplier"] = self.view_matrix_manager.scale

    def _bind_shaders(self):
        shader_reader = ShaderReader()
        self.program_vertices = vispy.gloo.Program(shader_reader.get_vertices_vshader(),
                                                   shader_reader.get_vertices_fshader())
        self.program_vertices["u_radius_multiplier"] = 3
        self.program_vertices["u_antialias"] = 1
        self.program_vertices.bind(self.vertices_buffer)

        self.program_edges = vispy.gloo.Program(shader_reader.get_edges_vshader(), shader_reader.get_edges_fshader())
        self.program_edges.bind(self.edges_buffer)

    def _bind_buffers(self):
        ps = self.pixel_scale
        retriever = MonteCarloTreeDrawDataRetriever(self.tree)
        self.tree_draw_data = retriever.retrieve_draw_data(ps)
        self.vertices_buffer = vispy.gloo.VertexBuffer(self.tree_draw_data.vertices)
        self.edges_buffer = vispy.gloo.VertexBuffer(self.tree_draw_data.edges)

    def handle_mouse_click_event(self, event):
        if not self.tree:
            return
        pos = event.pos()
        if event.button() == QtCore.Qt.RightButton:
            QApplication.setOverrideCursor(QCursor(QtCore.Qt.ClosedHandCursor))
            self.previous_mouse_pos = pos
        elif event.button() == QtCore.Qt.LeftButton:
            x_clicked = pos.x()
            y_clicked = pos.y()
            width = self.native.frameGeometry().width()
            height = self.native.frameGeometry().height()
            world_x, world_y = self.view_matrix_manager.parse_click(x_clicked, y_clicked, width, height)

            clicked_node = self.tree_draw_data.get_node_at(world_x, world_y, self.view_matrix_manager.scale)
            self.on_node_clicked.fire(self, earg=clicked_node)

    def handle_mouse_move_event(self, event):
        if not self.tree:
            return
        if event.buttons() == QtCore.Qt.RightButton:
            diff = self.previous_mouse_pos - event.pos()

            self.previous_mouse_pos = event.pos()

            size = self.native.frameGeometry()
            self.view_matrix_manager.translate_view(diff.x() / size.width(), diff.y() / size.height())
            self._update_view_matrix()

    def _update_view_matrix(self):
        self.program_vertices["u_view"] = self.view_matrix_manager.view_matrix_1
        self.program_edges["u_view"] = self.view_matrix_manager.view_matrix_2
        self.program_vertices["u_projection"] = self.view_matrix_manager.projection_matrix_1
        self.program_edges["u_projection"] = self.view_matrix_manager.projection_matrix_2
        self.update()

    def handle_mouse_release_event(self, event):
        QApplication.setOverrideCursor(QCursor(QtCore.Qt.ArrowCursor))

    def _setup_widget(self):
        self.native.setMinimumWidth(600)
        self.native.setMinimumHeight(600)
        self.native.wheelEvent = self.handle_wheel_event
        self.native.mousePressEvent = self.handle_mouse_click_event
        self.native.mouseMoveEvent = self.handle_mouse_move_event
        self.native.mouseReleaseEvent = self.handle_mouse_release_event
        self.on_node_clicked = CustomEvent()
        set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
        set_state(clear_color=(160 / 255, 160 / 255, 160 / 255, 1), depth_test=False, blend=True,
                  blend_func=("src_alpha", "one_minus_src_alpha"))

    def reset_view(self):
        if self.root:
            self.view_matrix_manager.reset_view()
            self._update_view_matrix()
