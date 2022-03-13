from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from views.erro import ErroUi
from PyQt5 import QtCore
from datetime import date

from views.votacao import VotacaoUi


class ValidarVotanteUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, eleicao_id):
        self.erro_dialog = None
        self.__controller = aplicacao_controller
        self.__validar_controller = aplicacao_controller.validar_votante_controller(eleicao_id)
        self.__eleicao_id = eleicao_id
        super().__init__()

        uic.loadUi(f"{UI_PATH}/validar_votante.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.buscar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_buscar')
        self.buscar_button.clicked.connect(self.buscar)

        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')
        self.nascimento_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_data_nascimento')

        self.autenticar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_autenticar')
        self.autenticar_button.clicked.connect(self.autenticar)
        self.autenticar_button.setEnabled(False)

        self.cpf_de_busca = self.findChild(QtWidgets.QLineEdit, 'lineEdit_cpf')
        self.cpf_de_busca.textChanged.connect(self.validate_cpf)
        self.cpf_de_busca.setMaxLength(11)

        self.cpf_selected = None

        self.menu_exit = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_exit')
        self.menu_exit.clicked.connect(self.close)
        self.showMaximized()

    def validate_cpf(self):
        reg_ex = QRegExp("^[0-9]+$")
        cpf_validator = QRegExpValidator(reg_ex, self.cpf_de_busca)
        self.cpf_de_busca.setValidator(cpf_validator)

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

    def buscar(self):
        cpf = self.cpf_de_busca.text()
        if not cpf:
            self.mostrar_erro("Insira um CPF")
            self.clear()
            return
        try:
            votante = self.__controller.votantes_controller.detalhar(cpf)
            self.nome_field.setText(votante["nome"])
            self.nascimento_field.setText(date.strftime(votante["data_nascimento"], "%d/%m/%y"))
            self.cpf_selected = cpf
            self.autenticar_button.setEnabled(True)
        except ValueError as e:
            self.clear()
            self.mostrar_erro(str(e))

    def autenticar(self):
        try:
            if self.__validar_controller.autenticar(self.cpf_selected):
                self.votacao_window = VotacaoUi(self.__controller, self.__validar_controller.votacao(self.cpf_selected))
        except ValueError as e:
            self.clear()
            self.mostrar_erro(str(e))

    def clear(self):
        self.nome_field.clear()
        self.nascimento_field.clear()
        self.cpf_de_busca.clear()
        self.cpf_selected = None
        self.autenticar_button.setEnabled(False)
