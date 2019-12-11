from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

from src.main_application.GUI_utils import center_window_on_screen
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, parent=None, trees_info=None):
        super(MonteCarloTreeWindow, self).__init__(parent)
        self._setup_window(trees_info)

    def _setup_window(self, trees_info=None):
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        self.canvas_widget = MonteCarloTreeCanvasWidget(sequences=True, trees_info=trees_info)
        main_layout.addWidget(self.canvas_widget, 0, 0)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
