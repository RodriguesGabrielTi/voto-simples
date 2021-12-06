from models.usuario import Usuario, BaseModel
from engine import engine
from sqlalchemy import Column, Integer, String


class Administrador(Usuario):
    __tablename__ = 'administradores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    senha = Column(String)


BaseModel.metadata.create_all(engine)
