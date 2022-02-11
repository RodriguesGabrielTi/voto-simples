from models.votante import Votante
from models.categoria import Categoria


class VotantesController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__administradores_ui = None

    def listar(self):
        return self.__sessao.query(Votante).all()

    def detalhar(self, votante_cpf) -> dict:
        votante = self.__sessao.query(Votante).filter_by(cpf=votante_cpf).first()
        if not votante:
            raise ValueError("votante não achado")
        return votante.__dict__

    def criar(self, parametros):
        votante = Votante(
            nome=parametros["nome"],
            cpf=parametros["cpf"],
            data_nascimento=parametros["data_nascimento"],
            endereco=parametros["endereco"],
            ativo=parametros["ativo"],
            categoria_id=self.__sessao.query(Categoria).filter_by(nome=parametros["categoria"]).first().id
        )
        self.__sessao.add(votante)
        self.__sessao.commit()

    def atualizar(self, votante_cpf, parametros):
        votante = self.__sessao.query(Votante).filter_by(cpf=votante_cpf).first()
        if not votante:
            raise ValueError("votante não achado")
        votante.nome = parametros["nome"]
        votante.cpf = parametros["cpf"]
        votante.data_nascimento = parametros["data_nascimento"]
        votante.endereco = parametros["endereco"] if parametros["endereco"] else ""
        votante.ativo = parametros["ativo"]
        votante.categoria = self.__sessao.query(Categoria).filter_by(nome=parametros["categoria"]).first()
        self.__sessao.commit()

    def excluir(self, votante_cpf):
        votante = self.__sessao.query(Votante).filter_by(cpf=votante_cpf).first()
        if not votante:
            raise ValueError("votante não achado")
        self.__sessao.delete(votante)
        self.__sessao.commit()
