# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from models.base_model import BaseModel


class Candidato(BaseModel):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    imagem = Column(String)
    questao_id = Column(Integer, ForeignKey('questoes.id'))
    questao = relationship('Questao', back_populates="candidatos")
    votos = relationship('Voto', back_populates="candidato", cascade="all, delete")

    @validates('nome')
    def validar_nome(self, key, nome):
        if len(nome) < 3 or len(nome) > 50:
            raise ValueError("Nome inválido")
        return nome
