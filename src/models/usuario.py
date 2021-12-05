from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from src.models.base_model import BaseModel
import re


class Usuario(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    data_nascimento = Column(Date)
    cpf = Column(String, primary_key=True)
    endereco = Column(String)
    ativo = Column(Boolean)
    created_at = Column(Date, server_default=func.now())

    @validates('nome')
    def validate_nome(self, key, address):
        if len(address) < 3 or len(address) > 50:
            raise ValueError("Nome inválido")
        return address

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Email inválido")
        return address

    @validates('cpf')
    def validate_cpf(self, key, address):
        valido = re.compile("([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})")
        if not valido.match(address):
            raise ValueError("Cpf invalido")
        return address

    @validates('endereco')
    def validate_endereco(self, key, address):
        if len(address) < 3 or len(address) > 50:
            raise ValueError("Endereço inválido")
        return address

