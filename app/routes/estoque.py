from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/estoque", response_model=list[schemas.Estoque])
def listar_estoque(db: Session = Depends(get_db)):
    return db.query(models.Estoque).all()

@router.post("/estoque", response_model=schemas.Estoque)
def adicionar_estoque(item: schemas.EstoqueCreate, db: Session = Depends(get_db)):
    db_item = models.Estoque(**item.dict(), data_atualizacao=datetime.now().isoformat())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/estoque/{item_id}", response_model=schemas.Estoque)
def atualizar_estoque(item_id: int, item: schemas.EstoqueCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Estoque).filter(models.Estoque.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db_item.data_atualizacao = datetime.now().isoformat()
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/estoque/{item_id}")
def remover_estoque(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Estoque).filter(models.Estoque.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(db_item)
    db.commit()
    return {"ok": True}
