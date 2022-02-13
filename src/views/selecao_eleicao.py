from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from views.erro import ErroUi


class SelecaoEleicaoUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller):
        self.questoes_window = None
        self.erro_dialog = None
        self.publicar_dialog = None
        self.__controller = aplicacao_controller
        self.__eleicoes_controller = self.__controller.eleicoes_controller()
        super().__init__()

        uic.loadUi(f"{UI_PATH}/selecionar_eleicao.ui", self)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')

        self.selecionar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')

        self.table.clicked.connect(self.on_click)
        self.id_selected = None
        self.listar_eleicoes()
        self.showMaximized()

    def listar_eleicoes(self):
        eleicoes = self.__eleicoes_controller.listar_mesario_eleicoes(self.__controller.usuario_atual)
        self.table.setRowCount(0)
        for eleicao in eleicoes:
            print(eleicao)
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(str(eleicao.id)))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(eleicao.nome))
            self.table.setItem(
                position,
                2,
                QtWidgets.QTableWidgetItem(
                    eleicao.data_inicio.strftime("%d/%m/%Y, %H:%M") if eleicao.data_inicio else "não publicada"
                )
            )
            self.table.setItem(
                position,
                3,
                QtWidgets.QTableWidgetItem(
                    eleicao.data_fim.strftime("%d/%m/%Y, %H:%M") if eleicao.data_fim else "não finalizada"
                )
            )
            self.table.setItem(position, 4, QtWidgets.QTableWidgetItem(eleicao.estado))

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())
        self.id_selected = index.sibling(index.row(), 0).data()

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)


