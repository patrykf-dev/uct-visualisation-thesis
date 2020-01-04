import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QSizePolicy, QPushButton, QLineEdit, QRadioButton, QCheckBox, QMessageBox

DEFAULT_FONT = QtGui.QFont("Helvetica", 10)
DEFAULT_FONT_BOLD = QtGui.QFont("Helvetica", 10, QtGui.QFont.Bold)
LARGE_FONT_BOLD = QtGui.QFont("Helvetica", 20, QtGui.QFont.Bold)
DEFAULT_FONT_ITALIC = QtGui.QFont("Helvetica", 10, -1, True)

PYQT_KEY_CODE_LEFT = 16777234
PYQT_KEY_CODE_RIGHT = 16777236

TREES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "trees")


def amend_window_position_on_screen(window, top_padding=40):
    """
    Function is responsible for centering X of the given window on the screen.
    Y position is default 40, can be changed with the parameter 'top_padding'
    :param window: window we are going to center
    :param top_padding: number of pixels the window will be under the upper bound of the screen
    """
    bounds = window.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    center_point.setY(int(bounds.height() / 2) + top_padding)
    bounds.moveCenter(center_point)
    window.move(bounds.topLeft())


def get_box_background_stylesheet(color=(160, 200, 150)):
    """
    :param color: tuple of RGB values
    :return: string with css-like settings
    """
    return "QWidget#box{background-color: rgb" + str(color) + "; margin:2px; border-radius: 10px}"


def get_non_resizable_label(caption=""):
    """
    Generates label with fixed, non-resizable policy with given caption.
    """
    rc = QLabel(caption)
    rc.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    rc.setFont(DEFAULT_FONT)
    return rc


def get_button(caption="", padding_width=50, padding_height=0):
    """
    Returns PyQt button with given parameters.
    :param caption: text on button
    :param padding_width:
    :param padding_height:
    :return: customized button
    """
    rc = QPushButton(caption)
    rc.setFont(DEFAULT_FONT)
    rc.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    rc.setFixedWidth(rc.sizeHint().width() + padding_width)
    rc.setFixedHeight(rc.sizeHint().height() + padding_height)
    return rc


def get_resizable_button(caption="", padding_width=50, padding_height=0):
    """
    Returns PyQt resizable button with given parameters. It means it fills its parent-layout entirely.
    :param caption: text on button
    :param padding_width:
    :param padding_height:
    :return: customized button
    """
    rc = QPushButton(caption)
    rc.setFont(DEFAULT_FONT)
    rc.setMinimumWidth(rc.sizeHint().width() + padding_width)
    rc.setMinimumHeight(rc.sizeHint().height() + padding_height)
    return rc


def get_checkbox(caption=""):
    """
    Returns default PyQt checkbox.
    """
    rc = QCheckBox(caption)
    rc.setFont(DEFAULT_FONT)
    return rc


def get_radiobutton(caption=""):
    """
    Returns default PyQt radiobutton.
    """
    rc = QRadioButton(caption)
    rc.setFont(DEFAULT_FONT)
    return rc


def get_line_edit(width=0):
    """
    Returns default PyQt textfield with a given width.
    """
    rc = QLineEdit()
    rc.setFont(DEFAULT_FONT)
    if width != 0:
        rc.setFixedWidth(width)
    return rc


def get_hint_line_edit(text=""):
    """
    Returns default PyQt label with italic.
    """
    rc = QLineEdit(text)
    rc.setFont(DEFAULT_FONT_ITALIC)
    return rc


def gray_out_radiobutton_text(button: QRadioButton, disable):
    """
    Function disables/enables given radiobutton.
    """
    if disable:
        button.setStyleSheet("color: gray")
    else:
        button.setStyleSheet("color: black")


def show_eror_dialog(message):
    """
    Function pops up a critical error message box with given text.
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def show_dialog(message):
    """
    Function pops up a message box with given text.
    :returns QMessageBox.Ok or QMessageBox.Cancel
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(message)
    msg.setWindowTitle("Confirm")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    return msg.exec_()
