from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from settings import UI_PATH
from views.erro import ErroUi


class AdminUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller):
        self.erro_dialog = None
        self.__controller = aplicacao_controller
        self.__admin_controller = self.__controller.administradores_controller()
        super().__init__()

        uic.loadUi(f"{UI_PATH}/administradores.ui", self)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')
        self.data_nascimento_field = self.findChild(QtWidgets.QDateEdit, 'dateEdit_nascimento')
        self.cpf_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_cpf')
        self.senha_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_senha')
        self.endereco = self.findChild(QtWidgets.QLineEdit, 'lineEdit_endereco')
        self.ativo_checkbox = self.findChild(QtWidgets.QCheckBox, 'checkBox_ativo')

        self.cpf_field.textChanged.connect(self.validate_cpf)
        self.cpf_field.setMaxLength(11)

        self.cadastrar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')
        self.cadastrar_button.clicked.connect(self.cadastrar)
        self.atualizar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_atualizar')
        self.atualizar_button.setEnabled(False)
        self.atualizar_button.clicked.connect(self.atualizar)
        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.excluir_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.excluir)

        self.table.clicked.connect(self.on_click)
        self.cpf_selected = None
        self.listar_admins()
        self.showMaximized()

    def listar_admins(self):
        admins = self.__admin_controller.listar()
        self.table.setRowCount(0)
        for admin in admins:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(admin.nome))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(admin.cpf))
            self.table.setItem(position, 2, QtWidgets.QTableWidgetItem("ativo" if admin.ativo else "inativo"))

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())
        if self.cpf_selected == index.sibling(index.row(), 1).data():
            self.clean()
            self.cpf_selected = None
        else:
            self.cpf_selected = index.sibling(index.row(), 1).data()
            self.carregar_fields()
        self.botoes()

    def carregar_fields(self):
        admin = self.__admin_controller.detalhar(self.cpf_selected)
        self.nome_field.setText(admin["nome"])
        self.data_nascimento_field.setDate(admin["data_nascimento"])
        self.cpf_field.setText(admin["cpf"])
        self.cpf_field.setEnabled(False)
        self.senha_field.setText(admin["senha"])
        self.endereco.setText(admin["endereco"])
        self.ativo_checkbox.setChecked(admin["ativo"])

    def clean(self):
        self.nome_field.clear()
        self.data_nascimento_field.clear()
        self.cpf_field.clear()
        self.cpf_field.setEnabled(True)
        self.senha_field.clear()
        self.endereco.clear()
        self.ativo_checkbox.setChecked(True)
        self.table.clearSelection()

    def cadastrar(self):
        try:
            dados = self.validate_fields()
            self.__admin_controller.criar(dados)
            self.listar_admins()
            self.clean()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def atualizar(self):
        try:
            dados = self.validate_fields()
            self.__admin_controller.atualizar(self.cpf_selected, dados)
            self.carregar_fields()
            self.listar_admins()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            if self.cpf_selected == self.__controller.usuario_atual.cpf:
                raise ValueError("Você não pode se excluir")
            self.__admin_controller.excluir(self.cpf_selected)
            self.listar_admins()
            self.clean()
            self.cpf_selected = None
            self.botoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def validate_cpf(self):
        reg_ex = QRegExp("^[0-9]+$")
        cpf_validator = QRegExpValidator(reg_ex, self.cpf_field)
        self.cpf_field.setValidator(cpf_validator)

    def validate_fields(self):
        dados = {
            "nome": self.nome_field.text(),
            "cpf": self.cpf_field.text(),
            "data_nascimento": self.data_nascimento_field.date().toPyDate(),
            "endereco": self.endereco.text(),
            "senha": self.senha_field.text(),
        }
        for campo in dados:
            if not dados.get(campo):
                raise ValueError("Preencha todos os campos!")
        dados["ativo"] = self.ativo_checkbox.isChecked()
        return dados

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

    def botoes(self):
        if self.cpf_selected:
            self.atualizar_button.setEnabled(True)
            self.cadastrar_button.setEnabled(False)
            self.excluir_button.setEnabled(True)
        else:
            self.atualizar_button.setEnabled(False)
            self.cadastrar_button.setEnabled(True)
            self.excluir_button.setEnabled(False)
