import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona o diretório pai ao path para permitir importações
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, SessionLocal
from app.models import Perfil, Orcamento, ItemOrcamento, Acessorio, Estoque, Projeto, Vidro, Usuario
from app.security import get_password_hash

def init_db():
    print("Criando tabelas no banco de dados...")
    
    # Cria todas as tabelas definidas nos modelos
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
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
        print(f"Usuário administrador criado com sucesso!")
        print(f"Username: admin")
        print(f"Senha: admin123")
        print("\nIMPORTANTE: Altere a senha padrão após o primeiro login!")
    
    db.close()
    print("\nBanco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_db()
