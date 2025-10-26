from fastapi import FastAPI
from .core.config import get_settings
from .api.v1.endpoints import auth, users

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

# Include routers (rotas em português)
app.include_router(auth.router, prefix="/api/v1", tags=["autenticacao"])
app.include_router(users.router, prefix="/api/v1", tags=["usuarios"])