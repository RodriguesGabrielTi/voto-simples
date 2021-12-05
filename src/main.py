from src.controllers.application_controller import ApplicationController
from engine import engine
from sqlalchemy.orm import sessionmaker
from src.models.categoria import Categoria


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    with Session() as session:
        with session.begin():
            if len(session.query(Categoria).all()) == 0:
                estudante = Categoria(nome="estudante")
                professor = Categoria(nome="professor")
                tae = Categoria(nome="tae")

                session.add(estudante)
                session.add(professor)
                session.add(tae)

                session.commit()

            ApplicationController(session).abrir()
