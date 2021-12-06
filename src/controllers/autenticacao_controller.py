from models.administrador import Administrador


class AutenticacaoController:

    def __init__(self, aplicacao_controller, sessao):
        self.__aplicacao_controller = aplicacao_controller
        self.__sessao = sessao
        self.__window = None

    def autenticar(self, cpf, senha):
        administrador = self.__sessao.query(Administrador).filter_by(cpf=cpf, senha=senha).first()
        if not administrador:
            raise ValueError("Usuário ou senha incorretos")
        else:
            print(administrador)
            self.__aplicacao_controller.usuario_atual = administrador
        return True
