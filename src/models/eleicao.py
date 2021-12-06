from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship, validates
from models.base_model import BaseModel
from models.categoria import Categoria  # não é possível criar o banco de dados sem esse import
from engine import engine

association_table = Table('eleicao_categoria', BaseModel.metadata,
                          Column('eleicao_id', ForeignKey('eleicoes.id')),
                          Column('categoria_id', ForeignKey('categorias.id')))


class Eleicao(BaseModel):
    __tablename__ = 'eleicoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(Text)
    estado = Column(String, default="em edicao")
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    questoes = relationship("Questao", back_populates="eleicao", cascade="all, delete")
    categorias = relationship("Categoria", secondary=association_table)

    @validates('nome')
    def validar_nome(self, key, nome):
        if len(nome) < 3 or len(nome) > 50:
            raise ValueError("Nome inválido")
        return nome

    @validates('descricao')
    def validar_descricao(self, key, descricao):
        if len(descricao) < 3 or len(descricao) > 50:
            raise ValueError("Descricao inválida")
        return descricao


BaseModel.metadata.create_all(engine)
