from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy

from src.main_application.GUI_utils import get_button, get_non_resizable_label, \
    get_box_background_stylesheet
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.canvas import MonteCarloTreeCanvas


class MonteCarloTreeWidgetLayout:
    NO_INFO_LABEL = "-NO INFO-"

    def __init__(self, main_widget, canvas: MonteCarloTreeCanvas, sequences):
        self.canvas = canvas
        self.reset_button = get_button("Reset view")
        self.serialize_csv_button = get_button("Save to csv file")
        self.serialize_binary_button = get_button("Save to binary file")
        self.save_image_button = get_button("Save to bitmap")
        self.node_panel_widget = None
        self.tree_details_panel_widget = None
        self.tree_details_labels = [
            ["Vertices count", None]]
        self.node_labels = [
            ["Id", None],
            ["State name", None],
            ["Move name", None],
            ["Visits count", None],
            ["Visits count pre", None],
            ["Win score", None],
            ["Average prize", None],
            ["Current player", None]]
        self._create_layout(main_widget, sequences)

    def reset_node_panel_info(self):
        self._set_node_panel_color((160, 160, 160))
        for i in range(len(self.node_labels)):
            self.node_labels[i][1].setText(self.NO_INFO_LABEL)

    def fill_tree_details_panel_info(self, vertices_count):
        self._set_tree_details_panel_color((255, 255, 255))
        self.tree_details_labels[0][1].setText(str(vertices_count))

    def fill_node_panel_info(self, node: MonteCarloNode):
        if node is None:
            self.reset_node_panel_info()
        else:
            self._set_node_panel_color((255, 255, 255))
            self.node_labels[0][1].setText(str(node.id))
            if node.details:
                self.node_labels[1][1].setText(node.details.state_name)
                self.node_labels[2][1].setText(node.details.move_name)
                self.node_labels[3][1].setText(str(node.details.visits_count))
                self.node_labels[4][1].setText(str(node.details.visits_count_pre_modified))
                self.node_labels[5][1].setText(str(node.details.win_score))
                self.node_labels[6][1].setText(str(node.details.average_prize))
            if node.move:
                self.node_labels[7][1].setText(str(node.move.player))

    def _create_left_right_button_widget(self):
        self.left_button = get_button("<<", 35)
        self.right_button = get_button(">>", 35)
        self.tree_info_number_label = get_non_resizable_label()
        self.tree_info_filename_label = get_non_resizable_label()
        self.left_right_widget = QWidget()
        left_right_layout = QGridLayout()
        self.left_right_widget.setLayout(left_right_layout)
        left_right_layout.addWidget(self.tree_info_filename_label, 0, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        if len(self.canvas.trees_info) > 1:
            left_right_layout.addWidget(self.tree_info_number_label, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
            left_right_layout.addWidget(self.left_button, 2, 0)
            left_right_layout.addWidget(self.right_button, 2, 1)
        else:
            left_right_layout.addWidget(self.left_button, 1, 0)
            left_right_layout.addWidget(self.right_button, 1, 1)

    def _create_layout(self, main_widget, sequences):
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)

        self.tree_details_panel_widget = self._get_panel(self.tree_details_labels, 400, 80)
        self.node_panel_widget = self._get_panel(self.node_labels, 400, 250)
        self._set_tree_details_panel_color((160, 160, 160))
        self._set_node_panel_color((160, 160, 160))

        if sequences:
            self._create_left_right_button_widget()
            if len(self.canvas.trees_info) >= 1:
                tree = self.canvas.trees_info[0].tree
                self.canvas.use_tree_data(tree)
                self.fill_tree_details_panel_info(tree.data.vertices_count)
                if len(self.canvas.trees_info) == 1:
                    self.right_button.setEnabled(False)
            self.left_button.setEnabled(False)

        main_layout.addWidget(self.canvas.native, 0, 0)

        panels_widget = QWidget()
        panels_layout = QGridLayout()
        panels_widget.setLayout(panels_layout)
        panels_layout.addWidget(self.tree_details_panel_widget, 0, 0, alignment=QtCore.Qt.AlignBottom)
        panels_layout.addWidget(self.node_panel_widget, 1, 0, alignment=QtCore.Qt.AlignTop)

        main_layout.addWidget(panels_widget, 0, 1)
        main_layout.addWidget(self.reset_button, 1, 0, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.serialize_csv_button, 2, 0, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.serialize_binary_button, 3, 0, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.save_image_button, 4, 0, alignment=QtCore.Qt.AlignCenter)
        if sequences:
            main_layout.addWidget(self.left_right_widget, 5, 0, alignment=QtCore.Qt.AlignCenter)

    def _get_panel(self, labels, width, height):
        rc = QWidget()
        rc.setMinimumSize(width, height)
        rc.setObjectName("box")
        layout = QGridLayout()
        rc.setLayout(layout)
        rc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for i, label in enumerate(labels):
            label_title = get_non_resizable_label()
            label_title.setText(label[0] + ": ")
            label_content = get_non_resizable_label()
            label_content.setText(self.NO_INFO_LABEL)
            layout.addWidget(label_title, i, 0)
            layout.addWidget(label_content, i, 1)
            labels[i][1] = label_content
        return rc

    def _set_node_panel_color(self, color):
        self.node_panel_widget.setStyleSheet(get_box_background_stylesheet(color))

    def _set_tree_details_panel_color(self, color):
        self.tree_details_panel_widget.setStyleSheet(get_box_background_stylesheet(color))
