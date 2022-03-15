from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from sqlalchemy.exc import IntegrityError

from settings import UI_PATH
from views.erro import ErroUi


class VotanteUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, main_window):
        self.erro_dialog = None
        self.main_window = None
        self.__controller = aplicacao_controller
        self.__votante_controller = self.__controller.votantes_controller
        self.__main_window = main_window
        super().__init__()

        uic.loadUi(f"{UI_PATH}/votantes.ui", self)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')
        self.data_nascimento_field = self.findChild(QtWidgets.QDateEdit, 'dateEdit_nascimento')
        self.cpf_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_cpf')
        self.categoria_field = self.findChild(QtWidgets.QComboBox, 'comboBox_categoria')
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
        self.listar_votantes()
        self.showMaximized()

        # genericos
        self.menu_exit = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_exit')
        self.menu_exit.clicked.connect(self.close)
        self.main_button = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_main')
        self.main_button.clicked.connect(self.abrir_main_window)

    def listar_votantes(self):
        votantes = self.__votante_controller.listar()
        self.table.setRowCount(0)
        for votante in votantes:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(votante.nome))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(votante.cpf))
            self.table.setItem(position, 2, QtWidgets.QTableWidgetItem(votante.categoria.nome))
            self.table.setItem(position, 3, QtWidgets.QTableWidgetItem("ativo" if votante.ativo else "inativo"))

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
        votante = self.__votante_controller.detalhar(self.cpf_selected)
        self.nome_field.setText(votante["nome"])
        self.data_nascimento_field.setDate(votante["data_nascimento"])
        self.cpf_field.setText(votante["cpf"])
        self.cpf_field.setEnabled(False)
        self.endereco.setText(votante["endereco"])
        self.ativo_checkbox.setChecked(votante["ativo"])

    def clean(self):
        self.nome_field.clear()
        self.data_nascimento_field.clear()
        self.cpf_field.clear()
        self.cpf_field.setEnabled(True)
        self.endereco.clear()
        self.ativo_checkbox.setChecked(True)
        self.table.clearSelection()

    def cadastrar(self):
        try:
            dados = self.validate_fields()
            self.__votante_controller.criar(dados)
            self.listar_votantes()
            self.clean()
        except IntegrityError:
            self.__controller.sessao.rollback()
            self.mostrar_erro("CPF ja cadastrado")
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def atualizar(self):
        try:
            dados = self.validate_fields()
            self.__votante_controller.atualizar(self.cpf_selected, dados)
            self.carregar_fields()
            self.listar_votantes()
        except IntegrityError:
            self.__controller.sessao.rollback()
            self.mostrar_erro("CPF ja cadastrado")
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            self.__votante_controller.excluir(self.cpf_selected)
            self.listar_votantes()
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
            "categoria": self.categoria_field.itemText(self.categoria_field.currentIndex()),
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

    def abrir_main_window(self):
        self.close()
        self.__main_window.show()

