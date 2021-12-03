from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from base_model import BaseModel

association_table = Table('eleicao_categoria', BaseModel.metadata,
                          Column('eleicao_id', ForeignKey('eleicao.id')),
                          Column('categoria_id'), ForeignKey('categoria.id'))


class Eleicao(BaseModel):
    __tablename__ = 'eleicoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(Text)
    estado = Column(String)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    questoes = relationship("Questao", back_populates="eleicoes", cascade="all, delete")
    categorias = relationship("Categoria", secondary=association_table)

    def __init__(self, nome, descricao):
        self.__nome = nome
        self.__descricao = descricao
        self.__estado = "editavel"
