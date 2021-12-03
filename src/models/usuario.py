from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.sql import func
from base_model import BaseModel


class Usuario(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    data_nascimento = Column(Date)
    cpf = Column(String, primary_key=True)
    endereco = Column(String)
    ativo = Column(Boolean)
    created_at = Column(Date, server_default=func.now())

    def __init__(self, nome, data_nascimento, cpf, endereco, ativo=True):
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__cpf = cpf
        self.__endereco = endereco
        self.__ativo = ativo


