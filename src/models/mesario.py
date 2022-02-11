from models.usuario import Usuario
from sqlalchemy import Column, Integer, String


class Mesario(Usuario):
    __tablename__ = 'mesarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    senha = Column(String)
