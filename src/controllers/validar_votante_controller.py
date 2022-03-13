from controllers.votacao_controller import VotacaoController
from models.votante import Votante
from models.eleicao import Eleicao


class ValidarVotanteController:
    def __init__(self, eleicao_id, sessao, aplicacao_controller):
        self.__sessao = sessao
        self.__eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        self.__aplicacao_controller = aplicacao_controller

    def autenticar(self, cpf):
        votante = self.__sessao.query(Votante).filter_by(cpf=cpf).first()
        if votante is None:
            raise ValueError("Votante não cadastrado")
        if votante.categoria not in self.__eleicao.categorias_validas:
            raise ValueError("Votante não pode votar nesta eleiçao")

        return True

    def votacao(self, cpf):
        votante = self.__sessao.query(Votante).filter_by(cpf=cpf).first()
        return VotacaoController(self.__eleicao, votante, self.__aplicacao_controller, self.__sessao)
