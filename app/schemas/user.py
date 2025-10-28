from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Schema de criação (nome do schema coincide com o arquivo: user_create)
class user_create(BaseModel):
    nome: str
    username: str
    senha: str
    observacoes: Optional[str] = None


# Schema de retorno (nome do schema coincide com o arquivo: user)
class user(BaseModel):
    id: str
    nome: str
    username: str
    ativo: bool
    data_criacao: datetime
    observacoes: Optional[str] = None

    model_config = {
        "from_attributes": True
    }