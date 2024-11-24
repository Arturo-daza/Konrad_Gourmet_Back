from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.middlewares.jwt_bearer import JWTBearer
from app.utils.database import DatabaseManager
from app.facades.plato_facade import PlatoFacade
from app.schemas import PlatoCreate, PlatoUpdate, PlatoResponse
from app.managers.seguridad_manager import SeguridadManager
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

def get_db():
    db_instance = DatabaseManager.get_instance()
    db = db_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlatoResponse, dependencies=[Depends(JWTBearer())])
def crear_plato(
    plato_data: PlatoCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Crea un nuevo plato."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Crear Plato"):
        raise HTTPException(status_code=403, detail="No tienes permisos para crear platos.")

    facade = PlatoFacade(db)
    return facade.crear_plato(plato_data)

@router.get("/", response_model=list[PlatoResponse], dependencies=[Depends(JWTBearer())])
def listar_platos(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Lista todos los platos."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Listar Platos"):
        raise HTTPException(status_code=403, detail="No tienes permisos para listar platos.")

    facade = PlatoFacade(db)
    return facade.listar_platos()

@router.get("/{id_plato}", response_model=PlatoResponse, dependencies=[Depends(JWTBearer())])
def obtener_plato(
    id_plato: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Obtiene un plato por su ID."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Consultar Plato"):
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar platos.")

    facade = PlatoFacade(db)
    return facade.obtener_plato(id_plato)

@router.put("/{id_plato}", response_model=PlatoResponse, dependencies=[Depends(JWTBearer())])
def actualizar_plato(
    id_plato: int,
    plato_data: PlatoUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Actualiza un plato."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Actualizar Plato"):
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar platos.")

    facade = PlatoFacade(db)
    return facade.actualizar_plato(id_plato, plato_data)

@router.delete("/{id_plato}", dependencies=[Depends(JWTBearer())])
def eliminar_plato(
    id_plato: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Elimina un plato."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Eliminar Plato"):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar platos.")

    facade = PlatoFacade(db)
    return facade.eliminar_plato(id_plato)
