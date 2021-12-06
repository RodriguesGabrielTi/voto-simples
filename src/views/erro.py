from PyQt5 import QtWidgets, uic

from settings import UI_PATH


class ErroUi(QtWidgets.QDialog):
    def __init__(self, mensagem: str):
        super().__init__()
        uic.loadUi(f"{UI_PATH}/erro_dialog.ui", self)
        self.erro_info = self.findChild(QtWidgets.QLabel, 'erro_info')
        self.erro_info.setText(mensagem)
        self.showNormal()

