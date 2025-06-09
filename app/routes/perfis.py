from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/perfis", response_model=list[schemas.Perfil])
def listar_perfis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_perfis(db, skip=skip, limit=limit)

@router.post("/perfis", response_model=schemas.Perfil)
def criar_perfil(perfil: schemas.PerfilBase, db: Session = Depends(get_db)):
    return crud.create_perfil(db, perfil)

@router.put("/perfis/{codigo}", response_model=schemas.Perfil)
def atualizar_perfil(codigo: str, perfil: schemas.PerfilBase, db: Session = Depends(get_db)):
    db_perfil = crud.update_perfil(db, codigo, perfil)
    if db_perfil is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return db_perfil

@router.delete("/perfis/{codigo}", response_model=schemas.Perfil)
def excluir_perfil(codigo: str, db: Session = Depends(get_db)):
    db_perfil = crud.delete_perfil(db, codigo)
    if db_perfil is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return db_perfil
