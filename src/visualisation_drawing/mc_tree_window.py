from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QFrame, QPushButton
from vispy import app as VispyApp

from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas


class MonteCarloTreeWindow(QMainWindow):
    NO_INFO_LABEL = "_NO INFO_"

    def __init__(self, canvas: MonteCarloTreeCanvas):
        super().__init__()
        self.canvas = canvas
        self.right_panel_widget = None
        self.labels = [
            ["Id", None],
            ["State name", None],
            ["Move name", None],
            ["Visits count", None],
            ["Visits count pre", None],
            ["Win score", None],
            ["Average prize", None],
            ["Current player", None]]
        self._setup_window()

    def show(self):
        super().show()
        VispyApp.run()
        self.setFocus()

    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        if node is None:
            self.right_panel_widget.change_background_color((160, 160, 160))
            for i in range(8):
                self.labels[i][1].setText(self.NO_INFO_LABEL)
        else:
            self.right_panel_widget.change_background_color((255, 255, 255))
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

    def _handle_reset_button_clicked_event(self):
        self.canvas.reset_view()

    def _setup_window(self):
        self.canvas.on_node_clicked += self._handle_node_clicked_event

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QGridLayout()
        self.right_panel_widget = PanelWidget()
        right_panel_layout = QGridLayout()
        self.reset_button = self._create_reset_button()
        self.reset_button.clicked.connect(self._handle_reset_button_clicked_event)

        main_widget.setLayout(main_layout)
        main_layout.addWidget(self.canvas.native, 0, 0)
        self.right_panel_widget.setLayout(right_panel_layout)
        main_layout.addWidget(self.right_panel_widget, 0, 1)
        main_layout.addWidget(self.reset_button, 1, 0)

        self._fill_right_panel(right_panel_layout)

    def _fill_right_panel(self, right_panel_layout):
        content_font = QtGui.QFont("Helvetica", 10)
        title_font = QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold)
        counter = 0
        for label in self.labels:
            label_title = QLabel()
            label_title.setText(label[0] + ": ")
            label_title.setFont(title_font)
            label_content = QLabel()
            label_content.setFont(content_font)
            label_content.setText(self.NO_INFO_LABEL)
            right_panel_layout.addWidget(label_title, counter, 0)
            right_panel_layout.addWidget(label_content, counter, 1)
            self.labels[counter][1] = label_content
            counter += 1

    def _create_reset_button(self):
        rc = QPushButton()
        button_font = QtGui.QFont("Helvetica", 10)
        rc.setText("Reset view")
        rc.setFont(button_font)
        return rc


class PanelWidget(QFrame):
    def __init__(self, *args):
        super(PanelWidget, self).__init__(*args)
        self.setStyleSheet("background-color: rgb(160, 160, 160); margin:2px; border:2px solid rgb(0, 0, 0);")
        # self.setMinimumWidth(300)
        self.setFixedSize(400, 400)

    def change_background_color(self, color):
        self.setStyleSheet(
            f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); margin:2px; border:2px solid rgb(0, 0, 0);")
