from sqlalchemy.orm import Session
from . import models, schemas

def get_perfis(db: Session, skip: int = 0, limit: int = 100):
    try:
        # Primeiro, verificar as colunas existentes na tabela
        from sqlalchemy import inspect, text
        
        # Verificar se a coluna origem existe
        inspector = inspect(db.connection())
        columns = [col['name'] for col in inspector.get_columns('PerfisAluminio')]
        
        # Selecionar apenas as colunas existentes
        colunas_disponiveis = [
            'codigo', 'descricao', 'preco_barra', 'peso_kg_por_metro',
            'unidade_medida', 'fornecedor'
        ]
        
        # Filtrar apenas as colunas que existem na tabela
        colunas_selecionadas = [col for col in colunas_disponiveis if col in columns]
        
        # Adicionar a coluna origem com valor padrão 'parceiro'
        colunas_sql = ', '.join(colunas_selecionadas)
        colunas_sql += ", 'parceiro' as origem"
        
        query = text(f"""
            SELECT {colunas_sql}
            FROM PerfisAluminio
            LIMIT :limit OFFSET :offset
        """)
        
        print(f"[DEBUG] Executando query: {query}")
        result = db.execute(query, {"limit": limit, "offset": skip})
        
        # Converter o resultado em dicionário
        perfis = []
        for row in result:
            perfil = dict(row._mapping)
            # Garantir que temos a chave 'origem' no dicionário
            if 'origem' not in perfil:
                perfil['origem'] = 'parceiro'
            perfis.append(perfil)
        
        print(f"[DEBUG] Retornando {len(perfis)} perfis")
        if perfis:
            print(f"[DEBUG] Primeiro perfil: {perfis[0]}")
        return perfis
        
    except Exception as e:
        print(f"[ERROR] Erro ao buscar perfis: {str(e)}")
        print(f"[ERROR] Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise

def create_perfil(db: Session, perfil: schemas.PerfilBase):
    db_perfil = models.Perfil(**perfil.dict())
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

def update_perfil(db: Session, codigo: str, perfil: schemas.PerfilBase):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.codigo == codigo).first()
    if not db_perfil:
        return None
    for attr, value in perfil.dict().items():
        setattr(db_perfil, attr, value)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil

def delete_perfil(db: Session, codigo: str):
    db_perfil = db.query(models.Perfil).filter(models.Perfil.codigo == codigo).first()
    if not db_perfil:
        return None
    db.delete(db_perfil)
    db.commit()
    return db_perfil
