from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, validates
from src.models.base_model import BaseModel
from src.engine import engine


class Questao(BaseModel):
    __tablename__ = 'questoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(Text)
    numero_escolhas = Column(Integer)
    eleicao_id = Column(Integer, ForeignKey('eleicoes.id'))
    eleicao = relationship('Eleicao', back_populates="questoes")


    @validates('nome')
    def validate_nome(self, key, address):
        if len(address) < 3 or len(address) > 50:
            raise ValueError("Nome inválido")
        return address

    @validates('descricao')
    def validate_nome(self, key, address):
        if len(address) < 3 or len(address) > 50:
            raise ValueError("Descricao inválida")
        return address

    @validates('numero_escolhas')
    def validate_numero_escolhas(self, key, address):
        if address < 1 or address > 10:
            raise ValueError("Número inválido de escolhas")
        return address


BaseModel.metadata.create_all(engine)