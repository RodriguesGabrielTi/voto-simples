from models.base_model import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Voto(BaseModel):
    __tablename__ = 'voto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidato_id = Column(Integer, ForeignKey('candidatos.id'))
    candidato = relationship('Candidato', back_populates="votos")



