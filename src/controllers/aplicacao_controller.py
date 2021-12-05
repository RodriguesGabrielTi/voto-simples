from controllers.administradores_controller import AdministradoresController
from controllers.eleicoes_controller import EleicoesController
from controllers.autenticacao_controller import AutenticacaoController


class AplicacaoController:
    def __init__(self, sessao):
        self.__session = sessao
        self.__eleicoes_controller = EleicoesController(self, sessao)
        self.__administradores_controller = AdministradoresController(self, sessao)
        self.__autenticacao_controller = AutenticacaoController(self, sessao)
        self.__usuario_atual = None
        self.__application_ui = None

    def abrir(self):
        if self.__usuario_atual is None:
            print("abrindo")
            self.__autenticacao_controller.abrir()
        else:
            pass
            # self.__application_ui.abrir()

    def administradores(self):
        self.__administradores_controller.abrir()

    def eleicoes(self):
        self.__eleicoes_controller.abrir()

    @property
    def usuario_atual(self):
        return self.__usuario_atual

    @usuario_atual.setter
    def usuario_atual(self, usuario_atual):
        self.__usuario_atual = usuario_atual
