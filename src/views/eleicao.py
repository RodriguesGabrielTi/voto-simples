from PyQt5 import QtWidgets, uic
from sqlalchemy import Enum
from settings import UI_PATH
from views.erro import ErroUi
from views.publicar import PublicarUi


class EleicaoUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller):
        self.erro_dialog = None
        self.publicar_dialog = None
        self.__controller = aplicacao_controller
        self.__eleicoes_controller = self.__controller.eleicoes_controller()
        super().__init__()

        uic.loadUi(f"{UI_PATH}/eleicoes.ui", self)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')
        self.descricao_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_descricao')
        self.estado_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_estado')
        self.estado_field.setEnabled(False)

        self.cadastrar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')
        self.cadastrar_button.clicked.connect(self.cadastrar)

        self.atualizar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_atualizar')
        self.atualizar_button.setEnabled(False)
        self.atualizar_button.clicked.connect(self.atualizar)

        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.excluir_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.excluir)

        self.publicar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_publicar')
        self.publicar_button.setEnabled(False)
        self.publicar_button.clicked.connect(self.publicar)

        self.relatorio_button = self.findChild(QtWidgets.QPushButton, 'pushButton_relatorio')
        self.relatorio_button.setEnabled(False)
        self.relatorio_button.clicked.connect(self.relatorio)

        self.categorias_button = self.findChild(QtWidgets.QPushButton, 'pushButton_categorias')
        self.categorias_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.categorias)

        self.questoes_button = self.findChild(QtWidgets.QPushButton, 'pushButton_questoes')
        self.questoes_button.setEnabled(False)
        self.questoes_button.clicked.connect(self.questoes)

        self.table.clicked.connect(self.on_click)
        self.id_selected = None
        self.listar_eleicoes()
        self.showMaximized()

    def listar_eleicoes(self):
        eleicoes = self.__eleicoes_controller.listar()
        self.table.setRowCount(0)
        for eleicao in eleicoes:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(str(eleicao.id)))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(eleicao.nome))
            self.table.setItem(position, 2, QtWidgets.QTableWidgetItem(
                eleicao.data_inicio.strftime("%d/%m/%Y, %H:%M") if eleicao.data_inicio else "nao publicada"))
            self.table.setItem(position, 3, QtWidgets.QTableWidgetItem(
                eleicao.data_fim.strftime("%d/%m/%Y, %H:%M") if eleicao.data_inicio else "nao publicada"))
            self.table.setItem(position, 4, QtWidgets.QTableWidgetItem(eleicao.estado))

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())
        if self.id_selected == index.sibling(index.row(), 0).data():
            self.clean()
            self.id_selected = None
        else:
            self.id_selected = index.sibling(index.row(), 0).data()
            self.carregar_fields()
        self.botoes()

    def carregar_fields(self):
        eleicao = self.__eleicoes_controller.detalhar(int(self.id_selected))
        self.nome_field.setText(eleicao["nome"])
        self.descricao_field.setText(eleicao["descricao"])
        self.estado_field.setText(eleicao["estado"])

    def clean(self):
        self.nome_field.clear()
        self.descricao_field.clear()
        self.estado_field.clear()
        self.table.clearSelection()

    def cadastrar(self):
        try:
            dados = self.validate_fields()
            self.__eleicoes_controller.criar(dados)
            self.listar_eleicoes()
            self.clean()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def atualizar(self):
        try:
            dados = self.validate_fields()
            self.__eleicoes_controller.atualizar(int(self.id_selected), dados)
            self.carregar_fields()
            self.listar_eleicoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            self.__eleicoes_controller.excluir(int(self.id_selected))
            self.listar_eleicoes()
            self.clean()
            self.id_selected = None
            self.botoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def publicar(self):
        self.publicar_dialog = PublicarUi(self)

    def enviar_publicacao(self, dados):
        try:
            self.__eleicoes_controller.publicar(int(self.id_selected), dados)
            self.carregar_fields()
            self.listar_eleicoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def relatorio(self):
        pass

    def categorias(self):
        pass

    def questoes(self):
        pass

    def validate_fields(self):
        dados = {
            "nome": self.nome_field.text(),
            "descricao": self.descricao_field.text()
        }
        for campo in dados:
            if not dados.get(campo):
                raise ValueError("Preencha todos os campos!")
        return dados

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

    def botoes(self):
        if self.id_selected:
            self.atualizar_button.setEnabled(True)
            self.cadastrar_button.setEnabled(False)
            self.excluir_button.setEnabled(True)
            self.publicar_button.setEnabled(True)
        else:
            self.atualizar_button.setEnabled(False)
            self.cadastrar_button.setEnabled(True)
            self.excluir_button.setEnabled(False)
            self.publicar_button.setEnabled(False)

