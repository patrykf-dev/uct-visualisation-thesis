from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QGridLayout, QLabel, QApplication
from vispy import app as VispyApp

from src.uct.algorithm.mc_node import MonteCarloNode


class MonteCarloTreeWindow(QMainWindow):
    def __init__(self, canvas):
        super().__init__()
        self.labels = [
            ["Id", None],
            ["State name", None],
            ["Move name", None],
            ["Visits count", None],
            ["Visits count pre", None],
            ["Win score", None],
            ["Average prize", None],
            ["Current player", None]]
        self._setup_window(canvas)

    def show(self):
        super().show()
        VispyApp.run()
        self.setFocus()



    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        self.labels[0][1].setText(str(node.id))

        if node.details:
            self.labels[1][1].setText(node.details.state_name)
            self.labels[2][1].setText(node.details.move_name)
            self.labels[3][1].setText(str(node.details.visits_count))
            self.labels[4][1].setText(str(node.details.visits_count_pre_modified))
            self.labels[5][1].setText(str(node.details.win_score))
            self.labels[6][1].setText(str(node.details.average_prize))
        if node.move:
            self.labels[7][1].setText(str(node.move.current_player))

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

    def _fill_right_panel(self, right_panel_layout):
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        counter = 0
        for label in self.labels:
            label_title = QLabel()
            label_title.setText(label[0] + ": ")
            label_title.setFont(bold_font)
            label_content = QLabel()
            label_content.setText("_NO INFO_")
            right_panel_layout.addWidget(label_title, counter, 0)
            right_panel_layout.addWidget(label_content, counter, 1)
            self.labels[counter][1] = label_content
            counter += 1
