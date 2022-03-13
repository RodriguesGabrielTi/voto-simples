class VotacaoController:
    def __init__(self, eleicao, votante, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__eleicao = eleicao
        self.__votante = votante
        self.__aplicacao_controller = aplicacao_controller

    def paginas(self):
        return self.__eleicao.questoes
