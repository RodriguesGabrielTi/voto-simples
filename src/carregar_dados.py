from datetime import date
from models.administrador import Administrador
from models.categoria import Categoria


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
