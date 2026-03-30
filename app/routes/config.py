from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..crud import get_config
from ..models import Config
from ..auth import get_current_user, validar_api_key

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_config(
    db: Session = Depends(get_db),
    api_key: str = Depends(validar_api_key)
):
    config = get_config(db)
    return config


@router.put("/")
def update_config(
    nova_config: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    config = db.query(Config).first()

    if not config:
        config = Config()

    config.tempo_minutos = nova_config.get("tempo_minutos", 60)
    config.bloqueio = nova_config.get("bloqueio", True)
    config.mensagem = nova_config.get("mensagem", "Hora de se alongar!")

    db.add(config)
    db.commit()
    db.refresh(config)

    return config