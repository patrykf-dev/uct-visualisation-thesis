from PyQt5.QtWidgets import QMainWindow, QFileDialog
from vispy import app as VispyApp

from src.serialization.serializator_csv import CsvSerializator
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_drawing.mc_tree_canvas import MonteCarloTreeCanvas
from src.visualisation_drawing.mc_tree_window_layout import MonteCarloTreeWindowLayout


class MonteCarloTreeWindow(QMainWindow):

    def __init__(self, canvas: MonteCarloTreeCanvas):
        super().__init__()
        self._setup_window(canvas)

    def show(self):
        super().show()
        VispyApp.run()
        self.setFocus()

    def _handle_node_clicked_event(self, sender, node: MonteCarloNode):
        self.layout.fill_right_panel_info(node)

    def _handle_reset_button_clicked_event(self):
        self.layout.canvas.reset_view()

    def _handle_serialize_button_clicked_event(self):
        path, category = QFileDialog.getSaveFileName(self, "Serialize tree", "", "Csv files (*.csv)")
        serializator = CsvSerializator()
        serializator.save_node_to_path(self.layout.canvas.root, path)
        print(f"Saved file: {path}")

    def _setup_window(self, canvas):
        self.layout = MonteCarloTreeWindowLayout(canvas)
        self.setCentralWidget(self.layout.main_widget)
        self.layout.canvas.on_node_clicked += self._handle_node_clicked_event
        self.layout.serialize_button.clicked.connect(self._handle_serialize_button_clicked_event)
        self.layout.reset_button.clicked.connect(self._handle_reset_button_clicked_event)
