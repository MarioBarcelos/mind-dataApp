from sqlalchemy.orm import Session
from ..models.user import user
from ..schemas.user import user_create
from ..core.security import gerar_hash_senha
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto")


def criar_usuario(db: Session, usuario: user_create) -> user:
    """Criar um usuário. Recebe user_create (nome, username, senha).
    A senha é hasheada antes de salvar no campo `senha`.
    """
    db_user = user(
        nome=usuario.nome,
        username=usuario.username,
        senha=gerar_hash_senha(usuario.senha),
        ativo=True,
        observacoes=getattr(usuario, "observacoes", None),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def obter_usuario_por_username(db: Session, username: str) -> user | None:
    return db.query(user).filter(user.username == username).first()


def obter_usuario_por_email(db: Session, email: str) -> user | None:
    return None

def consultar_usuarios_ativo(db: Session, username: str) -> list[user]:
    return db.query(user).filter(user.ativo == 1).all()