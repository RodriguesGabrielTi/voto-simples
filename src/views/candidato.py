from PyQt5 import QtWidgets, uic, QtCore
from settings import UI_PATH
from views.erro import ErroUi
from PyQt5.QtGui import QPixmap


class ImageLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("\n\nArraste a Imagem\n\n")

    def setPixmap(self, image):
        super().setPixmap(image)


class CandidatoUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, candidatos_controller):
        self.erro_dialog = None
        self.publicar_dialog = None
        self.__controller = aplicacao_controller
        self.__candidatos_controller = candidatos_controller
        super().__init__()

        uic.loadUi(f"{UI_PATH}/candidatos.ui", self)
        self.setAcceptDrops(True)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.nome_field = self.findChild(QtWidgets.QLineEdit, 'lineEdit_nome')

        self.img_frame = self.findChild(QtWidgets.QFrame, 'frame_img')
        self.imagem_field = ImageLabel()
        self.imagem_field.setParent(self.img_frame)
        self.imagem_field.setGeometry(10, 0, 110, 178)
        self.file_path = None

        self.cadastrar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_cadastrar')
        self.cadastrar_button.clicked.connect(self.cadastrar)

        self.atualizar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_atualizar')
        self.atualizar_button.setEnabled(False)
        self.atualizar_button.clicked.connect(self.atualizar)

        self.excluir_button = self.findChild(QtWidgets.QPushButton, 'pushButton_excluir')
        self.excluir_button.setEnabled(False)
        self.excluir_button.clicked.connect(self.excluir)

        self.table.clicked.connect(self.on_click)
        self.id_selected = None
        self.listar_candidatos()
        self.showMaximized()

    def listar_candidatos(self):
        candidatos = self.__candidatos_controller.listar()
        self.table.setRowCount(0)
        for candidato in candidatos:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(str(candidato.id)))
            self.table.setItem(position, 1, QtWidgets.QTableWidgetItem(candidato.nome))

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
        candidato = self.__candidatos_controller.detalhar(int(self.id_selected))
        self.nome_field.setText(candidato["nome"])
        self.set_image(candidato["imagem"])

    def clean(self):
        self.nome_field.clear()
        self.imagem_field.clear()
        self.imagem_field.setText("\n\nArraste a Imagem\n\n")
        self.file_path = None

    def cadastrar(self):
        try:
            if not self.file_path:
                raise ValueError("Selecione uma imagem válida")
            dados = self.validate_fields()
            dados["imagem"] = QPixmap(self.file_path).toImage()
            self.__candidatos_controller.criar(dados)
            self.listar_candidatos()
            self.clean()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def atualizar(self):
        try:
            if not self.file_path:
                raise ValueError("Selecione uma imagem válida")
            dados = self.validate_fields()
            dados["imagem"] = QPixmap(self.file_path).toImage()
            self.__candidatos_controller.atualizar(int(self.id_selected), dados)
            self.carregar_fields()
            self.listar_candidatos()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def excluir(self):
        try:
            self.__candidatos_controller.excluir(int(self.id_selected))
            self.listar_candidatos()
            self.clean()
            self.id_selected = None
            self.botoes()
        except Exception as e:
            self.__controller.sessao.rollback()
            self.mostrar_erro(str(e))

    def validate_fields(self):
        dados = {
            "nome": self.nome_field.text()
        }
        for campo in dados:
            if not dados.get(campo):
                raise ValueError("Preencha todos os campos!")
        return dados

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)

    def botoes(self):
        if self.id_selected:
            self.atualizar_button.setEnabled(True)
            self.cadastrar_button.setEnabled(False)
            self.excluir_button.setEnabled(True)
        else:
            self.atualizar_button.setEnabled(False)
            self.cadastrar_button.setEnabled(True)
            self.excluir_button.setEnabled(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.file_path = file_path
        self.imagem_field.setPixmap(QPixmap(file_path))
