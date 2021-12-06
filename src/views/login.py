from PyQt5 import QtWidgets, uic

from settings import UI_PATH
from views.menu import MenuUi


class LoginUi(QtWidgets.QDialog):
    def __init__(self, aplicacao_controller):
        self.__controller = aplicacao_controller
        self.menu_window = None
        super().__init__()
        uic.loadUi(f"{UI_PATH}/login.ui", self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton_entrar')

        self.cpf_input = self.findChild(QtWidgets.QLineEdit, 'lineEdit_cpf')
        self.senha_input = self.findChild(QtWidgets.QLineEdit, 'lineEdit_senha')
        self.button.clicked.connect(self.login)

        self.showMaximized()

    def login(self):
        cpf = self.cpf_input.text()
        senha = self.senha_input.text()
        if not cpf or not senha:
            print("digite os campos")
            return
        try:
            self.__controller.autenticacao_controller().autenticar(cpf, senha)
            self.close()
            self.open_menu()
        except ValueError:
            print("senha ou cpf invalido")
            return

    def open_menu(self):
        if self.menu_window is None:
            self.menu_window = MenuUi(self.__controller)
            self.menu_window.show()
