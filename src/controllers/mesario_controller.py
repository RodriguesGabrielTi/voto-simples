from models.mesario import Mesario


class MesarioController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__mesarioes_ui = None

    def listar(self):
        return self.__sessao.query(Mesario).all()

    def detalhar(self, mesario_cpf) -> dict:
        mesario = self.__sessao.query(Mesario).filter_by(cpf=mesario_cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        return mesario.__dict__

    def criar(self, parametros):
        mesario = Mesario(
            nome=parametros["nome"],
            cpf=parametros["cpf"],
            data_nascimento=parametros["data_nascimento"],
            endereco=parametros["endereco"],
            ativo=parametros["ativo"],
            senha=parametros["senha"]
        )
        self.__sessao.add(mesario)
        self.__sessao.commit()

    def atualizar(self, mesario_cpf, parametros):
        mesario = self.__sessao.query(Mesario).filter_by(cpf=mesario_cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        mesario.nome = parametros["nome"]
        mesario.cpf = parametros["cpf"]
        mesario.data_nascimento = parametros["data_nascimento"]
        mesario.endereco = parametros["endereco"] if parametros["endereco"] else ""
        mesario.ativo = parametros["ativo"]
        mesario.senha = parametros["senha"]
        self.__sessao.commit()

    def excluir(self, mesario_cpf):
        mesario = self.__sessao.query(Mesario).filter_by(cpf=mesario_cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        self.__sessao.delete(mesario)
        self.__sessao.commit()
