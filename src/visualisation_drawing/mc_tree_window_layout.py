from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy

from src.main_application.GUI_utils import DEFAULT_FONT, get_button, get_non_resizable_label
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas


class MonteCarloTreeWindowLayout:
    NO_INFO_LABEL = "-NO INFO-"

    def __init__(self, canvas: MonteCarloTreeCanvas):
        self.main_widget = None
        self.canvas = canvas
        self.reset_button = QPushButton()
        self.serialize_button = QPushButton()
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
        self._create_layout()

    def fill_right_panel_info(self, node: MonteCarloNode):
        if node is None:
            self._set_right_panel_color((160, 160, 160))
            for i in range(8):
                self.labels[i][1].setText(self.NO_INFO_LABEL)
        else:
            self._set_right_panel_color((255, 255, 255))
            self.labels[0][1].setText(str(node.id))
            if node.details:
                self.labels[1][1].setText(node.details.state_name)
                self.labels[2][1].setText(node.details.move_name)
                self.labels[3][1].setText(str(node.details.visits_count))
                self.labels[4][1].setText(str(node.details.visits_count_pre_modified))
                self.labels[5][1].setText(str(node.details.win_score))
                self.labels[6][1].setText(str(node.details.average_prize))
            if node.move:
                self.labels[7][1].setText(str(node.move.player))

    def _create_layout(self):
        self.main_widget = QWidget()
        main_layout = QGridLayout()
        self.main_widget.setLayout(main_layout)

        self._fill_right_panel_contents()

        self.reset_button = get_button("Reset view")
        self.serialize_button = get_button("Save tree to csv file")

        main_layout.addWidget(self.canvas.native, 0, 0)
        main_layout.addWidget(self.right_panel_widget, 0, 1)
        main_layout.addWidget(self.reset_button, 1, 0)
        main_layout.addWidget(self.serialize_button, 2, 0)

    def _fill_right_panel_contents(self):
        self.right_panel_widget = QWidget()
        self.right_panel_widget.setMinimumSize(400, 250)
        self.right_panel_widget.setObjectName("box")
        right_panel_layout = QGridLayout()
        self.right_panel_widget.setLayout(right_panel_layout)
        self._set_right_panel_color((160, 160, 160))

        self.right_panel_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        counter = 0
        for label in self.labels:
            label_title = get_non_resizable_label()
            label_title.setText(label[0] + ": ")
            label_content = get_non_resizable_label()
            label_content.setFont(DEFAULT_FONT)
            label_content.setText(self.NO_INFO_LABEL)
            right_panel_layout.addWidget(label_title, counter, 0)
            right_panel_layout.addWidget(label_content, counter, 1)
            self.labels[counter][1] = label_content
            counter += 1

    def _set_right_panel_color(self, color):
        self.right_panel_widget.setStyleSheet(
            "QWidget#box{background-color: rgb" + str(color) + "; margin:2px; border:2px solid rgb(0, 0, 0);}")
