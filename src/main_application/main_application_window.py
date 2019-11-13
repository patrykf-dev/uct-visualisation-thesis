import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QRadioButton, QSizePolicy, QWidget, QLineEdit, QPushButton


class MainApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        main_layout.addWidget(self._get_first_row(), 0, 0)
        main_layout.addWidget(self._get_second_row(), 1, 0)

    def _get_second_row(self):
        rc = QWidget()
        main_layout = QGridLayout()
        rc.setObjectName("box")
        rc.setStyleSheet(
            "QWidget#box{background-color: rgb(160, 160, 160); margin:2px; border:2px solid rgb(0, 0, 0);}")
        rc.setLayout(main_layout)
        main_layout.addWidget(QLineEdit("Path..."), 0, 0)
        main_layout.addWidget(QPushButton("Select"), 0, 1)
        main_layout.addWidget(QPushButton("Draw tree (OpenGL)"), 1, 0, 1, 2)
        main_layout.addWidget(QPushButton("Draw tree (matplotlib)"), 2, 0, 1, 2)
        return rc

    def _get_bottom_widget(self):
        return QWidget()

    def _get_first_row(self):
        rc = QWidget()
        main_layout = QGridLayout()
        rc.setObjectName("box")
        rc.setStyleSheet(
            "QWidget#box{background-color: rgb(160, 160, 160); margin:2px; border:2px solid rgb(0, 0, 0);}")
        rc.setLayout(main_layout)

        self._add_left_panel(main_layout)
        self._add_right_panel(main_layout)
        self._add_uct_panel(main_layout)
        main_layout.addWidget(QPushButton("Play"), 2, 0, 1, 2)
        return rc

    def get_non_resizable_label(self, caption):
        rc = QLabel(caption)
        rc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return rc

    def _add_left_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(self.get_non_resizable_label("Game"), 0, 0)
        layout.addWidget(QRadioButton("Chess"), 1, 0)
        layout.addWidget(QRadioButton("Mancala"), 2, 0)
        main_layout.addWidget(new_widget, 0, 0)

    def _add_right_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(self.get_non_resizable_label("Mode"), 0, 0)
        layout.addWidget(QRadioButton("Player vs player"), 1, 0)
        layout.addWidget(QRadioButton("Player vs PC"), 2, 0)
        layout.addWidget(QRadioButton("PC vs PC"), 3, 0)
        main_layout.addWidget(new_widget, 0, 1)

    def _add_uct_panel(self, main_layout):
        new_widget = QWidget()
        layout = QGridLayout()
        new_widget.setLayout(layout)
        layout.addWidget(self.get_non_resizable_label("UCT parameters"), 0, 0)
        layout.addWidget(self.get_non_resizable_label("Iterations before move"), 1, 0)
        layout.addWidget(self.get_non_resizable_label("Max time for move"), 2, 0)
        layout.addWidget(QLineEdit(), 1, 1)
        layout.addWidget(QLineEdit(), 2, 1)
        main_layout.addWidget(new_widget, 1, 0, 1, 2)


def launch_application():
    try:
        window = MainApplicationWindow()
        window.show()
    except:
        print("ERRRRO")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # error_trigger
    myapp = MainApplicationWindow()
    myapp.show()
    sys.exit(app.exec_())
