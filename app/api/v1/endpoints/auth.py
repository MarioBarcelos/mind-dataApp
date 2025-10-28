from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import criar_token_acesso, verificar_senha
from app.db.session import obter_db
from app.services.user_service import obter_usuario_por_username
from app.schemas.token import TokenResposta

router = APIRouter()
settings = get_settings()

@router.post("/login", response_model=TokenResposta)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(obter_db)
):
    user = obter_usuario_por_username(db, form_data.username)
    if not user or not verificar_senha(form_data.password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}