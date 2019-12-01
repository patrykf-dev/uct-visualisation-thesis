from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen
from src.main_application.iteration_progress_widget import IterationProgressWidget
from src.main_application.mc_window_manager import MonteCarloWindowManager
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class PlayerVsMachineWindow(QMainWindow):
    def __init__(self, manager: MonteCarloWindowManager, parent):
        super(PlayerVsMachineWindow, self).__init__(parent)
        self.manager = manager
        self.tree_widget = MonteCarloTreeCanvasWidget()
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.manager.canvas, 0, 0, 2, 1)
        main_layout.addWidget(IterationProgressWidget(), 0, 1)
        main_layout.addWidget(self.tree_widget, 1, 1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.manager.on_update_tree += self._handle_update_tree

    def _handle_update_tree(self, sender, node):
        self.tree_widget.layout.canvas.use_root_data(node)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
