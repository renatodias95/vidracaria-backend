from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import os

# Caminho para o banco de dados
DATABASE_URL = f"sqlite:///{os.path.join(os.getcwd(), 'orcamentos_esquadrias_v8_sqlalchemy.db')}"

# Criar engine e sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Obter o inspetor
    inspector = inspect(engine)
    
    # Listar todas as tabelas
    print("\n=== TABELAS NO BANCO DE DADOS ===")
    tabelas = inspector.get_table_names()
    for tabela in tabelas:
        print(f"\nTabela: {tabela}")
        print("Colunas:")
        for coluna in inspector.get_columns(tabela):
            print(f"  - {coluna['name']} ({coluna['type']})")
    
    # Verificar se a tabela PerfisAluminio existe
    if 'PerfisAluminio' in tabelas:
        print("\n=== ESTRUTURA DA TABELA PerfisAluminio ===")
        for col in inspector.get_columns('PerfisAluminio'):
            print(f"{col['name']} ({col['type']})")
    else:
        print("\n[ERRO] A tabela 'PerfisAluminio' não foi encontrada no banco de dados!")
        print("Tabelas disponíveis:", ", ".join(tabelas))
    
except Exception as e:
    print(f"\n[ERRO] {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    db.close()

print("\nScript concluído.")
