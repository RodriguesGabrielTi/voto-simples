from models.base_model import BaseModel
from sqlalchemy import Column, Integer, ForeignKey


class EleicaoMesario(BaseModel):
    __tablename__ = 'eleicao_mesario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    eleicao_id = Column(Integer, ForeignKey('eleicoes.id'))
    mesario_id = Column(Integer, ForeignKey('mesarios.id'))
