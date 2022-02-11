from models.usuario import Usuario
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Votante(Usuario):
    __tablename__ = 'votantes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    categoria = relationship("Categoria")