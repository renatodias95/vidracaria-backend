from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models import Orcamento, ItemOrcamento
import os

def check_db():
    # Caminho para o banco de dados
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    
    # Verifica se o arquivo do banco de dados existe
    if not os.path.exists(db_path):
        print(f"Erro: O arquivo do banco de dados não foi encontrado em {db_path}")
        return
    
    print(f"Banco de dados encontrado em: {db_path}")
    
    # Cria uma conexão com o banco de dados
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Verifica se a tabela de orçamentos existe
    inspector = inspect(engine)
    if 'Orcamentos' not in inspector.get_table_names():
        print("Aviso: A tabela 'Orcamentos' não foi encontrada no banco de dados.")
        print("Tabelas disponíveis:", inspector.get_table_names())
        return
    
    # Conta o número de orçamentos na tabela
    try:
        orcamentos_count = session.query(Orcamento).count()
        print(f"Número de orçamentos encontrados: {orcamentos_count}")
        
        if orcamentos_count > 0:
            # Mostra os 5 primeiros orçamentos
            print("\nPrimeiros orçamentos:")
            for orc in session.query(Orcamento).limit(5).all():
                print(f"- ID: {orc.id}, Número: {orc.numero_orcamento}, Cliente: {orc.cliente_nome}")
        
    except Exception as e:
        print(f"Erro ao consultar orçamentos: {str(e)}")

if __name__ == "__main__":
    check_db()
