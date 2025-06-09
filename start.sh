#!/bin/bash

# Instala as dependências
pip install -r requirements.txt

# Executa as migrações do banco de dados (se necessário)
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Inicia o servidor
uvicorn app.main:app --host 0.0.0.0 --port $PORT
