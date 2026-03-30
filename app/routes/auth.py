from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import UsuarioCreate, UsuarioLogin
from ..crud import criar_usuario, autenticar_usuario
from ..auth import criar_token, get_current_user
import os

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    if current_user.get("tipo") != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem registrar usuários")
    
    return criar_usuario(db, usuario)

@router.post("/login")
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    user = autenticar_usuario(db, dados.email, dados.senha)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({"sub": user.email, "tipo": user.tipo})

    return {
        "access_token": token,
        "tipo": user.tipo
    }