from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import get_db

router = APIRouter()

from app import schemas

@router.get("/vidros", response_model=list[schemas.VidroBase])
def listar_vidros(db: Session = Depends(get_db)):
    return db.query(models.Vidro).all()
