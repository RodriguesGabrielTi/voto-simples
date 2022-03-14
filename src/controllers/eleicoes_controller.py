import datetime
import uuid

from models.categoria import Categoria
from models.eleicao import Eleicao
from controllers.questoes_controller import QuestoesController
from models.eleicao_mesario import EleicaoMesario
from models.mesario import Mesario
import pandas

from models.questao import Questao
from models.registro_de_votacao import RegistroDeVotacao
from models.votante import Votante


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

    def finalizar(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        if eleicao.estado != 'EM_VOTACAO':
            raise ValueError("Eleicao precisa estar EM VOTACÃO para ser finalizada!")
        eleicao.estado = 'FINALIZADA'
        eleicao.data_fim = datetime.datetime.today()
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

    def gerar_relatorio(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        votantes = self.__sessao.query(Votante).filter(
            Votante.categoria_id.in_([categoria.id for categoria in eleicao.categorias_validas])
        ).all()
        votantes_presentes = self.__sessao.query(
            Votante
        ).join(
            RegistroDeVotacao
        ).filter(
            RegistroDeVotacao.votante_id == Votante.id,
            RegistroDeVotacao.eleicao_id == eleicao.id
        ).all()
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        if eleicao.estado != 'FINALIZADA':
            raise ValueError("Eleicao não finalizada!")
        path = f'temp/{uuid.uuid4()}.xlsx'

        escritor = pandas.ExcelWriter(path, engine='xlsxwriter')
        eleicao_dados = {
            "eleição": [eleicao.nome],
            "iniciada em": [eleicao.data_inicio],
            "finalizada em": [eleicao.data_fim],
            "votantes aptos": [len(votantes)],
            "votantes presentes": [len(votantes_presentes)],
            "votantes ausentes": [len(votantes) - len(votantes_presentes)],
            "votos nulos": [sum([questao.nulos for questao in eleicao.questoes])],
            "votos brancos": [sum([questao.brancos for questao in eleicao.questoes])]
        }
        pandas.DataFrame(eleicao_dados).to_excel(escritor, sheet_name="Eleição", index=False)
        for questao in eleicao.questoes:
            dados = {
                "nome do candidato": [],
                "votos": []
            }
            for candidato in questao.candidatos:
                dados["nome do candidato"].append(candidato.nome)
                dados["votos"].append(len(candidato.votos))
            pandas.DataFrame(dados).to_excel(escritor, sheet_name=questao.nome, index=False)
        escritor.save()
        return path

    def questoes(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        return QuestoesController(eleicao, self.__sessao, self.__aplicacao_controller)

    def categorias(self, eleicao_id, categorias):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        eleicao.categorias_validas = []
        for categoria in categorias:
            eleicao.categorias_validas.append(self.__sessao.query(Categoria).filter_by(nome=categoria).first())
        self.__sessao.commit()

    def categorias_string(self, eleicao_id):
        eleicao = self.__sessao.query(Eleicao).get(eleicao_id)
        if not eleicao:
            raise ValueError("Eleicao não encontrada")
        categorias_string = ""
        for categoria in eleicao.categorias_validas:
            categorias_string += categoria.nome + ', '
        return categorias_string

    def checar_permissao_para_modificar(self, eleicao: Eleicao):
        if eleicao.estado != 'EM_CRIACAO':
            raise ValueError("Só é possível alterar eleição em criação")

    def listar_mesario_eleicoes(self, mesario: Mesario):
        eleicoes = self.__sessao.query(
            Eleicao
        ).join(
            EleicaoMesario
        ).filter(
            EleicaoMesario.mesario_id == mesario.id,
            EleicaoMesario.eleicao_id == Eleicao.id,
            Eleicao.estado == "EM_VOTACAO"
        ).all()
        return eleicoes
