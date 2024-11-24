from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import DatabaseManager
from app.managers.seguridad_manager import SeguridadManager
from app.schemas.auth_schema import Token

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db_instance = DatabaseManager.get_instance()
    db = db_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/token", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token."""
    manager = SeguridadManager(db)
    token = manager.autenticar_usuario(email=username, password=password)
    return Token(access_token=token, token_type="bearer")

