from src.models.administrador import Admistrador


class AdministradoresController:
    def __init__(self, application_controller, sessao):
        self.__sessao = sessao
        self.__application_controller = application_controller
        self.__administradores_view = None

    def abrir(self):
        pass

    def index(self):
        administradores = self.__sessao.query(Admistrador).all()
        print(administradores)

    def show(self, administrador_id):
        administrador = self.__sessao.query(Admistrador).get(administrador_id)
        print(administrador)
        # mostrar na tela

    def create(self, params):
        administrador = Admistrador(nome=params["nome"], email=params["email"], cpf=params["cpf"],
                                    data_nascimento=params["data_nascimento"], endereco=params["endereco"],
                                    ativo=params["ativo"])
        self.__sessao.add(administrador)
        self.__sessao.commit()

    def update(self, params):
        administrador = self.__sessao.query(Admistrador).get(params["id"])
        administrador.nome = params["nome"]
        administrador.email = params["email"]
        administrador.cpf = params["cpf"]
        administrador.data_nascimento = params["data_nascimento"]
        administrador.endereco = params["endereco"]
        administrador.ativo = params["ativo"]
        self.__sessao.commit()

    def delete(self, administrador_id):
        administrador = self.__sessao.query(Admistrador).get(administrador_id)
        administrador.delete()
        self.__sessao.commit()
