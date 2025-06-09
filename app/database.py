from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

import os

# Define o caminho do banco de dados na pasta do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
import os
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'orcamentos_esquadrias_v8_sqlalchemy.db'))}"

# Cria o diretório do banco de dados se não existir
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

print(f"Conectando ao banco de dados em: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para prover sessão do banco para FastAPI
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
