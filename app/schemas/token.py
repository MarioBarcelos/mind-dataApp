from pydantic import BaseModel


class TokenResposta(BaseModel):
    access_token: str
    token_type: str


class CargaToken(BaseModel):
    sub: str | None = None