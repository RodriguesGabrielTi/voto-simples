from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from settings import UI_PATH
from views.erro import ErroUi


class AdminUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller):
        self.erro_dialog = None
        self.__controllers = aplicacao_controller
        self.__admin_controller = self.__controllers.administradores_controller()
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
        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.atualizar_button.setEnabled(False)

        self.table.clicked.connect(self.on_click)
        self.table.doubleClicked.connect(self.clean)
        self.cpf_selected = None
        self.listar_admins()
        self.showMaximized()

    def listar_admins(self):
        admins = self.__admin_controller.listar()
        for admin in admins:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(admin.nome))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(admin.cpf))
            self.table.setItem(position, 2, QtWidgets.QTableWidgetItem("ativo" if admin.ativo else "inativo"))

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())
        self.cpf_selected = index.sibling(index.row(), 1).data()
        self.carregar_fields()

    def carregar_fields(self):
        print(self.cpf_selected)
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
            self.validate_fields()
        except Exception as e:
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
            "ativo": self.ativo_checkbox.isChecked()
        }
        for campo in dados:
            if not dados.get(campo):
                self.mostrar_erro("Preencha todos os campos!")
                return

        self.__admin_controller.criar(dados)
        self.listar_admins()

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)
