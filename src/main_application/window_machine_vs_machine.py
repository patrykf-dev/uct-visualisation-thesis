from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen, get_button
from src.main_application.game_canvas import GameCanvas
from src.visualisation_drawing.canvas_widget import MonteCarloTreeCanvasWidget


class MachineVsMachineWindow(QMainWindow):
    def __init__(self, game_canvas: GameCanvas, parent):
        super(MachineVsMachineWindow, self).__init__(parent)
        self.game_canvas = game_canvas
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.game_canvas, 0, 0)
        self.tree_widget = MonteCarloTreeCanvasWidget()
        main_layout.addWidget(self.tree_widget, 0, 1)
        self.next_move_button = get_button("Make next move")
        self.next_move_button.clicked.connect(self.handle_next_move_button)
        main_layout.addWidget(self.next_move_button, 1, 0)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.game_canvas.on_update_tree += self._handle_update_tree

    def _handle_update_tree(self, sender, node):
        self.tree_widget.layout.canvas.use_root_data(node)

    def handle_next_move_button(self, sender):
        self.game_canvas.perform_algorithm_move()

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
