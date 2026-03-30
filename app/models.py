from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True, index=True)
    tempo_minutos = Column(Integer, default=60)
    bloqueio = Column(Boolean, default=True)
    mensagem = Column(String)

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_windows = Column(String)
    horario_alerta = Column(DateTime)
    horario_confirmacao = Column(DateTime)
    tempo_ativo = Column(Integer)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)
    tipo = Column(String)  # admin ou rh