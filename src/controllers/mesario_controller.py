from models.eleicao_mesario import EleicaoMesario
from models.mesario import Mesario


class MesarioController:
    def __init__(self, aplicacao_controller, sessao):
        self.__sessao = sessao
        self.__aplicacao_controller = aplicacao_controller
        self.__mesarioes_ui = None

    def listar(self):
        return self.__sessao.query(Mesario).all()

    def pesquisar(self, cpf):
        cpf = "%{}%".format(cpf)
        return self.__sessao.query(Mesario).filter(Mesario.cpf.like(cpf)).all()

    def vincular_eleicao(self, cpf, eleicao_id):
        mesario = self.__sessao.query(Mesario).filter_by(cpf=cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        eleicao_mesario = EleicaoMesario(mesario_id=mesario.id, eleicao_id=eleicao_id)
        self.__sessao.add(eleicao_mesario)
        self.__sessao.commit()

    def desinvilcular_eleicao(self, cpf, eleicao_id):
        vinculo = self.__sessao.query(
            EleicaoMesario
        ).join(
            Mesario
        ).filter(
            Mesario.cpf == cpf,
            EleicaoMesario.eleicao_id == eleicao_id,
            EleicaoMesario.mesario_id == Mesario.id
        ).first()
        if not vinculo:
            raise ValueError("Mesário não está vinculado!")
        self.__sessao.delete(vinculo)
        self.__sessao.commit()


    def detalhar(self, mesario_cpf) -> dict:
        mesario = self.__sessao.query(Mesario).filter_by(cpf=mesario_cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        return mesario.__dict__

    def criar(self, parametros):
        mesario = Mesario(
            nome=parametros["nome"],
            cpf=parametros["cpf"],
            data_nascimento=parametros["data_nascimento"],
            endereco=parametros["endereco"],
            ativo=parametros["ativo"],
            senha=parametros["senha"]
        )
        self.__sessao.add(mesario)
        self.__sessao.commit()

    def atualizar(self, mesario_cpf, parametros):
        mesario = self.__sessao.query(Mesario).filter_by(cpf=mesario_cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        mesario.nome = parametros["nome"]
        mesario.cpf = parametros["cpf"]
        mesario.data_nascimento = parametros["data_nascimento"]
        mesario.endereco = parametros["endereco"] if parametros["endereco"] else ""
        mesario.ativo = parametros["ativo"]
        mesario.senha = parametros["senha"]
        self.__sessao.commit()

    def esta_vinculado_a_eleicao(self, eleicao_id, mesario_id):
        return bool(self.__sessao.query(EleicaoMesario).filter_by(eleicao_id=eleicao_id, mesario_id=mesario_id).first())

    def excluir(self, mesario_cpf):
        mesario = self.__sessao.query(Mesario).filter_by(cpf=mesario_cpf).first()
        if not mesario:
            raise ValueError("mesario não achado")
        self.__sessao.delete(mesario)
        self.__sessao.commit()
