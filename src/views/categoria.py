from PyQt5 import QtWidgets, uic

from settings import UI_PATH


class CategoriaUi(QtWidgets.QDialog):
    def __init__(self, eleicao_view, categorias_string):
        super().__init__()
        self.eleicao_view = eleicao_view
        uic.loadUi(f"{UI_PATH}/categorias_eleicao.ui", self)
        self.categorias_list = self.findChild(QtWidgets.QListWidget, 'lista_categorias')
        self.categorias_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_categorias')
        self.categorias_field.setText(categorias_string)

        self.botao_confirmar = self.findChild(QtWidgets.QPushButton, 'pushButton_confirmar')
        self.botao_confirmar.clicked.connect(self.enviar)
        self.botao_cancelar = self.findChild(QtWidgets.QPushButton, 'pushButton_cancelar')
        self.botao_cancelar.clicked.connect(self.cancelar)

        self.showNormal()

    def enviar(self):
        try:
            dados = self.categorias_list.selectedItems()
            self.eleicao_view.enviar_categorias(dados)
            self.close()
        except ValueError as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def cancelar(self):
        self.close()
