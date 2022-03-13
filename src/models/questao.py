from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, validates
from models.base_model import BaseModel


class Questao(BaseModel):
    __tablename__ = 'questoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(Text)
    numero_escolhas = Column(Integer)
    candidatos = relationship("Candidato", back_populates="questao", cascade="all, delete")
    eleicao_id = Column(Integer, ForeignKey('eleicoes.id'))
    eleicao = relationship("Eleicao", back_populates="questoes")
    nulos = Column(Integer, default=0)
    brancos = Column(Integer, default=0)

    @validates('nome')
    def validar_nome(self, key, nome):
        if len(nome) < 3 or len(nome) > 50:
            raise ValueError("Nome inválido")
        return nome

    @validates('descricao')
    def validate_descricao(self, key, descricao):
        if len(descricao) < 3 or len(descricao) > 50:
            raise ValueError("Descricao inválida")
        return descricao

    @validates('numero_escolhas')
    def validate_numero_escolhas(self, key, address):
        if address < 1 or address > 10:
            raise ValueError("Número inválido de escolhas")
        return address



