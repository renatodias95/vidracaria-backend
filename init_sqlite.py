import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Configuração do SQLAlchemy
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///C:/Users/renat/OneDrive/Área de Trabalho/renatodias/orcamentos_esquadrias_v8_sqlalchemy.db"
print(f"Conectando ao banco de dados em: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Usuário
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    nome = Column(String)
    hashed_password = Column(String)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Função para criar hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init_db():
    print("Criando tabelas no banco de dados (apenas as que faltam, sem afetar as existentes)...")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
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