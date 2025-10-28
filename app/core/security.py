from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from .config import get_settings
from ..schemas.token import CargaToken

settings = get_settings()

# OAuth2PasswordBearer para extrair e validar o token JWT
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def _truncate_password_to_72_bytes(senha: str | bytes) -> bytes:
    """Encode senha para bytes em UTF-8 e trunca para 72 bytes (limite do bcrypt).

    Retornamos bytes porque o backend bcrypt opera em bytes.
    """
    if isinstance(senha, str):
        b = senha.encode("utf-8")
    else:
        b = senha
    if len(b) > 72:
        return b[:72]
    return b


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica a senha plana contra o hash. Trunca a senha para 72 bytes antes.

    Se ocorrer um erro de backend (ex.: ValueError por comprimento), retorna False.
    """
    try:
        # Certifica-se que a senha está em bytes e truncada em 72 bytes
        senha_bytes = senha_plana.encode('utf-8')[:72]
        hash_bytes = senha_hash.encode('utf-8')
        
        return bcrypt.checkpw(senha_bytes, hash_bytes)
    except Exception as e:
        print(f"Erro na verificação da senha: {str(e)}")  # Para debug
        return False
    


def gerar_hash_senha(senha: str) -> str:
    """Gera hash para a senha; trunca para 72 bytes antes de hashear (bcrypt).

    Observação: truncamos para manter compatibilidade com a limitação do bcrypt.
    """
    try:
        senha_bytes = senha.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha_bytes, salt)
        return hash_bytes.decode('utf-8')
    except Exception as e:
        print(f"Erro ao gerar hash da senha: {str(e)}")  # Para debug
        raise


def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def obter_token_usuario_atual(token: str = Depends(oauth2_esquema)) -> CargaToken:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = CargaToken(sub=username)
    except JWTError:
        raise credentials_exception
    return token_data