from sqlalchemy.orm import Session
from . import models
from .auth import hash_senha

def get_config(db: Session):
    return db.query(models.Config).first()

def create_log(db: Session, log):
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def criar_usuario(db, usuario):
    db_user = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha),
        tipo=usuario.tipo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def autenticar_usuario(db, email, senha):
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not user:
        return None
    from .auth import verificar_senha
    if not verificar_senha(senha, user.senha_hash):
        return None
    return user