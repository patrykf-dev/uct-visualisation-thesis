from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

from main_application.GUI_utils import amend_window_position_on_screen
from visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, parent=None, trees_paths=None, display_settings=None):
        super(MonteCarloTreeWindow, self).__init__(parent)
        self._setup_window(display_settings=display_settings, trees_paths=trees_paths)

    def _setup_window(self, display_settings, trees_paths=None):
        main_widget = QWidget()
        main_layout = QGridLayout()
        self.setWindowTitle('UCT Tree Preview')
        main_widget.setLayout(main_layout)
        self.canvas_widget = MonteCarloTreeCanvasWidget(sequences=True, trees_paths=trees_paths,
                                                        display_settings=display_settings)
        main_layout.addWidget(self.canvas_widget, 0, 0)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        amend_window_position_on_screen(self)
