from PyQt5 import QtWidgets, uic
from settings import UI_PATH


class AdminUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{UI_PATH}/administradores.ui", self)
        self.show()
