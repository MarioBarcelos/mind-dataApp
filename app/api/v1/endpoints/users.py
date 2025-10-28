from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from http import HTTPStatus
from app.db.session import obter_db
from app.services.user_service import *
from app.schemas.user import user as user_schema, user_create as user_create_schema
from app.core.security import obter_token_usuario_atual
from app.schemas.token import CargaToken

router = APIRouter()


@router.post("/usuarios/", response_model=user_schema)
def criar_novo_usuario(usuario: user_create_schema, db: Session = Depends(obter_db)):
    # Validação de unicidade: impede criação de usuário com mesmo username
    existente = obter_usuario_por_username(db, usuario.username)
    if existente:
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="Username já existe")

    dbUser = criar_usuario(db=db, usuario=usuario)
    return dbUser


@router.get("/usuarios/meusDetalhes", response_model=user_schema)
async def ler_usuario_atual(
    usuario_atual: CargaToken = Depends(obter_token_usuario_atual),
    db: Session = Depends(obter_db)
):
    dbUser = obter_usuario_por_username(db, usuario_atual.sub)
    if dbUser is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST.value, detail="Usuário não encontrado")
    return dbUser

@router.get("/usuarios/ativos", response_model=list[user_schema])
async def ler_usuarios_ativos(
    usuario_atual: CargaToken = Depends(obter_token_usuario_atual),
    db: Session = Depends(obter_db)     
):
    dbUsers = consultar_usuarios_ativo(db, usuario_atual.sub)
    if not dbUsers:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND.value, detail="Não há usuários ativos no Sistema.")
    return dbUsers