from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.chess.chess_canvas import ChessCanvas
from src.main_application.GUI_utils import center_window_on_screen
from src.visualisation_drawing.mc_tree_canvas_widget import MonteCarloTreeCanvasWidget


class PlayerVsMachineWindow(QMainWindow):
    def __init__(self, game_canvas: QWidget, parent):
        super(PlayerVsMachineWindow, self).__init__(parent)
        self.game_canvas = game_canvas
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.game_canvas, 0, 0)
        main_layout.addWidget(MonteCarloTreeCanvasWidget(), 0, 1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
