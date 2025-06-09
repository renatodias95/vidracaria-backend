from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/projetos", response_model=list[schemas.Projeto])
def listar_projetos(db: Session = Depends(get_db)):
    return db.query(models.Projeto).all()

@router.post("/projetos", response_model=schemas.Projeto)
def criar_projeto(projeto: schemas.ProjetoCreate, db: Session = Depends(get_db)):
    db_projeto = models.Projeto(
        nome=projeto.nome,
        tipo=projeto.tipo,
        descricao=projeto.descricao,
        data_criacao=projeto.data_criacao or datetime.now().isoformat()
    )
    db.add(db_projeto)
    db.commit()
    db.refresh(db_projeto)
    return db_projeto
