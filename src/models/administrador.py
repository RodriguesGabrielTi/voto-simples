from usuario import Usuario
from sqlalchemy import Column, String


class Admistrador(Usuario):
    __tablename__ = 'administradores'

    senha = Column(String)

    def __init__(self):
        super().__init__()
