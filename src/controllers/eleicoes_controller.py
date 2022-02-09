from models.eleicao import Eleicao
from controllers.questoes_controller import QuestoesController
from controllers.categorias_controller import CategoriasController


class EleicoesController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__eleicoes_ui = None

    def listar(self):
        eleicoes = self.__sessao.query(Eleicao).all()
        return eleicoes

    def detalhar(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicão não encontrada")
        return eleicao.__dict__

    def criar(self, parametros):
        eleicao = Eleicao(nome=parametros["nome"], descricao=parametros["descricao"])
        self.__sessao.add(eleicao)
        self.__sessao.commit()

    def atualizar(self, eleicao_id, parametros):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        self.checar_permissao_para_modificar(eleicao)
        eleicao.nome = parametros["nome"]
        eleicao.descricao = parametros["descricao"]
        self.__sessao.commit()

    def excluir(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        self.checar_permissao_para_modificar(eleicao)
        self.__sessao.delete(eleicao)
        self.__sessao.commit()

    def publicar(self, eleicao_id, parametros):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        if eleicao.estado == 'EM_VOTACAO':
            raise ValueError("Eleicao já publicada")
        if eleicao.estado == 'FINALIZADA':
            raise ValueError("Eleicao já finalizada")

        eleicao.data_inicio = parametros["data_inicio"]
        eleicao.data_fim = parametros["data_fim"]
        eleicao.estado = "EM_VOTACAO"
        self.__sessao.commit()

    def questoes(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        return QuestoesController(eleicao, self.__sessao, self.__aplicacao_controller)

    def categorias(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        CategoriasController(eleicao, self.__sessao).abrir()

    def checar_permissao_para_modificar(self, eleicao: Eleicao):
        if eleicao.estado != 'EM_CRIACAO':
            raise ValueError("Só é possível alterar eleição em criação")

