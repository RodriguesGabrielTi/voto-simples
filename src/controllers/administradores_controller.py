from src.models.administrador import Admistrador


class AdministradoresController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__administradores_ui = None

    def abrir(self):
        # self,__administradores_ui.show()
        pass

    def listar(self):
        administradores = self.__sessao.query(Admistrador).all()
        return administradores

    def detalhar(self, administrador_id):
        administrador = self.__sessao.query(Admistrador).get(administrador_id)
        return administrador

    def criar(self, parametros):
        administrador = Admistrador(nome=parametros["nome"], email=parametros["email"], cpf=parametros["cpf"],
                                    data_nascimento=parametros["data_nascimento"], endereco=parametros["endereco"],
                                    ativo=parametros["ativo"])
        self.__sessao.add(administrador)
        self.__sessao.commit()

    def atualizar(self, administrador_id, parametros):
        administrador = self.__sessao.query(Admistrador).get(administrador_id)
        administrador.nome = parametros["nome"]
        administrador.email = parametros["email"]
        administrador.cpf = parametros["cpf"]
        administrador.data_nascimento = parametros["data_nascimento"]
        administrador.endereco = parametros["endereco"]
        administrador.ativo = parametros["ativo"]
        self.__sessao.commit()

    def excluir(self, administrador_id):
        administrador = self.__sessao.query(Admistrador).get(administrador_id)
        administrador.delete()
        self.__sessao.commit()
