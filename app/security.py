from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, get_db

# Configurações de segurança
SECRET_KEY = "sua_chave_secreta_aqui"  # Em produção, use uma chave segura e armazene em variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração do contexto de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha"""
    return pwd_context.hash(password)

def get_user(db: Session, username: str) -> Optional[models.Usuario]:
    """Obtém um usuário pelo nome de usuário"""
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """Autentica um usuário com nome de usuário e senha"""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT de acesso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"[DEBUG] Token recebido em get_current_user: {token}")  # DEBUG
    """Obtém o usuário atual a partir do token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.Usuario = Depends(get_current_user)):
    """Verifica se o usuário atual está ativo"""
    if not current_user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

def create_first_admin_user(db: Session):
    """Cria um usuário administrador padrão se não existirem usuários"""
    if db.query(models.Usuario).count() == 0:
        admin_user = models.Usuario(
            username="admin",
            email="admin@vidracaria.com",
            nome="Administrador",
            hashed_password=get_password_hash("admin123"),
            admin=True,
            ativo=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        return admin_user
    return None
