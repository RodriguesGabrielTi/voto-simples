from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel


class Questao(BaseModel):
    __tablename__ = 'questoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(Text)
    numero_escolhas = Column(Integer)
    eleicao_id = Column(Integer, ForeignKey('eleicao.id'))
    eleicao = relationship('Eleicao', back_populates="questoes")

    def __init__(self, nome, descricao, numero_escolhas):
        self.__nome = nome
        self.__descricao = descricao
        self.__numero_escolhas = numero_escolhas
