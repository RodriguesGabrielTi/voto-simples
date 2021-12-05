from src.models.eleicao import Eleicao
from src.controllers.questoes_controller import QuestoesController
from src.controllers.categorias_controller import CategoriasController


class EleicoesController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__eleicoes_ui = None

    def abrir(self):
        # self.__eleicoes_ui.abrir()
        pass

    def listar(self):
        eleicoes = self.__sessao.query(Eleicao).all()
        return eleicoes

    def detalhar(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        return eleicao

    def criar(self, parametros):
        eleicao = Eleicao(nome=parametros["nome"], descricao=parametros["descricao"])
        self.__sessao.add(eleicao)
        self.__sessao.commit()

    def atualizar(self, eleicao_id, parametros):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        eleicao.nome = parametros["nome"]
        eleicao.descricao = parametros["descricao"]
        self.__sessao.commit()

    def excluir(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        eleicao.delete()
        self.__sessao.commit()

    def publicar(self, eleicao_id, parametros):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        eleicao.data_inicio = parametros["data_inicio"]
        eleicao.data_fim = parametros["data_fim"]
        eleicao.estado = "publicada"
        self.__sessao.commit()

    def questoes(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        QuestoesController(eleicao, self.__sessao).abrir()

    def categorias(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        CategoriasController(eleicao, self.__sessao).abrir()
