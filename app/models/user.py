from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func
from ..db.base import Base


class user(Base):
    """Modelo de usuário com nome de classe igual ao nome do arquivo: `user`.

    Mantemos `__tablename__ = 'user'` para compatibilidade com a migration já
    aplicada no banco.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    username = Column(String(150), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)  # Armazene senha já hasheada
    ativo = Column(Boolean(), default=True, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    observacoes = Column(Text, nullable=True)