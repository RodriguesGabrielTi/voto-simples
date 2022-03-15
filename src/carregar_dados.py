import datetime
from datetime import date
from models.categoria import Categoria
from models.administrador import Administrador
from models.candidato import Candidato
from models.eleicao import Eleicao
from models.questao import Questao
from models.voto import Voto
from models.mesario import Mesario
from models.eleicao_mesario import EleicaoMesario
from models.votante import Votante
from models.registro_de_votacao import RegistroDeVotacao
from models.base_model import BaseModel
from engine import engine

BaseModel.metadata.create_all(engine)


def carregar(sessao):
    with sessao.begin():
        if len(sessao.query(Categoria).all()) == 0:
            estudante = Categoria(nome="estudante")
            professor = Categoria(nome="professor")
            tae = Categoria(nome="tae")

            sessao.add(estudante)
            sessao.add(professor)
            sessao.add(tae)
            sessao.commit()

    with sessao.begin():
        if len(sessao.query(Administrador).all()) == 0:
            admin = Administrador(
                nome="admin",
                senha="1234",
                cpf="00000000000",
                data_nascimento=date(year=2001, month=10, day=1),
                endereco="endereco"
            )
            sessao.add(admin)
            sessao.commit()

    with sessao.begin():
        if len(sessao.query(Eleicao).all()) == 0:
            eleicao = Eleicao(
                nome="EleicaoTeste",
                descricao="gerada automaticamente")
            sessao.add(eleicao)

            eleicao.categorias_validas = sessao.query(Categoria).all()

            questao = Questao(nome="questao1", descricao="gerada automaticamente",
                              numero_escolhas=2, eleicao_id=eleicao.id)
            sessao.add(questao)
            for i in range(1, 4):
                candidato = Candidato(nome="Candidato" + str(i),
                                      imagem="statics/default_candidato_img/default" + str(i) + ".jpg")
                candidato.questao = questao
                sessao.add(candidato)

            questao2 = Questao(nome="questao2", descricao="gerada automaticamente",
                              numero_escolhas=2, eleicao_id=eleicao.id)
            sessao.add(questao2)
            for i in range(1, 4):
                candidato = Candidato(nome="Candidato" + str(i+3),
                                      imagem="statics/default_candidato_img/default" + str(i) + ".jpg")
                candidato.questao = questao2
                sessao.add(candidato)

            mesario = Mesario(nome="mesario", senha="1234", cpf="11111111111",
                              data_nascimento=date(year=2002, month=10, day=1), endereco="endereco")
            sessao.add(mesario)

            eleicao_mesario = EleicaoMesario(mesario_id=1, eleicao_id=1)
            sessao.add(eleicao_mesario)

            eleicao.data_inicio = datetime.datetime.now()
            eleicao.data_fim = datetime.datetime(year=2023, month=10, day=1)
            eleicao.estado = "EM_VOTACAO"

            sessao.commit()

    with sessao.begin():
        if len(sessao.query(Votante).all()) == 0:
            votante = Votante(
                nome="Votante",
                cpf="22222222222",
                data_nascimento=date(year=2001, month=10, day=1),
                endereco="endereco",
                categoria_id=1
            )
            votante2 = Votante(
                nome="Votante2",
                cpf="33333333333",
                data_nascimento=date(year=2001, month=10, day=1),
                endereco="endereco",
                categoria_id=2
            )
            votante3 = Votante(
                nome="Votante3",
                cpf="44444444444",
                data_nascimento=date(year=2001, month=10, day=1),
                endereco="endereco",
                categoria_id=3
            )
            sessao.add(votante)
            sessao.add(votante2)
            sessao.add(votante3)
            sessao.commit()

