from PyQt5 import QtWidgets, uic, QtCore

from settings import UI_PATH
from views.confirmar_voto import ConfirmarVotoUi
from views.erro import ErroUi
from PyQt5.QtGui import QPixmap

from views.voto_computado import VotoComputadoUi


class ImageLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)

    def setPixmap(self, image):
        super().setPixmap(image)


class Pagina(QtWidgets.QWidget):
    def __init__(self, questao, votacao):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi(f"{UI_PATH}/pagina.ui", self)
        self.votacao = votacao

        self.table: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, 'table')
        self.table.clicked.connect(self.on_click)

        self.img_frame = self.findChild(QtWidgets.QFrame, 'frame_img')
        self.imagem_field = ImageLabel()
        self.imagem_field.setParent(self.img_frame)
        self.imagem_field.setGeometry(10, 0, 110, 178)
        self.file_path = None

        self.questao_nome: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'label_questao')
        self.questao_nome.setText(questao.nome)

        self.questao_escolhas: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'label_n_escolhas')
        self.questao_escolhas.setText("Selecionar " + str(questao.numero_escolhas) + " candidatos")

        self.questao = questao

        self.selecionar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_selecionar')
        self.selecionar_button.clicked.connect(self.votacao.proxima_pagina)

        self.__voltar_button = self.findChild(QtWidgets.QPushButton, 'pushButton_voltar')
        self.__voltar_button.clicked.connect(self.votacao.voltar)
        self.listar_candidatos()


    def listar_candidatos(self):
        candidatos = self.questao.candidatos
        self.table.setRowCount(0)
        for candidato in candidatos:
            position = self.table.rowCount()
            self.table.insertRow(position)
            self.table.setItem(position, 0, QtWidgets.QTableWidgetItem(candidato.nome))

    def on_click(self):
        index = (self.table.selectionModel().currentIndex())

        candidato = self.questao.candidatos[index.row()]
        self.set_image(candidato.imagem)

    def set_image(self, file_path):
        self.file_path = file_path
        self.imagem_field.setPixmap(QPixmap(file_path))

    def selecionados(self):
        if len(self.table.selectedIndexes()) > self.questao.numero_escolhas:
            raise ValueError("Erro na questao: " + self.questao.nome + ". São apenas permitidas "
                             + str(self.questao.numero_escolhas) + " escolhas")

        candidatos = []
        for index in self.table.selectedIndexes():
            candidatos.append(self.questao.candidatos[index.row()])

        sobras = None
        if len(self.table.selectedIndexes()) < self.questao.numero_escolhas:
            box = QtWidgets.QMessageBox()
            box.setWindowTitle("Votos Sobrando")
            box.setText("Na questão: " + self.questao.nome
                                                    + " foram selecionados apenas "
                                                    + str(len(self.table.selectedIndexes())) + " de "
                                                    + str(self.questao.numero_escolhas)
                                                    + ". Deseja votar nulo ou branco?")

            box.addButton("Branco", QtWidgets.QMessageBox.ButtonRole.YesRole)
            box.addButton("Nulo", QtWidgets.QMessageBox.ButtonRole.YesRole)
            box.addButton("Cancelar", QtWidgets.QMessageBox.ButtonRole.RejectRole)
            resultado = box.exec_()
            print("AQUI")
            print(resultado)
            print("AQUI")
            if resultado <= 1:
                sobras = {"tipo": box.clickedButton().text().lower(), "numero": self.questao.numero_escolhas - len(self.table.selectedIndexes())}
            else:
                raise ValueError("Termine a votação")
        return {"nome": self.questao.nome, "candidatos": candidatos, "sobras": sobras}


class VotacaoUi(QtWidgets.QMainWindow):
    def __init__(self, aplicacao_controller, votacao_controller):
        self.voto_computado_window = None
        self.confirmar_window = None
        self.erro_dialog = None
        self.__controller = aplicacao_controller
        self.__votacao_controller = votacao_controller
        super().__init__()

        uic.loadUi(f"{UI_PATH}/votacoes.ui", self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.questoes_paginas: QtWidgets.QStackedWidget = self.findChild(QtWidgets.QStackedWidget, 'paginas')

        self.id_selected = None
        self.showMaximized()
        self.paginas = []
        for questao in self.__votacao_controller.paginas():
            pagina = Pagina(questao,self)
            self.questoes_paginas.addWidget(pagina)
            self.paginas.append(pagina)

    def proxima_pagina(self):
        index = self.questoes_paginas.currentIndex()
        if index < self.questoes_paginas.count() - 1:
            self.questoes_paginas.setCurrentIndex(index + 1)
        else:
            self.abrir_confirmar_window()

    def voltar(self):
        index = self.questoes_paginas.currentIndex()
        if index != 0:
            self.questoes_paginas.setCurrentIndex(index - 1)

    def abrir_confirmar_window(self):
        try:
            escolhas = {}
            for pagina in self.paginas:
                escolhas[pagina.questao.id] = pagina.selecionados()
            print("AQui")
            print(escolhas)
            self.confirmar_window = ConfirmarVotoUi(self, escolhas)
        except ValueError as e:
            self.mostrar_erro(str(e))

    def confirmar(self, escolhas):
        self.__votacao_controller.votar(escolhas)
        self.confirmar_window.close()
        self.close()
        self.voto_computado_window = VotoComputadoUi()

    def mostrar_erro(self, erro):
        self.erro_dialog = ErroUi(erro)


