from src.models.eleicao import Eleicao
from src.controllers.questoes_controller import QuestoesController
from src.controllers.categorias_controller import CategoriasController


class EleicoesController:
    def __init__(self, application_controller):
        self.__application_controller = application_controller
        self.__eleicoes_view = None

    def abrir(self):
        pass

    def index(self):
        eleicoes = Eleicao.query.all()

    def show(self, eleicao_id):
        eleicao = Eleicao.query.get(eleicao_id)
        # mostrar na tela

    def create(self, params):
        eleicao = Eleicao(nome=params["nome"], descricao=params["descricao"])
        # session.add(administrador)
        # session.commit()

    def update(self, params):
        eleicao = Eleicao.query.get(params["id"])
        eleicao.nome = params["nome"]
        eleicao.descricao = params["descricao"]
        eleicao.session.commit()

    def delete(self, eleicao_id):
        eleicao = Eleicao.query.get(eleicao_id)
        eleicao.delete()
        # session.commit()

    def publicar(self, eleicao_id):
        eleicao = Eleicao.query.get(eleicao_id)
        eleicao.estado = "publicada"
        # session.commit()

    def questoes(self, eleicao_id):
        eleicao = Eleicao.query.get(eleicao_id)
        QuestoesController(eleicao).abrir()

    def categorias(self, eleicao_id):
        eleicao = Eleicao.query.get(eleicao_id)
        CategoriasController(eleicao).abrir()
