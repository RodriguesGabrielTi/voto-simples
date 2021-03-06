import settings
from controllers.administradores_controller import AdministradoresController
from controllers.eleicoes_controller import EleicoesController
from controllers.autenticacao_controller import AutenticacaoController
from controllers.mesario_controller import MesarioController
from controllers.validar_votante_controller import ValidarVotanteController
from controllers.votantes_controller import VotantesController
from views.login import LoginUi


class AplicacaoController:
    def __init__(self, sessao):
        self.__sessao = sessao
        self.__eleicoes_controller = EleicoesController(self, sessao)
        self.__administradores_controller = AdministradoresController(self, sessao)
        self.__autenticacao_controller = AutenticacaoController(self, sessao)
        self.__mesario_controller = MesarioController(self, sessao)
        self.__votantes_controller = VotantesController(self, sessao)
        self.__usuario_atual = None
        self.__usuario_atual_tipo = None

    def iniciar(self):
        app = settings.APP
        window = LoginUi(self)
        app.exec_()

    def autenticacao_controller(self):
        return self.__autenticacao_controller

    def administradores_controller(self):
        return self.__administradores_controller

    def eleicoes_controller(self):
        return self.__eleicoes_controller

    def mesarios_controller(self):
        return self.__mesario_controller

    @property
    def votantes_controller(self):
        return self.__votantes_controller

    def validar_votante_controller(self, eleicao_id):
        return ValidarVotanteController(eleicao_id, self.__sessao, self)

    @property
    def usuario_atual(self):
        return self.__usuario_atual

    @usuario_atual.setter
    def usuario_atual(self, usuario_atual):
        self.__usuario_atual = usuario_atual
        self.__usuario_atual_tipo = "ADMIN"

    @property
    def sessao(self):
        return self.__sessao
