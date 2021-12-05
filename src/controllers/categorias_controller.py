from models.categoria import Categoria


class CategoriasController:
    def __init__(self, eleicao, sessao):
        self.__categorias_view = None
        self.__eleicao = eleicao
        self.__sessao = sessao

    def abrir(self):
        categorias = self.__sessao(Categoria).all()
        print(categorias)
        pass

    def adicionar(self, categoria_id):
        categoria = self.__sessao(Categoria).get(categoria_id)
        self.__eleicao.categorias.append(categoria)
        self.__sessao.commit()

    def remover(self, categoria_id):
        categoria = self.__sessao(Categoria).get(categoria_id)
        self.__eleicao.categorias.remove(categoria)
        self.__sessao.commit()
