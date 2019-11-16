from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.chess.chess_canvas import ChessCanvas
from src.main_application.GUI_utils import center_window_on_screen
from src.visualisation_drawing.mc_tree_canvas_widget import MonteCarloTreeCanvasWidget


class ChessGameWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ChessGameWindow, self).__init__(parent)
        main_widget = QWidget()
        main_layout = QGridLayout()
        self.chess_widget = ChessCanvas()
        main_layout.addWidget(self.chess_widget, 0, 0)
        main_layout.addWidget(MonteCarloTreeCanvasWidget(), 0, 1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
