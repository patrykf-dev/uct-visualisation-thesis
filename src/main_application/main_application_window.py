import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from src.chess.game import launch_game
from src.main_application.main_application_window_layout import MainApplicationWindowLayout


class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        self.layout = MainApplicationWindowLayout()
        self.setCentralWidget(self.layout.main_widget)
        self.layout.play_button.clicked.connect(self._handle_play_button)

    def _handle_play_button(self):
        launch_game()


def launch_application():
    try:
        window = MainApplicationWindow()
        window.show()
    except:
        print("ERRRRO")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainApplicationWindow()
    myapp.show()
    sys.exit(app.exec_())
