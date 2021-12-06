# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from models.base_model import BaseModel
import re


class Usuario(BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    data_nascimento = Column(Date)
    cpf = Column(String, primary_key=True)
    endereco = Column(String)
    ativo = Column(Boolean, default=True)
    criado_em = Column(Date, server_default=func.now())

    @validates('nome')
    def validar_nome(self, key, nome):
        if len(nome) < 3 or len(nome) > 50:
            raise ValueError("Nome inválido")
        return nome

    @validates('email')
    def validar_email(self, key, email):
        if '@' not in email:
            raise ValueError("Email inválido")
        return email

    @validates('cpf')
    def validar_cpf(self, key, cpf):
        valido = re.compile("([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})")
        if not valido.match(cpf):
            raise ValueError("Cpf invalido")
        return cpf

    @validates('endereco')
    def validar_endereco(self, key, endereco):
        if len(endereco) < 3 or len(endereco) > 50:
            raise ValueError("Endereço inválido")
        return endereco
