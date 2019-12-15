from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

from src.main_application.GUI_utils import center_window_on_screen
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, parent=None, trees_info=None, display_settings=None):
        super(MonteCarloTreeWindow, self).__init__(parent)
        self._setup_window(display_settings=display_settings, trees_info=trees_info)

    def _setup_window(self, display_settings, trees_info=None):
        main_widget = QWidget()
        main_layout = QGridLayout()
        self.setWindowTitle('UCT Tree Preview')
        main_widget.setLayout(main_layout)
        self.canvas_widget = MonteCarloTreeCanvasWidget(sequences=True, trees_info=trees_info,
                                                        display_settings=display_settings)
        main_layout.addWidget(self.canvas_widget, 0, 0)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
