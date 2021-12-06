from models.questao import Questao


class QuestoesController:
    def __init__(self, eleicao, sessao):
        self.__eleicao = eleicao
        self.__questoes_ui = None
        self.__sessao = sessao

    def abrir(self):
        # self.__questoes_ui.abrir()
        pass

    def index(self):
        questoes = self.__eleicao.questoes
        return questoes

    def show(self, questao_id):
        questao = self.__sessao.query(Questao).get(questao_id)
        return questao

    def create(self, parametros):
        questao = Questao(nome=parametros["nome"], descricao=parametros["descricao"],
                          numero_escolhas=parametros["numero_escolhas"], eleicao_id=self.__eleicao.id)
        self.__sessao.add(questao)
        self.__sessao.commit()

    def update(self, questao_id, parametros):
        questao = self.__sessao.query(Questao).get(questao_id)
        questao.nome = parametros["nome"]
        questao.descricao = parametros["descricao"]
        questao.numero_escolhas = parametros["numero_escolhas"]
        self.__sessao.commit()

    def delete(self, questao_id):
        questao = self.__sessao.query(Questao).get(questao_id)
        questao.delete()
        self.__sessao.commit()

    def candidatos(self):
        pass