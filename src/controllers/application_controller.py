from administradores_controller import AdministradoresController
from eleicoes_controller import EleicoesController


class ApplicationController:
    def __init__(self):
        self.__eleicoes_controller = EleicoesController(self)
        self.__administradores_controller = AdministradoresController(self)
        self.__current_user = None

    def administradores(self):
        self.__administradores_controller.abrir()

    def eleicoes(self):
        self.__eleicoes_controller.abrir()
