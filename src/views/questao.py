from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from views.erro import ErroUi
from PyQt5 import QtCore

class QuestaoUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, questoes_controller):
        self.erro_dialog = None
        self.publicar_dialog = None
        self.__controller = aplicacao_controller
        self.__questoes_controller = questoes_controller
        super().__init__()

        uic.loadUi(f"{UI_PATH}/questoes.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')
        self.descricao_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_descricao')
        self.escolhas_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_escolhas')

        self.cadastrar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')
        self.cadastrar_button.clicked.connect(self.cadastrar)

        self.atualizar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_atualizar')
        self.atualizar_button.setEnabled(False)
        self.atualizar_button.clicked.connect(self.atualizar)

        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.excluir_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.excluir)

        self.candidatos_button = self.findChild(QtWidgets.QPushButton, 'pushButton_candidatos')
        self.candidatos_button.setEnabled(False)
        self.candidatos_button.clicked.connect(self.candidatos)

        self.table.clicked.connect(self.on_click)
        self.id_selected = None
        self.listar_questoes()
        self.showMaximized()

    def listar_questoes(self):
        questoes = self.__questoes_controller.listar()
        self.table.setRowCount(0)
        for questao in questoes:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(str(questao.id)))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(questao.nome))
            self.table.setItem(position, 2, QtWidgets.QTableWidgetItem(str(questao.numero_escolhas)))

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
        questao = self.__questoes_controller.detalhar(int(self.id_selected))
        self.nome_field.setText(questao["nome"])
        self.descricao_field.setText(questao["descricao"])
        self.escolhas_field.setText(str(questao["numero_escolhas"]))

    def clean(self):
        self.nome_field.clear()
        self.descricao_field.clear()
        self.escolhas_field.clear()
        self.table.clearSelection()

    def cadastrar(self):
        try:
            dados = self.validate_fields()
            self.__questoes_controller.criar(dados)
            self.listar_questoes()
            self.clean()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def atualizar(self):
        try:
            dados = self.validate_fields()
            self.__questoes_controller.atualizar(int(self.id_selected), dados)
            self.carregar_fields()
            self.listar_questoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            self.__questoes_controller.excluir(int(self.id_selected))
            self.listar_questoes()
            self.clean()
            self.id_selected = None
            self.botoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def candidatos(self):
        self.__questoes_controller.candidatos(int(self.id_selected))


    def validate_fields(self):
        dados = {
            "nome": self.nome_field.text(),
            "descricao": self.descricao_field.text(),
            "numero_escolhas": int(self.escolhas_field.text())
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
            self.candidatos_button.setEnabled(True)
        else:
            self.atualizar_button.setEnabled(False)
            self.cadastrar_button.setEnabled(True)
            self.excluir_button.setEnabled(False)
            self.candidatos_button.setEnabled(False)