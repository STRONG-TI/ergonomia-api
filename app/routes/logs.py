from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import LogCreate
from ..crud import create_log
from ..auth import validar_api_key
from fastapi.responses import StreamingResponse
import csv
import io
from ..models import Log
from ..auth import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_new_log(
    log: LogCreate,
    db: Session = Depends(get_db),
    api_key=Depends(validar_api_key)
):
    return create_log(db, log)


@router.get("/export")
def export_logs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    logs = db.query(Log).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "usuario",
        "alerta",
        "confirmacao",
        "tempo_ativo"
    ])

    for log in logs:
        writer.writerow([
            log.usuario_windows,
            log.horario_alerta,
            log.horario_confirmacao,
            log.tempo_ativo
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=relatorio.csv"
        }
    )