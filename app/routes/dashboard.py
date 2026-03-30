# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from ..database import SessionLocal
# from ..models import Log
# from ..auth import get_current_user

# router = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.get("/")
# def dashboard(db: Session = Depends(get_db), user=Depends(get_current_user)):
#     total_alertas = db.query(Log).count()

#     confirmados = db.query(Log).filter(Log.horario_confirmacao != None).count()

#     tempo_medio = db.query(func.avg(Log.tempo_ativo)).scalar()

#     return {
#         "total_alertas": total_alertas,
#         "confirmados": confirmados,
#         "tempo_medio": tempo_medio
#     }

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..database import SessionLocal
from ..models import Log
from ..auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    total_alertas = db.query(Log).count()

    confirmados = db.query(Log).filter(
        Log.horario_confirmacao != None
    ).count()

    tempo_medio = db.query(func.avg(Log.tempo_ativo)).scalar() or 0


    sete_dias = datetime.now() - timedelta(days=7)

    dados = (
        db.query(
            func.date(Log.horario_alerta),
            func.count()
        )
        .filter(Log.horario_alerta >= sete_dias)
        .group_by(func.date(Log.horario_alerta))
        .all()
    )

    return {
        "total_alertas": total_alertas,
        "confirmados": confirmados,
        "tempo_medio": round(tempo_medio, 2),
        "alertas_por_dia": [
            {"data": str(d[0]), "total": d[1]} for d in dados
        ]
    }