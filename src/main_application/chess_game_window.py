import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

from src.chess.chess_canvas import ChessCanvas


class ChessGameWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ChessGameWindow, self).__init__(parent)
        main_widget = QWidget()
        main_layout = QGridLayout()
        self.chess_widget = ChessCanvas()
        main_layout.addWidget(self.chess_widget, 0, 0)
        self.button = QPushButton("CLICK ME")
        self.button.clicked.connect(self._handle_click)
        main_layout.addWidget(self.button, 0, 1)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _handle_click(self):
        print("ASDASD")


def launch_chess_game_window():
    app = QApplication(sys.argv)
    w = ChessGameWindow()
    w.show()
    app.exec_()


if __name__ == "__main__":
    launch_chess_game_window()
