from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QProgressBar

from src.main_application.GUI_utils import center_window_on_screen, get_non_resizable_label
from src.main_application.sequence_utils import TreesRetrieverWorker
from src.utils.custom_event import CustomEvent


class SequenceLoadingWindow(QMainWindow):
    def __init__(self, parent, paths):
        super(SequenceLoadingWindow, self).__init__(parent)
        self.paths = paths
        self._setup_window()
        self._setup_event()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        center_window_on_screen(self)
        self.thread.start()

    def _setup_event(self):
        self.finished_event = CustomEvent()
        self.thread = QThread()
        self.worker = TreesRetrieverWorker(self.paths)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.do_work)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.tree_retrieved_signal.connect(self.handle_progress_made)

    def handle_progress_made(self, value):
        self.progress_bar.setValue(value * 100)
        if value == 1:
            self.finished_event.fire(self, earg=self.worker.trees_info)

    def _setup_window(self):
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        self.progress_bar = QProgressBar()
        main_layout.addWidget(get_non_resizable_label("Loading trees..."), 0, 0)
        main_layout.addWidget(self.progress_bar, 1, 0)
        self.setCentralWidget(main_widget)
