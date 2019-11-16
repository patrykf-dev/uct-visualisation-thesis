import sys

from PyQt5 import QtWidgets

from src.main_application.mc_tree_window import MonteCarloTreeWindow


def redefine_exceptions():
    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "An exception was raised",
                                       f"Exception info: [{t}] [{val}] [{tb}]")
        old_hook(t, val, tb)

    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions


if __name__ == '__main__':
    redefine_exceptions()
    app = QtWidgets.QApplication(sys.argv)
    window = MonteCarloTreeWindow()
    window.show()
    sys.exit(app.exec_())
