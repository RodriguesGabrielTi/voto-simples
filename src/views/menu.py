from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from views.administrador import AdminUi
from views.eleicao import EleicaoUi


class MenuUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller):
        super().__init__()
        uic.loadUi(f"{UI_PATH}/menu.ui", self)
        self.__controllers = aplicacao_controller
        self.votantes_window = None
        self.mesarios_window = None
        self.admin_window = None
        self.eleicao_window = None

        self.menu_exit = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_exit')
        self.menu_exit.clicked.connect(self.close)
        self.admin_menu_button = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_admin')
        self.admin_button = self.findChild(QtWidgets.QPushButton, 'pushButton_admin')
        self.admin_button.clicked.connect(self.abrir_admin_window)
        self.admin_menu_button.clicked.connect(self.abrir_admin_window)

        self.eleicao_menu_button = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_eleicao')
        self.eleicao_button = self.findChild(QtWidgets.QPushButton, 'pushButton_eleicao')
        self.eleicao_button.clicked.connect(self.abrir_eleicao_window)
        self.eleicao_menu_button.clicked.connect(self.abrir_eleicao_window)

        self.showMaximized()

    def abrir_admin_window(self):
        if self.admin_window is None:
            self.close()
            self.admin_window = AdminUi(self.__controllers)

    def abrir_eleicao_window(self):
        if self.eleicao_window is None:
            self.close()
            self.eleicao_window = EleicaoUi(self.__controllers)

