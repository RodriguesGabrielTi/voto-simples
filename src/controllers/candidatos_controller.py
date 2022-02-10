from models.candidato import Candidato
from settings import IMG_PATH
import os


class CandidatosController:
    def __init__(self, questao, sessao, aplicacao_controller):
        self.__questao = questao
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller

    def listar(self):
        candidatos = self.__sessao.query(Candidato).filter_by(questao_id=self.__questao.id)
        return candidatos

    def detalhar(self, candidato_id):
        candidato = self.__sessao.query(Candidato).get(candidato_id)
        if not candidato:
            raise ValueError("Candidato não encontrado")
        return candidato.__dict__

    def criar(self, parametros):
        candidato = Candidato(nome=parametros["nome"], questao_id=self.__questao.id)
        self.__sessao.add(candidato)
        self.__sessao.commit()
        candidato.imagem = IMG_PATH + '/candidato_' + str(candidato.id) + '.png'
        parametros["imagem"].save(candidato.imagem, 'png', 94)
        self.__sessao.commit()

    def atualizar(self, candidato_id, parametros):
        candidato = self.__sessao.query(Candidato).get(candidato_id)
        if not candidato:
            raise ValueError("Candidato não encontrado")
        candidato.nome = parametros["nome"]
        os.remove(candidato.imagem)
        parametros["imagem"].save(candidato.imagem, 'png', 94)
        self.__sessao.commit()

    def excluir(self, candidato_id):
        candidato = self.__sessao.query(Candidato).get(candidato_id)
        if not candidato:
            raise ValueError("Candidato não encontrado")
        os.remove(candidato.imagem)
        self.__sessao.delete(candidato)
        self.__sessao.commit()
