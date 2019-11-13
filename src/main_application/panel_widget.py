from PyQt5.QtWidgets import QFrame


class PanelWidget(QFrame):
    def __init__(self, *args):
        super(PanelWidget, self).__init__(*args)
        self.setStyleSheet("background-color: rgb(160, 160, 160); margin:2px; border:2px solid rgb(0, 0, 0);")
        self.setFixedSize(400, 400)

    def change_background_color(self, color):
        self.setStyleSheet(
            f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); margin:2px; border:2px solid rgb(0, 0, 0);")