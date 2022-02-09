from models.questao import Questao


class QuestoesController:
    def __init__(self, eleicao, sessao, aplicacao_controller):
        self.__eleicao = eleicao
        self.__questoes_ui = None
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller

    def listar(self):
        questoes = self.__sessao.query(Questao).filter_by(eleicao_id=self.__eleicao.id)
        return questoes

    def detalhar(self, questao_id):
        questao = self.__sessao.query(Questao).get(questao_id)
        if not questao:
            raise ValueError("Eleicão não encontrada")
        return questao.__dict__

    def criar(self, parametros):
        questao = Questao(nome=parametros["nome"], descricao=parametros["descricao"],
                          numero_escolhas=parametros["numero_escolhas"], eleicao_id=self.__eleicao.id)
        self.__sessao.add(questao)
        self.__sessao.commit()

    def atualizar(self, questao_id, parametros):
        questao = self.__sessao.query(Questao).get(questao_id)
        if not questao:
            raise ValueError("Questao não encontrada")
        questao.nome = parametros["nome"]
        questao.descricao = parametros["descricao"]
        questao.numero_escolhas = parametros["numero_escolhas"]
        self.__sessao.commit()

    def excluir(self, questao_id):
        questao = self.__sessao.query(Questao).get(questao_id)
        self.__sessao.delete(questao)
        self.__sessao.commit()

    def candidatos(self):
        pass