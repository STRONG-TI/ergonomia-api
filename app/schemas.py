from pydantic import BaseModel
from datetime import datetime

class ConfigResponse(BaseModel):
    tempo_minutos: int
    bloqueio: bool
    mensagem: str

class LogCreate(BaseModel):
    usuario_windows: str
    horario_alerta: datetime
    horario_confirmacao: datetime
    tempo_ativo: int

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"