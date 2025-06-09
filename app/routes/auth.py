from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["autenticacao"])

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica o usuário e retorna um token de acesso JWT.
    """
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint temporário para criar admin
@router.post("/admin/create", tags=["admin"])
def create_admin(db: Session = Depends(get_db)):
    """
    Cria o usuário admin padrão (admin/admin123) se não existir.
    """
    admin = security.create_first_admin_user(db)
    if admin:
        return {"msg": "Usuário admin criado!", "username": admin.username}
    return {"msg": "Usuário admin já existe."}

@router.post("/register", response_model=schemas.Usuario)
def register_user(
    user: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(security.get_current_active_user)
):
    """
    Registra um novo usuário. Apenas administradores podem registrar novos usuários.
    """
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem registrar novos usuários"
        )
    
    # Verifica se o nome de usuário já está em uso
    db_user = security.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já cadastrado"
        )
    
    # Verifica se o e-mail já está em uso
    db_email = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado"
        )
    
    # Cria o novo usuário
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Usuario(
        username=user.username,
        email=user.email,
        nome=user.nome,
        hashed_password=hashed_password,
        admin=user.admin,
        ativo=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/me", response_model=schemas.Usuario)
async def read_users_me(current_user: models.Usuario = Depends(security.get_current_active_user)):
    """
    Retorna as informações do usuário atualmente autenticado.
    """
    return schemas.Usuario.from_orm(current_user)
