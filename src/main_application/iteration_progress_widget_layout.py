from PyQt5.QtWidgets import QGridLayout, QProgressBar, QWidget


class IterationProgressWidgetLayout:
    """
    Class is responsible for the layout of visualization iteration progress bar.
    """

    def __init__(self, main_widget):
        self.progress_bar = QProgressBar()
        self._create_layout(main_widget)

    def _create_layout(self, main_widget: QWidget):
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        main_layout.addWidget(self.progress_bar, 0, 0)
