from PyQt5 import QtWidgets
import sys
from models.administrador import Admistrador
from views.login import LoginUi


class AutenticacaoController:

    def __init__(self, aplicacao_controller, sessao):
        self.__aplicacao_controller = aplicacao_controller
        self.__sessao = sessao

    def abrir(self):
        app = QtWidgets.QApplication(sys.argv)
        LoginUi()
        app.exec_()

    def autenticar(self, cpf, senha):
        administrador = self.__sessao.query(Admistrador).where(Admistrador.cpf == cpf, Admistrador.senha == senha)
        try:
            if len(administrador) == 0:
                raise ValueError("Usuário ou senha incorretos")
            else:
                self.__aplicacao_controller.usuario_atual = administrador[0]
        except ValueError as e:
            return e
