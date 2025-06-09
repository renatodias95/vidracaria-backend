from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/orcamentos", response_model=list[schemas.OrcamentoComItens])
def listar_orcamentos(db: Session = Depends(get_db)):
    orcamentos = db.query(models.Orcamento).all()
    resultados = []
    for orc in orcamentos:
        itens = db.query(models.ItemOrcamento).filter(models.ItemOrcamento.orcamento_id == orc.id).all()
        itens_dict = [schemas.ItemOrcamentoBase.model_validate(item.__dict__) for item in itens]
        orc_dict = orc.__dict__.copy()
        orc_dict["itens"] = itens_dict
        resultados.append(schemas.OrcamentoComItens(**orc_dict))
    return resultados
