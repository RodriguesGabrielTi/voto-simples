from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from models.base_model import BaseModel


CATEGORIAS_PERMITIDAS = ['estudante', 'professor', 'tae']


class Categoria(BaseModel):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)

    @validates("nome")
    def validar_nome(self, key, nome):
        if nome not in CATEGORIAS_PERMITIDAS:
            raise ValueError("Categoria inválida")
        return nome



