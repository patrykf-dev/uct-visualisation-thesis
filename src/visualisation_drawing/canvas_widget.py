from PyQt5.QtWidgets import QWidget, QFileDialog

from src.main_application.GUI_utils import TREES_PATH
from src.serialization.serializator_csv import CsvSerializator
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.canvas import MonteCarloTreeCanvas
from src.visualisation_drawing.canvas_widget_layout import MonteCarloTreeWidgetLayout


class MonteCarloTreeCanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_widget()

    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        self.layout.fill_right_panel_info(node)

    def _handle_reset_button_clicked_event(self):
        self.layout.canvas.reset_view()

    def _handle_serialize_button_clicked_event(self):
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree", TREES_PATH, "Csv files (*.csv)")
        serializator = CsvSerializator()
        serializator.save_node_to_path(self.layout.canvas.root, path)
        print(f"Saved file: {path}")

    def _handle_left_arrow_button_clicked_event(self):
        tree_changed = self.canvas.make_previous_tree_as_root()
        if tree_changed:
            self.canvas.reset_view()
            self.canvas.use_root_data(self.canvas.root)

    def _handle_right_arrow_button_clicked_event(self):
        tree_changed = self.canvas.make_next_tree_as_root()
        if tree_changed:
            self.canvas.reset_view()
            self.canvas.use_root_data(self.canvas.root)

    def _setup_widget(self):
        self.canvas = MonteCarloTreeCanvas()
        self.layout = MonteCarloTreeWidgetLayout(self, self.canvas)
        self.layout.canvas.on_node_clicked += self._handle_node_clicked_event
        self.layout.serialize_button.clicked.connect(self._handle_serialize_button_clicked_event)
        self.layout.reset_button.clicked.connect(self._handle_reset_button_clicked_event)
        self.layout.left_button.clicked.connect(self._handle_left_arrow_button_clicked_event)
        self.layout.right_button.clicked.connect(self._handle_right_arrow_button_clicked_event)
