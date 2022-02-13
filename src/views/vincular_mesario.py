from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from views.erro import ErroUi
from PyQt5 import QtCore


class VincularMesarioUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, eleicao_id):
        self.erro_dialog = None
        self.publicar_dialog = None
        self.__controller = aplicacao_controller
        self.__m_controller = aplicacao_controller.mesarios_controller()
        self.__eleicao_id = eleicao_id
        super().__init__()

        uic.loadUi(f"{UI_PATH}/vincular_mesario.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')

        self.cadastrar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')
        self.cadastrar_button.clicked.connect(self.cadastrar)

        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.excluir_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.excluir)

        self.buscar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_buscar')
        self.buscar_button.clicked.connect(self.buscar)

        self.cpf_de_busca = self.findChild(QtWidgets.QLineEdit, 'lineEdit_cpf')
        self.cpf_de_busca.textChanged.connect(self.validate_cpf)
        self.cpf_de_busca.setMaxLength(11)
        
        self.table.clicked.connect(self.on_click)
        self.cpf_selected = None
        self.vinculado = False
        self.listar_mesarios()
        self.showMaximized()

    def validate_cpf(self):
        reg_ex = QRegExp("^[0-9]+$")
        cpf_validator = QRegExpValidator(reg_ex, self.cpf_de_busca)
        self.cpf_de_busca.setValidator(cpf_validator)

    def listar_mesarios(self):
        mesarios = self.__controller.mesarios_controller().listar()
        self.build_table(mesarios)

    def build_table(self, mesarios):
        self.table.setRowCount(0)
        for mesario in mesarios:
            position = self.table.rowCount()
            vinculado = self.__m_controller.esta_vinculado_a_eleicao(self.__eleicao_id, mesario.id)
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(str(mesario.nome)))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(mesario.cpf))
            self.table.setItem(
                position,
                2,
                QtWidgets.QTableWidgetItem(
                    "SIM" if vinculado else "NÃO"
                )
            )

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())
        if self.cpf_selected == index.sibling(index.row(), 1).data():
            self.clean()
            self.cpf_selected = None
        else:
            self.cpf_selected = index.sibling(index.row(), 1).data()
            self.vinculado = index.sibling(index.row(), 2).data() == "SIM"
        self.botoes()

    def clean(self):
        self.table.clearSelection()

    def cadastrar(self):
        try:
            self.__m_controller.vincular_eleicao(self.cpf_selected, self.__eleicao_id)
            self.listar_mesarios()
            self.clean()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            self.__m_controller.desinvilcular_eleicao(self.cpf_selected, self.__eleicao_id)
            self.listar_mesarios()
            self.clean()
            self.cpf_selected = None
            self.botoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

    def botoes(self):
        if self.cpf_selected:
            if self.vinculado:
                self.excluir_button.setEnabled(True)
                self.cadastrar_button.setEnabled(False)
            else:
                self.excluir_button.setEnabled(False)
                self.cadastrar_button.setEnabled(True)
        else:
            self.cadastrar_button.setEnabled(False)
            self.excluir_button.setEnabled(False)

    def buscar(self):
        cpf = self.cpf_de_busca.text()
        if not cpf:
            self.listar_mesarios()
            return
        self.build_table(self.__m_controller.pesquisar(cpf))
