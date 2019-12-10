from PyQt5.QtWidgets import QWidget, QFileDialog

from src.main_application.GUI_utils import TREES_PATH
from src.serialization.serializator_csv import CsvSerializator
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.canvas import MonteCarloTreeCanvas
from src.visualisation_drawing.canvas_widget_layout import MonteCarloTreeWidgetLayout


class MonteCarloTreeCanvasWidget(QWidget):
    def __init__(self, sequences):
        super().__init__()
        self._setup_widget(sequences)

    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        self.layout.fill_right_panel_info(node)

    def _handle_reset_button_clicked_event(self):
        self.layout.canvas.reset_view()

    def _handle_serialize_button_clicked_event(self):
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree", TREES_PATH, "Csv files (*.csv)")
        serializator = CsvSerializator()
        serializator.save_node_to_path(self.layout.canvas.root, path)
        print(f"Saved file: {path}")

    def _make_arrow_buttons_enabled_or_disabled(self):
        current_tree_index = self.canvas.tree_index
        if current_tree_index == 0:
            self.layout.left_button.setEnabled(False)
        elif current_tree_index == 1:
            self.layout.left_button.setEnabled(True)
        if current_tree_index == len(self.canvas.trees) - 1:
            self.layout.right_button.setEnabled(False)
        elif current_tree_index == len(self.canvas.trees) - 2:
            self.layout.right_button.setEnabled(True)

    def _handle_left_arrow_button_clicked_event(self):
        tree_changed = self.canvas.make_previous_tree_as_root()
        if tree_changed:
            self.canvas.root.reset_walkers_data()
            self._make_arrow_buttons_enabled_or_disabled()
            self.canvas.use_root_data(self.canvas.root)

    def _handle_right_arrow_button_clicked_event(self):
        tree_changed = self.canvas.make_next_tree_as_root()
        if tree_changed:
            self.canvas.root.reset_walkers_data()
            self._make_arrow_buttons_enabled_or_disabled()
            self.canvas.use_root_data(self.canvas.root)

    def _setup_widget(self, sequences):
        self.canvas = MonteCarloTreeCanvas()
        self.layout = MonteCarloTreeWidgetLayout(self, self.canvas, sequences)
        self.layout.canvas.on_node_clicked += self._handle_node_clicked_event
        self.layout.serialize_button.clicked.connect(self._handle_serialize_button_clicked_event)
        self.layout.reset_button.clicked.connect(self._handle_reset_button_clicked_event)
        if sequences:
            self.layout.left_button.clicked.connect(self._handle_left_arrow_button_clicked_event)
            self.layout.right_button.clicked.connect(self._handle_right_arrow_button_clicked_event)
