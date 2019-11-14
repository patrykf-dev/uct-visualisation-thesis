import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QSizePolicy, QPushButton, QLineEdit, QRadioButton


DEFAULT_FONT = QtGui.QFont("Helvetica", 10)
DEFAULT_FONT_BOLD = QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold)
DEFAULT_FONT_ITALIC = QtGui.QFont("Helvetica", 10, -1, True)

PYQT_KEY_CODE_LEFT = 16777234
PYQT_KEY_CODE_UP = 16777235
PYQT_KEY_CODE_RIGHT = 16777236
PYQT_KEY_CODE_DOWN = 16777237

TREES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "trees")

def get_non_resizable_label(caption=""):
    rc = QLabel(caption)
    rc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    rc.setFont(DEFAULT_FONT)
    return rc


def get_button(caption=""):
    rc = QPushButton(caption)
    rc.setFont(DEFAULT_FONT)
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
