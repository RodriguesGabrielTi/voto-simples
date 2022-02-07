import datetime

from PyQt5 import QtWidgets, uic

from settings import UI_PATH


class PublicarUi(QtWidgets.QDialog):
    def __init__(self, eleicao_view):
        super().__init__()
        self.eleicao_view = eleicao_view
        uic.loadUi(f"{UI_PATH}/publicar.ui", self)
        self.data_inicio = self.findChild(QtWidgets.QDateTimeEdit, 'data_inicio')
        self.data_fim = self.findChild(QtWidgets.QDateTimeEdit, 'data_fim')

        self.botao_confirmar = self.findChild(QtWidgets.QPushButton, 'pushButton_confirmar')
        self.botao_confirmar.clicked.connect(self.enviar)
        self.botao_cancelar = self.findChild(QtWidgets.QPushButton, 'pushButton_cancelar')
        self.botao_cancelar.clicked.connect(self.cancelar)

        self.showNormal()

    def enviar(self):
        try:
            dados = {
                "data_fim": self.data_fim.dateTime().toPyDateTime(),
                "data_inicio": datetime.datetime.today()
            }
            self.eleicao_view.enviar_publicacao(dados)
            self.close()
        except ValueError as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def cancelar(self):
        self.close()
