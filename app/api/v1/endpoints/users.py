from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import obter_db
from ...services.user_service import criar_usuario, obter_usuario_por_username
from ...schemas.user import user as user_schema, user_create as user_create_schema
from ...core.security import obter_token_usuario_atual
from ...schemas.token import CargaToken

router = APIRouter()


@router.post("/usuarios/", response_model=user_schema)
def criar_novo_usuario(usuario: user_create_schema, db: Session = Depends(obter_db)):
    # Validação de unicidade: impede criação de usuário com mesmo username
    existente = obter_usuario_por_username(db, usuario.username)
    if existente:
        raise HTTPException(status_code=409, detail="Username já existe")

    db_user = criar_usuario(db=db, usuario=usuario)
    return db_user


@router.get("/usuarios/me", response_model=user_schema)
async def ler_usuario_atual(
    usuario_atual: CargaToken = Depends(obter_token_usuario_atual),
    db: Session = Depends(obter_db)
):
    """
    Endpoint protegido que requer um token JWT válido
    """
    db_user = obter_usuario_por_username(db, usuario_atual.sub)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user