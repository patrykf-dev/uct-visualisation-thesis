from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from src.main_application.GUI_utils import center_window_on_screen


class PlayerVsPlayerWindow(QMainWindow):
    def __init__(self, game_canvas: QWidget, parent):
        super(PlayerVsPlayerWindow, self).__init__(parent)
        self.game_canvas = game_canvas
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.addWidget(self.game_canvas)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def showEvent(self, event):
        super().showEvent(event)
        center_window_on_screen(self)
