from sqlalchemy.orm import Session
from ..models.user import user
from ..schemas.user import user_create
from ..core.security import gerar_hash_senha


def criar_usuario(db: Session, usuario: user_create) -> user:
    """Cria um usuário novo. Recebe user_create (nome, username, senha).

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
    """Compatibilidade: se o projeto usar email, tenta encontrar por email.

    Nota: o modelo atual não possui campo `email` — essa função retorna None
    a menos que o modelo seja alterado para incluir `email`.
    """
    return None