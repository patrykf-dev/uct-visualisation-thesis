import sys

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src import vispy
from src.vispy import app as VispyApp
from src.vispy.gloo import set_viewport, set_state, clear
from src.visualisation_drawing.shaders.shader_reader import ShaderReader


class TestCanvas(VispyApp.Canvas):
    def __init__(self, **kwargs):
        VispyApp.Canvas.__init__(self, **kwargs)
        self.native.setMinimumWidth(600)
        self.native.setMinimumHeight(600)
        set_viewport(0, 0, self.physical_size[0], self.physical_size[1])
        set_state(clear_color=(160 / 255, 160 / 255, 160 / 255, 1), depth_test=False, blend=True,
                  blend_func=("src_alpha", "one_minus_src_alpha"))
        clear()
        self._bind_buffers()
        self._bind_shaders()
        self._setup_matrices()

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_edges.draw("lines")

    def _bind_buffers(self):
        edges = self._get_edges_array()
        self.edges_buffer = vispy.gloo.VertexBuffer(edges)

    def _bind_shaders(self):
        reader = ShaderReader()
        self.program_edges = vispy.gloo.Program(reader._get_shader("EDGES_V_SHADER"),
                                                reader._get_shader("EDGES_F_SHADER"))
        self.program_edges.bind(self.edges_buffer)

    def _setup_matrices(self):
        self.program_edges["u_model"] = np.eye(4, dtype=np.float32)
        self.program_edges["u_view"] = np.eye(4, dtype=np.float32)
        self.program_edges["u_projection"] = np.eye(4, dtype=np.float32)

    @staticmethod
    def _get_edges_array():
        type_desc = [("a_x", np.float32),
                     ("a_y", np.float32),
                     ("a_color", np.float32, 4),
                     ("a_width", np.float32)]
        edges_array = np.zeros(4, dtype=type_desc)

        print(type(edges_array))
        first1 = np.array((-0.5, 0.5, (0, 0, 0, 1), 1), dtype=type_desc)
        first2 = np.array((0.5, -0.5, (0, 0, 0, 1), 1), dtype=type_desc)
        second1 = np.array((0.5, 0, (1, 0, 0, 1), 1), dtype=type_desc)
        second2 = np.array((0.5, 1, (1, 0, 0, 1), 1), dtype=type_desc)
        edges_array[0] = first1
        edges_array[1] = first2
        edges_array[2] = second1
        edges_array[3] = second2
        return edges_array


def launch_canvas():
    app = QtWidgets.QApplication([])
    window = QMainWindow()
    main_widget = QWidget()
    layout = QGridLayout()
    layout.addWidget(TestCanvas().native)
    main_widget.setLayout(layout)
    window.setCentralWidget(main_widget)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch_canvas()
