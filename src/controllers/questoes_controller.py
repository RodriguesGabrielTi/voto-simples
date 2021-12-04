from src.models.questao import Questao


class QuestoesController:
    def __init__(self, eleicao):
        self.__eleicao = eleicao
        self.__questoes_view = None

    def abrir(self):
        pass

    def index(self):
        questao = Questao.query.all()

    def show(self, id):
        questao = Questao.query.get(id)
        # mostrar na tela

    def create(self, params):
        questao = Questao(params)
        questao.eleicao_id = self.__eleicao.id
        # session.add(administrador)
        # session.commit()

    def update(self, params):
        questao = Questao.query.get(id)
        questao.nome = params["nome"]
        questao.descricao = params["descricao"]
        questao.session.commit()

    def delete(self, id):
        questao = Questao.query.get(id)
        questao.delete()
        # session.commit()

    def candidatos(self):
        pass