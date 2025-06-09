from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import get_db

router = APIRouter()

from app import schemas

@router.get("/acessorios", response_model=list[schemas.AcessorioBase])
def listar_acessorios(db: Session = Depends(get_db)):
    return db.query(models.Acessorio).all()
