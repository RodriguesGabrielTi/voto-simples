from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from src.models.base_model import BaseModel
from src.engine import engine

CATEGORIAS_PERMITIDAS = ['estudante', 'professor', 'tae']

class Categoria(BaseModel):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nome = Column(String)

    @validates("nome")
    def validate_nome(self, key, address):
        if address not in CATEGORIAS_PERMITIDAS:
            raise ValueError("Categoria inválida")
        return address


BaseModel.metadata.create_all(engine)
