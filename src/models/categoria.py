from sqlalchemy import Column, Integer, String
from base_model import BaseModel


class Categoria(BaseModel):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)

    CATEGORIAS_PERMITIDAS = ['estudante', 'professor', 'tae']
