from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from views.administrador import AdminUi


class MenuUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{UI_PATH}/menu.ui", self)
        self.votantes_window = None
        self.mesarios_window = None
        self.admin_window = None
        self.eleicao_window = None

        self.admin_menu_button = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_admin')
        self.admin_button = self.findChild(QtWidgets.QPushButton, 'pushButton_admin')
        self.admin_button.clicked.connect(self.abrir_admin_window)
        self.admin_menu_button.clicked.connect(self.abrir_admin_window)
        self.show()

    def abrir_admin_window(self):
        if self.admin_window is None:
            self.close()
            self.admin_window = AdminUi()
            self.admin_window.show()
