import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QSizePolicy, QPushButton, QLineEdit, QRadioButton

DEFAULT_FONT = QtGui.QFont("Helvetica", 10)
DEFAULT_FONT_BOLD = QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold)
DEFAULT_FONT_ITALIC = QtGui.QFont("Helvetica", 10, -1, True)

PYQT_KEY_CODE_LEFT = 16777234
PYQT_KEY_CODE_UP = 16777235
PYQT_KEY_CODE_RIGHT = 16777236
PYQT_KEY_CODE_DOWN = 16777237

TREES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "trees")


def center_window_on_screen(window):
    bounds = window.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    center_point.setY(int(bounds.height() / 2))  # Just for debugging purposes
    bounds.moveCenter(center_point)
    window.move(bounds.topLeft())


def get_non_resizable_label(caption=""):
    rc = QLabel(caption)
    rc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    rc.setFont(DEFAULT_FONT)
    return rc


def get_button(caption="", padding_width=50, padding_height=0):
    rc = QPushButton(caption)
    rc.setFont(DEFAULT_FONT)
    rc.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    rc.setFixedWidth(rc.sizeHint().width() + padding_width)
    rc.setFixedHeight(rc.sizeHint().height() + padding_height)
    return rc


def get_radiobutton(caption=""):
    rc = QRadioButton(caption)
    rc.setFont(DEFAULT_FONT)
    return rc


def get_line_edit():
    rc = QLineEdit()
    rc.setFont(DEFAULT_FONT)
    return rc


def get_hint_line_edit(text=""):
    rc = QLineEdit(text)
    rc.setFont(DEFAULT_FONT_ITALIC)
    return rc
