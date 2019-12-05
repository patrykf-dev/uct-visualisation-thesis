from PyQt5.QtWidgets import QGridLayout, QProgressBar, QWidget, QSizePolicy

from src.main_application.GUI_utils import get_line_edit, get_non_resizable_label


class IterationProgressWidgetLayout:
    def __init__(self, main_widget):
        self.progress_bar = QProgressBar()
        self.show_auto_button = get_non_resizable_label("Time between frames")
        self.time_interval_edit = get_line_edit(width=60)

        self._create_layout(main_widget)

    def _create_layout(self, main_widget: QWidget):
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        main_layout.addWidget(self.progress_bar, 0, 0, 1, 2)
        main_layout.addWidget(self.show_auto_button, 1, 0)
        main_layout.addWidget(self.time_interval_edit, 1, 1)

        self.show_auto_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.time_interval_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
