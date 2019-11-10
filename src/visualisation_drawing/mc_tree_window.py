from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from vispy import app as VispyApp

from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, canvas: MonteCarloTreeCanvas):
        super().__init__()
        self.mouse_tics = 0
        self.canvas = canvas
        self._setup_window(canvas)

    def show(self):
        super().show()
        VispyApp.run()

    def wheelEvent(self, event):
        self.mouse_tics = self.mouse_tics + event.angleDelta().y() / 120
        if self.mouse_tics > 30:
            self.mouse_tics = 30
        elif self.mouse_tics < -30:
            self.mouse_tics = -30
        self.canvas.react_to_mouse_scroll(self.mouse_tics)

    def _setup_window(self, canvas):
        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(QVBoxLayout())
        widget.layout().addWidget(canvas.native)
        widget.layout().addWidget(QPushButton())
