from PyQt5.QtWidgets import QWidget

from src.main_application.iteration_progress_widget_layout import IterationProgressWidgetLayout


class IterationProgressWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_widget()


    def _setup_widget(self):
        self.layout = IterationProgressWidgetLayout(self)