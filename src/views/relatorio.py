import os

from PyQt5 import QtWidgets, uic, QtGui, QtCore

from settings import UI_PATH
from views.erro import ErroUi


class RelatorioUi(QtWidgets.QDialog):
    def __init__(self, eleicao_id, eleicao_controler):
        super().__init__()
        self.eleicao_id = eleicao_id
        self.eleicao_controler = eleicao_controler
        self.caminho_do_arquivo = None
        uic.loadUi(f"{UI_PATH}/relatorio.ui", self)
        self.botao_acessar = self.findChild(QtWidgets.QPushButton, 'pushButton_acessar')
        self.botao_acessar.clicked.connect(self.acessar)
        self.label = self.findChild(QtWidgets.QLabel, 'lebel')

        self.showNormal()
        self.gerar_relatorio()

    def gerar_relatorio(self):
        try:
            self.caminho_do_arquivo = self.eleicao_controler.gerar_relatorio(self.eleicao_id)
            self.label.setText("Relatório Gerado!")
            self.botao_acessar.setEnabled(True)
        except ValueError as e:
            self.mostrar_erro(str(e))

    def acessar(self):
        caminho = os.path.realpath(self.caminho_do_arquivo)
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(caminho))
        self.close()

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)
