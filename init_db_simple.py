import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona o diretório pai ao path para permitir importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models import Usuario
from app.security import get_password_hash

def init_db():
    print("Criando tabelas no banco de dados...")
    
    # Cria todas as tabelas definidas nos modelos
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verifica se já existe algum usuário
        if db.query(Usuario).count() == 0:
            print("Criando usuário administrador padrão...")
            
            # Cria o usuário administrador
            admin_user = Usuario(
                username="admin",
                email="admin@vidracaria.com",
                nome="Administrador",
                hashed_password=get_password_hash("admin123"),
                admin=True,
                ativo=True
            )
            
            db.add(admin_user)
            db.commit()
            print("Usuário administrador criado com sucesso!")
            print("Username: admin")
            print("Senha: admin123")
            print("\nIMPORTANTE: Altere a senha padrão após o primeiro login!")
        else:
            print("Banco de dados já inicializado. Nenhuma alteração necessária.")
            
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()