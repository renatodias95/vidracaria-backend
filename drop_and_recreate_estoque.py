# drop_and_recreate_estoque.py
# Script seguro para apagar a tabela Estoque e recriá-la conforme o modelo atual

from app.database import engine, Base
import app.models
from sqlalchemy import text

with engine.connect() as conn:
    print('Removendo tabela Estoque, se existir...')
    conn.execute(text("DROP TABLE IF EXISTS Estoque"))
    conn.commit()

print('Recriando tabelas conforme models...')
Base.metadata.create_all(bind=engine)
print('Pronto! Tabela Estoque recriada.')
