from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

from src.main_application.GUI_utils import center_window_on_screen
from src.visualisation_drawing.mc_tree_canvas_widget import MonteCarloTreeCanvasWidget


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MonteCarloTreeWindow, self).__init__(parent)
        self._setup_window()

    def _setup_window(self):
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        self.canvas_widget = MonteCarloTreeCanvasWidget()
        main_layout.addWidget(self.canvas_widget, 0, 0)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
