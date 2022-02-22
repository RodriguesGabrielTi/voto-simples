from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from views.administrador import AdminUi
from views.eleicao import EleicaoUi
from views.mesario import MesarioUi
from views.votante import VotanteUi


class MenuUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller):
        super().__init__()
        self.__controllers = aplicacao_controller
        self.votante_window = None
        self.mesarios_window = None
        self.admin_window = None
        self.eleicao_window = None

    def show(self) -> None:
        uic.loadUi(f"{UI_PATH}/menu.ui", self)
        self.menu_exit = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_exit')
        self.menu_exit.clicked.connect(self.close)

        self.mesarios_button = self.findChild(QtWidgets.QPushButton, 'pushButton_mesarios')
        self.mesarios_button.clicked.connect(self.abrir_mesario_window)

        self.admin_button = self.findChild(QtWidgets.QPushButton, 'pushButton_admin')
        self.admin_button.clicked.connect(self.abrir_admin_window)

        self.eleicao_button = self.findChild(QtWidgets.QPushButton, 'pushButton_eleicao')
        self.eleicao_button.clicked.connect(self.abrir_eleicao_window)

        self.votante_button = self.findChild(QtWidgets.QPushButton, 'pushButton_votantes')
        self.votante_button.clicked.connect(self.abrir_votante_window)

        self.showMaximized()
        super().show()

    def abrir_admin_window(self):
        if self.admin_window is None:
            self.close()
            self.admin_window = AdminUi(self.__controllers, MenuUi(self.__controllers))

    def abrir_eleicao_window(self):
        if self.eleicao_window is None:
            self.close()
            self.eleicao_window = EleicaoUi(self.__controllers, MenuUi(self.__controllers))
            self.eleicao_window.show()

    def abrir_mesario_window(self):
        if self.mesarios_window is None:
            self.close()
            self.mesarios_window = MesarioUi(
                self.__controllers,
                MenuUi(self.__controllers),
                EleicaoUi(self.__controllers, MenuUi(self.__controllers))
            )

    def abrir_votante_window(self):
        if self.votante_window is None:
            self.close()
            self.eleicao_window = VotanteUi(self.__controllers, MenuUi(self.__controllers))

