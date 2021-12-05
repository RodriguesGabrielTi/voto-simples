from src.models.questao import Questao


class QuestoesController:
    def __init__(self, eleicao, sessao):
        self.__eleicao = eleicao
        self.__questoes_view = None
        self.__sessao = sessao

    def abrir(self):
        pass

    def index(self):
        questoes = self.__eleicao.questoes
        print(questoes)

    def show(self, questao_id):
        questao = self.__sessao.query(Questao).get(questao_id)
        print(questao)
        # mostrar na tela

    def create(self, params):
        questao = Questao(nome=params["nome"], descricao=params["descricao"],
                          numero_escolhas=params["numero_escolhas"], eleicao_id=self.__eleicao.id)
        self.__sessao.add(questao)
        self.__sessao.commit()

    def update(self, params):
        questao = self.__sessao.query(Questao).get(params["id"])
        questao.nome = params["nome"]
        questao.descricao = params["descricao"]
        questao.numero_escolhas = params["numero-escolhas"]
        self.__sessao.commit()

    def delete(self, questao_id):
        questao = self.__sessao.query(Questao).get(questao_id)
        questao.delete()
        self.__sessao.commit()

    def candidatos(self):
        pass