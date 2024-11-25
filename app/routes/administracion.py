from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import DatabaseManager
from app.facades.administracion_facade import AdministrationFacade
from app.schemas.user_schema import UsuarioCreate, RolBase, UsuarioResponse

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db_instance = DatabaseManager.get_instance()
    db = db_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioResponse)
def create_user(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    facade = AdministrationFacade(db)
    return facade.crear_usuario(user_data)

@router.get("/", response_model=list)
def get_all_users(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios."""
    facade = AdministrationFacade(db)
    return facade.get_users()

@router.post("/roles", response_model=dict)
def create_role(role_data: RolBase, db: Session = Depends(get_db)):
    """Crea un nuevo rol."""
    facade = AdministrationFacade(db)
    return facade.create_role(role_data)

@router.post("/roles/{role_id}/permisos", response_model=dict)
def assign_permissions(role_id: int, permissions: list[int], db: Session = Depends(get_db)):
    """Asigna permisos a un rol."""
    facade = AdministrationFacade(db)
    return facade.assign_permissions_to_role(role_id, permissions)
