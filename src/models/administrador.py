from src.models.usuario import Usuario, BaseModel
from src.engine import engine
from sqlalchemy import Column, String


class Admistrador(Usuario):
    __tablename__ = 'administradores'

    senha = Column(String)


BaseModel.metadata.create_all(engine)
