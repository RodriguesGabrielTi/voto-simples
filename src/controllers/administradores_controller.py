from models.administrador import Administrador


class AdministradoresController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__administradores_ui = None

    def listar(self):
        return self.__sessao.query(Administrador).all()

    def detalhar(self, administrador_cpf) -> dict:
        administrador = self.__sessao.query(Administrador).filter_by(cpf=administrador_cpf).first()
        if not administrador:
            raise ValueError("administrador não achado")
        return administrador.__dict__

    def criar(self, parametros):
        administrador = Administrador(
            nome=parametros["nome"],
            cpf=parametros["cpf"],
            data_nascimento=parametros["data_nascimento"],
            endereco=parametros["endereco"],
            ativo=parametros["ativo"],
            senha=parametros["senha"]
        )
        self.__sessao.add(administrador)
        self.__sessao.commit()

    def atualizar(self, administrador_cpf, parametros):
        administrador = self.__sessao.query(Administrador).filter_by(cpf=administrador_cpf).first()
        if not administrador:
            raise ValueError("administrador não achado")
        administrador.nome = parametros["nome"]
        administrador.cpf = parametros["cpf"]
        administrador.data_nascimento = parametros["data_nascimento"]
        administrador.endereco = parametros["endereco"]
        administrador.ativo = parametros["ativo"]
        administrador.senha = parametros["senha"]
        self.__sessao.commit()

    def excluir(self, administrador_cpf):
        administrador = self.__sessao.query(Administrador).filter_by(cpf=administrador_cpf).first()
        if not administrador:
            raise ValueError("administrador não achado")
        self.__sessao.delete(administrador)
        self.__sessao.commit()
