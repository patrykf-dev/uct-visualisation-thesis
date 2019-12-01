from PyQt5.QtWidgets import QGridLayout, QProgressBar, QWidget, QSizePolicy

from src.main_application.GUI_utils import get_radiobutton, get_line_edit, get_button, gray_out_radiobutton_text


class IterationProgressWidgetLayout:
    def __init__(self, main_widget):
        self.progress_bar = QProgressBar()
        self.show_auto_button = get_radiobutton("View iterations automatically")
        self.time_interval_edit = get_line_edit(width=75)
        self.show_manual_button = get_radiobutton("View iterations manually")
        self.show_next_button = get_button("Show next iteration")

        self._create_layout(main_widget)
        self._set_handlers()
        self._apply_defaults()

    def _create_layout(self, main_widget: QWidget):
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        main_layout.addWidget(self.progress_bar, 0, 0, 1, 2)
        main_layout.addWidget(self.show_auto_button, 1, 0)
        main_layout.addWidget(self.time_interval_edit, 1, 1)
        main_layout.addWidget(self.show_manual_button, 2, 0)
        main_layout.addWidget(self.show_next_button, 2, 1)

        self.show_auto_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.time_interval_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.show_manual_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.show_next_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def _set_handlers(self):
        self.show_manual_button.clicked.connect(self._handle_show_click)
        self.show_auto_button.clicked.connect(self._handle_show_click)

    def _handle_show_click(self):
        if self.show_manual_button.isChecked():
            self.show_next_button.setEnabled(True)
            self.time_interval_edit.setEnabled(False)
            gray_out_radiobutton_text(self.show_manual_button, False)
            gray_out_radiobutton_text(self.show_auto_button, True)
        else:
            self.show_next_button.setEnabled(False)
            self.time_interval_edit.setEnabled(True)
            gray_out_radiobutton_text(self.show_manual_button, True)
            gray_out_radiobutton_text(self.show_auto_button, False)

    def _apply_defaults(self):
        self.show_auto_button.click()
        self.time_interval_edit.setText("500")
