from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys

from main_application.main_application_window import MainApplicationWindow

APP_CONTEXT = ApplicationContext()

if __name__ == '__main__':
    window = MainApplicationWindow()
    window.resize(250, 150)
    window.show()
    exit_code = APP_CONTEXT.app.exec_()
    sys.exit(exit_code)

# def launch_application():
#     """
#     Main program function.
#     Shows menu window.
#     """
#     redefine_exceptions()
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainApplicationWindow()
#     window.show()
#     sys.exit(app.exec_())
#
#
# def redefine_exceptions():
#     """
#     Catches critical exceptions and displays them in message box.
#     """
#
#     def catch_exceptions(t, val, tb):
#         QtWidgets.QMessageBox.critical(None,
#                                        "An exception was raised",
#                                        f"Exception info: [{t}] [{val}] [{tb}]")
#         old_hook(t, val, tb)
#
#     old_hook = sys.excepthook
#     sys.excepthook = catch_exceptions
#
#
# if __name__ == '__main__':
#     launch_application()