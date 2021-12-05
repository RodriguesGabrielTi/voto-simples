from PyQt5 import QtWidgets
import sys

from controllers.aplicacao_controller import AplicacaoController
from engine import engine
from sqlalchemy.orm import sessionmaker
from carregar_dados import carregar


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Session = sessionmaker(bind=engine)
    with Session() as sessao:
        with sessao.begin():
            carregar(sessao)
            AplicacaoController(sessao).abrir()
    app.exec_()

