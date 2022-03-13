from models.questao import Questao
from models.registro_de_votacao import RegistroDeVotacao
from models.voto import Voto


class VotacaoController:
    def __init__(self, eleicao, votante, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__eleicao = eleicao
        self.__votante = votante
        self.__aplicacao_controller = aplicacao_controller

    def paginas(self):
        return self.__eleicao.questoes

    def votar(self, escolhas: dict):
        for escolha in escolhas.keys():
            for candidato in escolhas[escolha]["candidatos"]:
                voto = Voto(candidato_id=candidato.id)
                self.__sessao.add(voto)
            if escolhas[escolha]["sobras"]:
                questao = self.__sessao.query(Questao).get(escolha)
                if escolhas[escolha]["sobras"]["tipo"] == "branco":
                    questao.brancos += escolhas[escolha]["sobras"]["numero"]
                else:
                    questao.nulos += escolhas[escolha]["sobras"]["numero"]

        registro = RegistroDeVotacao(eleicao_id=self.__eleicao.id, votante_id=self.__votante.id)
        self.__sessao.add(registro)
        self.__sessao.commit()
