from models.categoria import Categoria


def carregar(sessao):
    if len(sessao.query(Categoria).all()) == 0:
        estudante = Categoria(nome="estudante")
        professor = Categoria(nome="professor")
        tae = Categoria(nome="tae")

        sessao.add(estudante)
        sessao.add(professor)
        sessao.add(tae)

        sessao.commit()