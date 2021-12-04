from src.models.categoria import Categoria


class CategoriasController:
    def __init__(self, eleicao):
        self.__categorias_view = None
        self.__eleicao = eleicao

    def abrir(self):
        pass

    def adicionar(self, categoria_id):
        categoria = Categoria.session.get(categoria_id)
        self.__eleicao.categorias.append(categoria)
        # session.commit()

    def remover(self, categoria_id):
        categoria = Categoria.session.get(categoria_id)
        self.__eleicao.categorias.remove(categoria)
        # session.commit()
