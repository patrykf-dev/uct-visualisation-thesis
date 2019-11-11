from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QGridLayout, QLabel
from vispy import app as VispyApp

from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, canvas: MonteCarloTreeCanvas):
        super().__init__()
        self.canvas = canvas
        self._setup_window(canvas)

    def show(self):
        super().show()
        VispyApp.run()
        self.setFocus()

    def _setup_window(self, canvas):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        main_layout.addWidget(canvas.native)
        right_panel_widget = QWidget()
        right_panel_layout = QGridLayout()
        self._fill_right_panel(right_panel_layout)
        right_panel_widget.setLayout(right_panel_layout)
        main_layout.addWidget(right_panel_widget)

    @staticmethod
    def _fill_right_panel(right_panel_layout):
        labels = ["Id", "State name", "Move name", "Visits count", "Visits count pre", "Win score", "Average prize"]
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        for i in range(len(labels)):
            label_title = QLabel()
            label_title.setText(labels[i] + ": ")
            label_title.setFont(bold_font)
            label_content = QLabel()
            label_content.setText("_EMPTY_")
            right_panel_layout.addWidget(label_title, i, 0)
            right_panel_layout.addWidget(label_content, i, 1)
