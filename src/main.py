from src.controllers.aplicacao_controller import AplicacaoController
from engine import engine
from sqlalchemy.orm import sessionmaker
from src.carregar_dados import carregar


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    with Session() as sessao:
        with sessao.begin():
            carregar(sessao)
            AplicacaoController(sessao).abrir()
