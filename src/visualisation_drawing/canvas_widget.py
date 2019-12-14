from PyQt5.QtWidgets import QWidget, QFileDialog

from src.main_application.GUI_utils import TREES_PATH
from src.main_application.GUI_utils import show_eror_dialog
from src.serialization.serializator_binary import BinarySerializator
from src.serialization.serializator_csv import CsvSerializator
from src.uct.algorithm.mc_node import MonteCarloNode
from src.vispy import io
from src.visualisation_drawing.canvas import MonteCarloTreeCanvas
from src.visualisation_drawing.canvas_widget_layout import MonteCarloTreeWidgetLayout


class MonteCarloTreeCanvasWidget(QWidget):
    def __init__(self, sequences, trees_info=None):
        super().__init__()
        self._setup_widget(sequences, trees_info)

    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        self.layout.fill_right_panel_info(node)

    def _handle_reset_button_clicked_event(self):
        self.layout.canvas.reset_view()

    def _handle_serialize_csv_button_clicked_event(self):
        if not self.layout.canvas.tree.root:
            show_eror_dialog("Cannot save an empty tree!")
            return
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree", TREES_PATH, "Csv files (*.csv)")
        serializator = CsvSerializator()
        serializator.save_node_to_path(self.layout.canvas.tree.root, path)

    def _handle_serialize_binary_button_clicked_event(self):
        if not self.layout.canvas.tree.root:
            show_eror_dialog("Cannot save an empty tree!")
            return
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree", TREES_PATH, "Binary tree files (*.tree)")
        if path:
            serializator = BinarySerializator()
            serializator.save_node_to_path(self.layout.canvas.tree.root, path)

    def _handle_save_image_button_clicked_event(self):
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree", TREES_PATH, "Png files (*.png)")
        if path:
            image = self.layout.canvas.render()
            io.write_png(path, image)

    def _update_tree_info_labels(self):
        current_tree_index = self.canvas.tree_index
        number_of_trees = len(self.canvas.trees_info)
        text = f"Tree {current_tree_index + 1} of {number_of_trees}"
        self.layout.tree_info_number_label.setText(text)
        self.layout.tree_info_filename_label.setText(self.canvas.trees_info[self.canvas.tree_index].filename)

    def _handle_left_arrow_button_clicked_event(self):
        tree_changed = self.canvas.make_previous_tree_as_root()
        if tree_changed:
            self.canvas.tree.reset_vis_data()
            self._make_arrow_buttons_enabled_or_disabled()
            self._update_tree_info_labels()
            self.canvas.use_tree_data(self.canvas.tree)

    def _handle_right_arrow_button_clicked_event(self):
        tree_changed = self.canvas.make_next_tree_as_root()
        if tree_changed:
            self.canvas.tree.reset_vis_data()
            self._make_arrow_buttons_enabled_or_disabled()
            self._update_tree_info_labels()
            self.canvas.use_tree_data(self.canvas.tree)

    def _make_arrow_buttons_enabled_or_disabled(self):
        current_tree_index = self.canvas.tree_index
        if current_tree_index == 0:
            self.layout.left_button.setEnabled(False)
        elif current_tree_index == 1:
            self.layout.left_button.setEnabled(True)
        if current_tree_index == len(self.canvas.trees_info) - 1:
            self.layout.right_button.setEnabled(False)
        elif current_tree_index == len(self.canvas.trees_info) - 2:
            self.layout.right_button.setEnabled(True)

    def _setup_widget(self, sequences, trees_info=None):
        self.canvas = MonteCarloTreeCanvas(trees_info=trees_info)
        self.layout = MonteCarloTreeWidgetLayout(self, self.canvas, sequences)
        self.layout.canvas.on_node_clicked += self._handle_node_clicked_event
        self.layout.serialize_csv_button.clicked.connect(self._handle_serialize_csv_button_clicked_event)
        self.layout.serialize_binary_button.clicked.connect(self._handle_serialize_binary_button_clicked_event)
        self.layout.save_image_button.clicked.connect(self._handle_save_image_button_clicked_event)
        self.layout.reset_button.clicked.connect(self._handle_reset_button_clicked_event)
        if sequences:
            self._update_tree_info_labels()
            self.layout.left_button.clicked.connect(self._handle_left_arrow_button_clicked_event)
            self.layout.right_button.clicked.connect(self._handle_right_arrow_button_clicked_event)
