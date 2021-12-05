from src.controllers.administradores_controller import AdministradoresController
from src.controllers.eleicoes_controller import EleicoesController
from src.views.application_view import ApplicationView


class ApplicationController:
    def __init__(self, sessao):
        self.__session = sessao
        self.__eleicoes_controller = EleicoesController(self, sessao)
        self.__administradores_controller = AdministradoresController(self, sessao)
        self.__current_user = None
        self.__application_view = ApplicationView(self)

    def abrir(self):
        self.__application_view.abrir()

    def administradores(self):
        self.__administradores_controller.abrir()

    def eleicoes(self):
        self.__eleicoes_controller.abrir()
