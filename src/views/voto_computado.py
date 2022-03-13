from PyQt5 import QtWidgets, uic, QtCore

from settings import UI_PATH


class VotoComputadoUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{UI_PATH}/voto_computado.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.showMaximized()