import sys

from PyQt5 import QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from main_application.main_application_window import MainApplicationWindow
from main_application.resources_container import ResourcesContainer


def redefine_exceptions():
    """
    Catches critical exceptions and displays them in message box.
    """
    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "An exception was raised",
                                       f"Exception info: {t}\n{val}\n{tb}")
        old_hook(t, val, tb)

    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions


class UCTVisualisationAppContext(ApplicationContext):
    """
    Class enables resources usage for UCT app.
    """
    def run(self):
        ResourcesContainer(self)
        window = MainApplicationWindow()
        window.show()
        return self.app.exec_()


if __name__ == '__main__':
    """
    Application entry point.
    """
    redefine_exceptions()
    context = UCTVisualisationAppContext()
    exit_code = context.run()
    sys.exit(exit_code)
