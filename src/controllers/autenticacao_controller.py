from models.administrador import Administrador
from models.mesario import Mesario


class AutenticacaoController:

    def __init__(self, aplicacao_controller, sessao):
        self.__aplicacao_controller = aplicacao_controller
        self.__sessao = sessao
        self.__window = None

    def autenticar(self, cpf, senha):
        administrador = self.__sessao.query(Administrador).filter_by(cpf=cpf, senha=senha).first()
        mesario = self.__sessao.query(Mesario).filter_by(cpf=cpf, senha=senha).first()
        if not administrador and not mesario:
            raise ValueError("Usuário ou senha incorretos")

        if administrador:
            self.__aplicacao_controller.usuario_atual = administrador
        elif mesario:
            self.__aplicacao_controller.usuario_atual = mesario
        return True
