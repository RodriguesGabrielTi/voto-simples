from PyQt5 import QtWidgets, uic
from settings import UI_PATH
from views.erro import ErroUi
from views.publicar import PublicarUi
from views.questao import QuestaoUi
from views.relatorio import RelatorioUi
from views.vincular_mesario import VincularMesarioUi
from views.categoria import CategoriaUi


class EleicaoUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, main_window):
        self.categorias_window = None
        self.questoes_window = None
        self.erro_dialog = None
        self.publicar_dialog = None
        self.__controller = aplicacao_controller
        self.__eleicoes_controller = self.__controller.eleicoes_controller()
        self.__main_window = main_window
        super().__init__()


    def show(self) -> None:
        uic.loadUi(f"{UI_PATH}/eleicoes.ui", self)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')
        self.descricao_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_descricao')
        self.estado_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_estado')
        self.estado_field.setEnabled(False)

        self.cadastrar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')
        self.cadastrar_button.clicked.connect(self.cadastrar)

        self.atualizar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_atualizar')
        self.atualizar_button.setEnabled(False)
        self.atualizar_button.clicked.connect(self.atualizar)

        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.excluir_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.excluir)

        self.publicar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_publicar')
        self.publicar_button.setEnabled(False)
        self.publicar_button.clicked.connect(self.publicar)

        self.relatorio_button = self.findChild(QtWidgets.QPushButton, 'pushButton_relatorio')
        self.relatorio_button.setEnabled(False)
        self.relatorio_button.clicked.connect(self.relatorio)

        self.finalizar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_finalizar')
        self.finalizar_button.setEnabled(False)
        self.finalizar_button.clicked.connect(self.finalizar)

        self.categorias_button = self.findChild(QtWidgets.QPushButton, 'pushButton_categorias')
        self.categorias_button.setEnabled(False)
        self.categorias_button.clicked.connect(self.categorias)

        self.questoes_button = self.findChild(QtWidgets.QPushButton, 'pushButton_questoes')
        self.questoes_button.setEnabled(False)
        self.questoes_button.clicked.connect(self.questoes)

        self.mesarios_button = self.findChild(QtWidgets.QPushButton, 'pushButton_mesarios')
        self.mesarios_button.setEnabled(False)
        self.mesarios_button.clicked.connect(self.mesarios)

        # genericos
        self.menu_exit = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_exit')
        self.menu_exit.clicked.connect(self.close)
        self.main_button = self.findChild(QtWidgets.QPushButton, 'pushButton_menu_main')
        self.main_button.clicked.connect(self.abrir_main_window)

        self.table.clicked.connect(self.on_click)
        self.id_selected = None
        self.listar_eleicoes()
        self.showMaximized()
        super().show()

    def listar_eleicoes(self):
        eleicoes = self.__eleicoes_controller.listar()
        self.table.setRowCount(0)
        for eleicao in eleicoes:
            print(eleicao)
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(str(eleicao.id)))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(eleicao.nome))
            self.table.setItem(
                position,
                2,
                QtWidgets.QTableWidgetItem(
                    eleicao.data_inicio.strftime("%d/%m/%Y, %H:%M") if eleicao.data_inicio else "n??o publicada"
                )
            )
            self.table.setItem(
                position,
                3,
                QtWidgets.QTableWidgetItem(
                    eleicao.data_fim.strftime("%d/%m/%Y, %H:%M") if eleicao.data_fim else "n??o finalizada"
                )
            )
            self.table.setItem(position, 4, QtWidgets.QTableWidgetItem(eleicao.estado))

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())
        if self.id_selected == index.sibling(index.row(), 0).data():
            self.clean()
            self.id_selected = None
        else:
            self.id_selected = index.sibling(index.row(), 0).data()
            self.carregar_fields()
        self.botoes()

    def carregar_fields(self):
        eleicao = self.__eleicoes_controller.detalhar(int(self.id_selected))
        self.nome_field.setText(eleicao["nome"])
        self.descricao_field.setText(eleicao["descricao"])
        self.estado_field.setText(eleicao["estado"])

    def clean(self):
        self.nome_field.clear()
        self.descricao_field.clear()
        self.estado_field.clear()
        self.table.clearSelection()

    def cadastrar(self):
        try:
            dados = self.validate_fields()
            self.__eleicoes_controller.criar(dados)
            self.listar_eleicoes()
            self.clean()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def atualizar(self):
        try:
            dados = self.validate_fields()
            self.__eleicoes_controller.atualizar(int(self.id_selected), dados)
            self.carregar_fields()
            self.listar_eleicoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def finalizar(self):
        try:
            self.__eleicoes_controller.finalizar(int(self.id_selected))
            self.carregar_fields()
            self.listar_eleicoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            self.__eleicoes_controller.excluir(int(self.id_selected))
            self.listar_eleicoes()
            self.clean()
            self.id_selected = None
            self.botoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def publicar(self):
        self.publicar_dialog = PublicarUi(self)

    def enviar_publicacao(self, dados):
        try:
            self.__eleicoes_controller.publicar(int(self.id_selected), dados)
            self.carregar_fields()
            self.listar_eleicoes()
        except (ValueError, AssertionError) as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def relatorio(self):
        self.relatorio_window = RelatorioUi(int(self.id_selected), self.__eleicoes_controller)

    def categorias(self):
        categorias_string = self.__eleicoes_controller.categorias_string(self.id_selected)
        self.categorias_window = CategoriaUi(self, categorias_string)

    def enviar_categorias(self, dados):
        categorias = []
        for dado in dados:
            categorias.append(dado.text())
        self.__eleicoes_controller.categorias(int(self.id_selected), categorias)

    def questoes(self):
        self.questoes_window = QuestaoUi(self.__controller, self.__eleicoes_controller.questoes(self.id_selected))

    def mesarios(self):
        self.mesarios_window = VincularMesarioUi(self.__controller, self.id_selected)

    def validate_fields(self):
        dados = {
            "nome": self.nome_field.text(),
            "descricao": self.descricao_field.text()
        }
        for campo in dados:
            if not dados.get(campo):
                raise ValueError("Preencha todos os campos!")
        return dados

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

    def abrir_main_window(self):
        self.close()
        self.__main_window.show()

    def botoes(self):
        if self.id_selected:
            self.atualizar_button.setEnabled(True)
            self.cadastrar_button.setEnabled(False)
            self.excluir_button.setEnabled(True)
            self.publicar_button.setEnabled(True)
            self.questoes_button.setEnabled(True)
            self.mesarios_button.setEnabled(True)
            self.categorias_button.setEnabled(True)
            self.finalizar_button.setEnabled(True)
            if self.estado_field.text() == 'FINALIZADA':
                self.relatorio_button.setEnabled(True)
        else:
            self.atualizar_button.setEnabled(False)
            self.cadastrar_button.setEnabled(True)
            self.excluir_button.setEnabled(False)
            self.publicar_button.setEnabled(False)
            self.questoes_button.setEnabled(False)
            self.mesarios_button.setEnabled(False)
            self.categorias_button.setEnabled(False)

    def abrir_main_window(self):
        self.close()
        self.__main_window.show()
