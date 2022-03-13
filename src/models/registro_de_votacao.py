from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class RegistroDeVotacao(BaseModel):
    __tablename__ = 'registros_de_votacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    eleicao_id = Column(Integer, ForeignKey('eleicoes.id'))
    eleicao = relationship("Eleicao")
    votante_id = Column(Integer, ForeignKey('votantes.id'))
    votante = relationship("Votante")
