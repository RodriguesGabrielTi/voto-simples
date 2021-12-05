from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship, validates
from src.models.base_model import BaseModel
from src.models.categoria import Categoria # não é possível criar o banco de dados sem esse import
from src.engine import engine

association_table = Table('eleicao_categoria', BaseModel.metadata,
                          Column('eleicao_id', ForeignKey('eleicoes.id')),
                          Column('categoria_id', ForeignKey('categorias.id')))


class Eleicao(BaseModel):
    __tablename__ = 'eleicoes'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(Text)
    estado = Column(String)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    questoes = relationship("Questao", back_populates="eleicao", cascade="all, delete")
    categorias = relationship("Categoria", secondary=association_table)

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


BaseModel.metadata.create_all(engine)
