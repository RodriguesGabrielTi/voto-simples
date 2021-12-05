from src.models.eleicao import Eleicao
from src.controllers.questoes_controller import QuestoesController
from src.controllers.categorias_controller import CategoriasController


class EleicoesController:
    def __init__(self, application_controller, sessao):
        self.__sessao = sessao
        self.__application_controller = application_controller
        self.__eleicoes_view = None

    def abrir(self):
        pass

    def index(self):
        eleicoes = self.__sessao.query(Eleicao).all()
        print(eleicoes)

    def show(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        print(eleicao)

    def create(self, params):
        eleicao = Eleicao(nome=params["nome"], descricao=params["descricao"])
        self.__sessao.add(eleicao)
        self.__sessao.commit()

    def update(self, params):
        eleicao = self.__sessao.query(Eleicao).get(params["id"])
        eleicao.nome = params["nome"]
        eleicao.descricao = params["descricao"]
        self.__sessao.commit()

    def delete(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        eleicao.delete()
        self.__sessao.commit()

    def publicar(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        eleicao.estado = "publicada"
        self.__sessao.commit()

    def questoes(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        QuestoesController(eleicao, self.__sessao).abrir()

    def categorias(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        CategoriasController(eleicao, self.__sessao).abrir()
