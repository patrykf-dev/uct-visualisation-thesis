import sys

from PyQt5 import QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from main_application.main_application_window import MainApplicationWindow


def redefine_exceptions():
    """
    Catches critical exceptions and displays them in message box.
    """

    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "An exception was raised",
                                       f"Exception info: [{t}] [{val}] [{tb}]")
        old_hook(t, val, tb)

    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions


APP_CONTEXT = ApplicationContext()

if __name__ == '__main__':
    """
    Application entry point
    """
    redefine_exceptions()
    window = MainApplicationWindow()
    window.show()
    exit_code = APP_CONTEXT.app.exec_()
    sys.exit(exit_code)
