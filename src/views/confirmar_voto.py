from PyQt5 import QtWidgets, uic, QtCore
from settings import UI_PATH
from views.erro import ErroUi


class ConfirmarVotoUi(QtWidgets.QMainWindow):
    def __init__(self, votacao, escolhas):
        self.erro_dialog = None
        self.votacao = votacao
        self.escolhas = escolhas
        super().__init__()

        uic.loadUi(f"{UI_PATH}/confirmar_voto.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')

        self.confirmar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_confirmar')
        self.confirmar_button.clicked.connect(self.confirmar)

        self.voltar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_voltar')
        self.voltar_button.clicked.connect(self.close)

        self.listar_escolhas()
        self.showMaximized()

    def listar_escolhas(self):
        self.table.setRowCount(0)
        for escolha in list(self.escolhas.values()):
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(escolha["nome"]))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(
                self.candidatos_escolhidos_para_string(escolha["candidatos"])))

    def candidatos_escolhidos_para_string(self, candidatos):
        candidatos_string = ""
        for candidato in candidatos:
            candidatos_string += candidato.nome + ", "
        return candidatos_string[:-2]


    def confirmar(self):
        self.votacao.confirmar(self.escolhas)

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

