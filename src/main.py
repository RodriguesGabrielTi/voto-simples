from controllers.aplicacao_controller import AplicacaoController
from engine import engine
from sqlalchemy.orm import sessionmaker
from carregar_dados import carregar


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    with Session() as sessao:
        carregar(sessao)
        AplicacaoController(sessao).iniciar()

