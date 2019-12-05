from PyQt5.QtWidgets import QWidget

from src.main_application.iteration_progress_widget_layout import IterationProgressWidgetLayout


class IterationProgressWidget(QWidget):
    """
    Class is responsible for creating a widget that keeps the information about the visualization iteration progress bar.
    """
    def __init__(self):
        super().__init__()
        self._setup_widget()


    def _setup_widget(self):
        self.layout = IterationProgressWidgetLayout(self)