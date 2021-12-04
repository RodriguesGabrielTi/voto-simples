from src.models.administrador import Admistrador


class AdministradoresController:
    def __init__(self, application_controller):
        self.__application_controller = application_controller
        self.__administradores_view = None

    def abrir(self):
        pass

    def index(self):
        administradores = Admistrador.query.all()

    def show(self, id):
        administrador = Admistrador.query.get(id)
        # mostrar na tela

    def create(self, params):
        administrador = Admistrador(params)
        # session.add(administrador)
        # session.commit()

    def update(self, params):
        administrador = Admistrador.query.get(id)
        administrador.nome = params["nome"]
        administrador.cpf = params["cpf"]
        administrador.data_nascimento = params["data_nascimento"]
        administrador.endereco = params["endereco"]
        administrador.ativo = params["ativo"]
        administrador.session.commit()

    def delete(self, categoria_id):
        administrador = Admistrador.query.get(id)
        administrador.delete()
        # session.commit()

