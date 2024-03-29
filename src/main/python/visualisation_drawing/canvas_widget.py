import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication

from main_application.GUI_utils import TREES_PATH, PYQT_KEY_CODE_RIGHT, PYQT_KEY_CODE_LEFT
from main_application.GUI_utils import show_eror_dialog
from serialization.serializator_binary import BinarySerializator
from serialization.serializator_csv import CsvSerializator
from uct.algorithm.mc_node import MonteCarloNode
from vispy import io
from visualisation_drawing.canvas import MonteCarloTreeCanvas
from visualisation_drawing.canvas_widget_layout import MonteCarloTreeWidgetLayout


class MonteCarloTreeCanvasWidget(QWidget):
    def __init__(self, sequences, display_settings, trees_paths=None):
        super().__init__()
        self._setup_widget(sequences, display_settings, trees_paths)

    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        self.layout.fill_node_panel_info(node)

    def _handle_reset_button_clicked_event(self):
        self.layout.canvas.reset_view()

    def serialize_csv(self):
        if not self.layout.canvas.tree:
            show_eror_dialog("Cannot save an empty tree!")
            return
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree to csv", TREES_PATH, "Csv files (*.csv)")
        if not path.endswith(".csv"):
            path += ".csv"
        if path:
            serializator = CsvSerializator()
            serializator.save_node_to_path(self.layout.canvas.tree.root, path)

    def serialize_binary(self):
        if not self.layout.canvas.tree:
            show_eror_dialog("Cannot save an empty tree!")
            return
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree to binary file", TREES_PATH, "Binary tree files (*.tree)")
        if not path.endswith(".tree"):
            path += ".tree"
        if path:
            serializator = BinarySerializator()
            serializator.save_node_to_path(self.layout.canvas.tree.root, path)

    def save_image(self):
        path, category = QFileDialog.getSaveFileName(self, "Save tree as image", TREES_PATH, "Png files (*.png)")
        if not path.endswith(".png"):
            path += ".png"
        if path:
            self.layout.canvas._smooth_enabled = False
            image = self.layout.canvas.render()
            self.layout.canvas._smooth_enabled = True
            io.write_png(path, image)

    def _handle_serialize_button_clicked_event(self):
        if self.layout.serialize_csv_radiobutton.isChecked():
            self.serialize_csv()
        elif self.layout.serialize_binary_radiobutton.isChecked():
            self.serialize_binary()
        else:
            return self.save_image()

    def _update_tree_info_labels(self):
        current_tree_index = self.canvas.tree_index
        number_of_trees = len(self.canvas.trees_paths)
        text = f"Tree {current_tree_index + 1} of {number_of_trees}"
        self.layout.tree_info_number_label.setText(text)
        tree_name = os.path.basename(self.canvas.trees_paths[self.canvas.tree_index])
        self.layout.tree_info_filename_label.setText(tree_name)

    def change_tree_in_sequence(self):
        self.layout.reset_node_panel_info()
        self.canvas.tree.reset_vis_data()
        self._make_arrow_buttons_enabled_or_disabled()
        self._update_tree_info_labels()
        tree = self.canvas.tree
        self.canvas.use_tree_data(tree)
        self.layout.fill_tree_details_panel_info(tree.data.vertices_count)

    def _handle_left_arrow_button_clicked_event(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        tree_changed = self.canvas.make_previous_tree_as_root()
        if tree_changed:
            self.change_tree_in_sequence()
        QApplication.restoreOverrideCursor()

    def _handle_right_arrow_button_clicked_event(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        tree_changed = self.canvas.make_next_tree_as_root()
        if tree_changed:
            self.change_tree_in_sequence()
        QApplication.restoreOverrideCursor()

    def _handle_jump_to_button_clicked_event(self):
        index = self.layout.jump_edit_line.text()
        if not index.isdigit():
            show_eror_dialog("Invalid tree number!")
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        tree_changed = self.canvas.make_selected_tree_as_root(int(index) - 1)
        if tree_changed:
            self.change_tree_in_sequence()
        else:
            show_eror_dialog("Invalid tree number!")
        QApplication.restoreOverrideCursor()

    def _make_arrow_buttons_enabled_or_disabled(self):
        current_tree_index = self.canvas.tree_index
        if current_tree_index == 0:
            self.layout.left_button.setEnabled(False)
        elif current_tree_index > 0:
            self.layout.left_button.setEnabled(True)
        if current_tree_index == len(self.canvas.trees_paths) - 1:
            self.layout.right_button.setEnabled(False)
        elif current_tree_index < len(self.canvas.trees_paths) - 1:
            self.layout.right_button.setEnabled(True)

    def handle_key_press_event(self, event):
        if event.key() == PYQT_KEY_CODE_RIGHT:
            self._handle_right_arrow_button_clicked_event()
        elif event.key() == PYQT_KEY_CODE_LEFT:
            self._handle_left_arrow_button_clicked_event()

    def setup_arrow_event_handler(self):
        self.canvas.native.keyPressEvent = self.handle_key_press_event

    def _setup_widget(self, sequences, display_settings, trees_paths=None):
        self.canvas = MonteCarloTreeCanvas(trees_paths=trees_paths, display_settings=display_settings)
        self.canvas.set_current_tree()
        self.layout = MonteCarloTreeWidgetLayout(self, self.canvas, sequences)
        self.layout.canvas.on_node_clicked += self._handle_node_clicked_event
        self.layout.serialize_button.clicked.connect(self._handle_serialize_button_clicked_event)
        self.layout.reset_button.clicked.connect(self._handle_reset_button_clicked_event)
        if sequences:
            self._update_tree_info_labels()
            self.layout.left_button.clicked.connect(self._handle_left_arrow_button_clicked_event)
            self.layout.right_button.clicked.connect(self._handle_right_arrow_button_clicked_event)
            self.layout.jump_button.clicked.connect(self._handle_jump_to_button_clicked_event)
            self.setup_arrow_event_handler()
